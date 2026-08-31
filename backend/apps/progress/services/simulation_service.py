"""
Guardelio — Simulation Service
The core engine that powers every cybersecurity incident simulation.

Public API (called from views.py):
  start_simulation(student, scenario_id)  → (SimulationSession, bool is_new)
  process_step_response(session, student, option_id=None) → dict result_payload
  get_session_result(session_id, student) → dict result_payload

Internal helpers (private):
  _get_next_step(current_step, chosen_option) → ScenarioStep | None
  _complete_session(session, student)
  _build_step_response(session, step) → dict
  _build_result_payload(session) → dict

Design principles:
  - Entire simulate/respond cycle is wrapped in @transaction.atomic
  - SessionDecision is immutable — created once, never updated
  - XP awarded only on correct decisions and completion bonuses
  - BadgeService called exactly once per session completion
  - Engine supports unlimited scenarios without code modification
"""

from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from apps.scenarios.models import Scenario, ScenarioStep, DecisionOption
from apps.scenarios.serializers import ScenarioStepSimulationSerializer
from apps.progress.models import SimulationSession, SessionDecision, XPHistory
from apps.progress.services import xp_service, badge_service
from apps.accounts.services import update_last_active


# ─── Public Interface ──────────────────────────────────────────────────────────

@transaction.atomic
def start_simulation(student, scenario_id: int) -> tuple:
    """
    Starts a new simulation session or resumes an existing in-progress one.

    Rules:
      - If an in_progress session exists for this student+scenario, resume it.
      - Otherwise, create a new session starting at the first active step.
      - Abandoned sessions are not resumed — a new session is created instead.

    Returns:
        (SimulationSession, is_new: bool)

    Raises:
        Scenario.DoesNotExist — if scenario not found or not active
        ValueError            — if scenario has no steps
    """
    scenario = get_object_or_404(Scenario, pk=scenario_id, is_active=True)

    # Check for an existing in-progress session
    existing = SimulationSession.objects.filter(
        student=student,
        scenario=scenario,
        status=SimulationSession.Status.IN_PROGRESS,
    ).select_related('current_step').first()

    if existing:
        update_last_active(student)
        return existing, False   # Resuming

    # Get the first active step
    first_step = (
        ScenarioStep.objects
        .filter(scenario=scenario, is_active=True)
        .order_by('step_number')
        .first()
    )
    if not first_step:
        raise ValueError(f'Scenario "{scenario.title}" has no active steps. Contact an administrator.')

    session = SimulationSession.objects.create(
        student=student,
        scenario=scenario,
        scenario_version=scenario.version,
        status=SimulationSession.Status.IN_PROGRESS,
        current_step=first_step,
        total_xp_earned=0,
        correct_decisions=0,
        total_decisions=0,
    )

    update_last_active(student)
    return session, True   # New session


@transaction.atomic
def process_step_response(session: SimulationSession, student, option_id: int = None) -> dict:
    """
    Processes the student's response to the current step.

    For INFO steps:
        option_id is None — the step is acknowledged and simulation advances.

    For DECISION / QUIZ steps:
        option_id must reference a valid DecisionOption for the current step.
        XP is awarded if the chosen option is_correct.
        A SessionDecision record is created (immutable audit log).

    Returns a dict with keys:
        feedback        — dict with is_correct, feedback_text, xp_earned, consequence_type
                          (None for info steps)
        next_step       — ScenarioStep instance or None (if final step)
        session_status  — 'in_progress' | 'completed'
        session_data    — summary of session stats so far

    Raises:
        PermissionError  — if session does not belong to student
        ValueError       — if session is not in_progress
        DecisionOption.DoesNotExist — if option_id invalid for this step
    """
    # Ownership and state validation
    if session.student_id != student.pk:
        raise PermissionError('This session does not belong to you.')
    if session.status != SimulationSession.Status.IN_PROGRESS:
        raise ValueError('This simulation session is not active. Start a new session.')

    current_step = session.current_step
    if current_step is None:
        raise ValueError('Session has no current step. This session may be corrupted.')

    # Already responded to this step?
    if SessionDecision.objects.filter(session=session, step=current_step).exists():
        raise ValueError('You have already responded to this step.')

    # ── Process the response ──────────────────────────────────────────────────
    chosen_option = None
    xp_earned     = 0
    feedback      = None

    if current_step.step_type in (ScenarioStep.StepType.DECISION, ScenarioStep.StepType.QUIZ):
        if not option_id:
            raise ValueError('option_id is required for decision and quiz steps.')

        # Validate the option belongs to the current step
        try:
            chosen_option = DecisionOption.objects.get(pk=option_id, step=current_step)
        except DecisionOption.DoesNotExist:
            raise ValueError(f'Option #{option_id} is not valid for this step.')

        xp_earned = chosen_option.xp_awarded

        # Update session counters
        session.total_decisions += 1
        if chosen_option.is_correct:
            session.correct_decisions += 1
        session.total_xp_earned += xp_earned

        # Award XP to the user (atomic F() update + XPHistory record)
        if xp_earned > 0:
            xp_service.award_xp(
                user=student,
                amount=xp_earned,
                session=session,
                transaction_type=XPHistory.TransactionType.STEP_CORRECT,
            )

        feedback = {
            'is_correct':       chosen_option.is_correct,
            'feedback_text':    chosen_option.feedback_text,
            'consequence_type': chosen_option.consequence_type,
            'xp_earned':        xp_earned,
        }

    # ── Create immutable audit record ─────────────────────────────────────────
    SessionDecision.objects.create(
        session=session,
        step=current_step,
        chosen_option=chosen_option,
        xp_earned_at_step=xp_earned,
    )

    # ── Determine next step ───────────────────────────────────────────────────
    next_step = _get_next_step(current_step, chosen_option)

    # ── Check for completion ──────────────────────────────────────────────────
    if current_step.is_final_step or next_step is None:
        _complete_session(session, student)
        return {
            'feedback':       feedback,
            'next_step':      None,
            'session_status': 'completed',
            'session_data':   _build_session_stats(session),
        }

    # ── Advance to next step ──────────────────────────────────────────────────
    session.current_step = next_step
    session.save(update_fields=['current_step', 'total_xp_earned',
                                'correct_decisions', 'total_decisions'])

    update_last_active(student)
    return {
        'feedback':       feedback,
        'next_step':      ScenarioStepSimulationSerializer(next_step).data,
        'session_status': 'in_progress',
        'session_data':   _build_session_stats(session),
    }


def get_session_result(session_id: int, student) -> dict:
    """
    Returns the completed session result for the Completion page.

    Raises:
        SimulationSession.DoesNotExist — if session not found or wrong owner
        PermissionError — if session belongs to a different student
    """
    try:
        session = (
            SimulationSession.objects
            .select_related('scenario', 'scenario__category')
            .prefetch_related('decisions__step', 'decisions__chosen_option')
            .get(pk=session_id)
        )
    except SimulationSession.DoesNotExist:
        raise SimulationSession.DoesNotExist(f'Session #{session_id} not found.')

    if session.student_id != student.pk:
        raise PermissionError('This session does not belong to you.')

    return _build_result_payload(session)


# ─── Internal Helpers ──────────────────────────────────────────────────────────

def _get_next_step(current_step: ScenarioStep, chosen_option) -> ScenarioStep | None:
    """
    Determines the next step after a response.

    Priority:
      1. chosen_option.next_step (branching — admin-configured)
      2. Next step by step_number (linear default)
      3. None (simulation ends)
    """
    if chosen_option and chosen_option.next_step_id:
        return chosen_option.next_step

    # Linear progression
    return (
        ScenarioStep.objects
        .filter(
            scenario=current_step.scenario,
            step_number__gt=current_step.step_number,
            is_active=True,
        )
        .order_by('step_number')
        .first()
    )


@transaction.atomic
def _complete_session(session: SimulationSession, student) -> None:
    """
    Marks the session as completed, awards completion bonuses, and checks badges.
    Called when is_final_step is reached or no next step exists.
    """
    session.status       = SimulationSession.Status.COMPLETED
    session.current_step = None
    session.completed_at = timezone.now()
    session.save(update_fields=[
        'status', 'current_step', 'completed_at',
        'total_xp_earned', 'correct_decisions', 'total_decisions',
    ])

    scenario = session.scenario

    # Award scenario completion bonus
    if scenario.xp_completion_bonus > 0:
        bonus = xp_service.award_xp(
            user=student,
            amount=scenario.xp_completion_bonus,
            session=session,
            transaction_type=XPHistory.TransactionType.COMPLETION,
        )
        session.total_xp_earned += bonus

    # Award perfect score bonus if applicable
    if (scenario.xp_perfect_score_bonus > 0
            and session.total_decisions > 0
            and session.correct_decisions == session.total_decisions):
        perfect_bonus = xp_service.award_xp(
            user=student,
            amount=scenario.xp_perfect_score_bonus,
            session=session,
            transaction_type=XPHistory.TransactionType.PERFECT_SCORE,
        )
        session.total_xp_earned += perfect_bonus

    session.save(update_fields=['total_xp_earned'])

    # Evaluate and award any newly earned badges
    badge_service.check_and_award_badges(student)

    update_last_active(student)


def _build_session_stats(session: SimulationSession) -> dict:
    """Returns lightweight session stats for in-progress feedback responses."""
    return {
        'session_id':        session.id,
        'total_xp_earned':   session.total_xp_earned,
        'correct_decisions': session.correct_decisions,
        'total_decisions':   session.total_decisions,
        'accuracy_percent':  session.accuracy_percentage,
    }


def _build_result_payload(session: SimulationSession) -> dict:
    """
    Builds the full result payload for the Completion page.
    Includes: session stats, per-step decision review, newly earned badges.
    """
    from apps.progress.models import UserBadge, Badge
    from apps.scenarios.serializers import DecisionOptionResultSerializer
    from apps.progress.serializers import UserBadgeSerializer

    # Build the decision review (what the student chose vs. correct answer)
    decision_review = []
    for decision in session.decisions.order_by('step__step_number'):
        step = decision.step
        correct_option = step.options.filter(is_correct=True).first()
        review_item = {
            'step_number':      step.step_number,
            'step_title':       step.title,
            'step_type':        step.step_type,
            'nist_phase':       step.nist_phase,
            'nist_phase_label': step.get_nist_phase_display(),
            'chosen_option':    None,
            'correct_option':   None,
            'was_correct':      decision.was_correct,
            'xp_earned':        decision.xp_earned_at_step,
        }
        if decision.chosen_option:
            review_item['chosen_option']  = DecisionOptionResultSerializer(decision.chosen_option).data
        if correct_option and step.step_type != 'info':
            review_item['correct_option'] = DecisionOptionResultSerializer(correct_option).data
        decision_review.append(review_item)

    # Lessons learned from the final step (last info step)
    final_step = session.scenario.steps.filter(is_final_step=True).first()
    lessons_learned_text = final_step.situation_text if final_step else ''

    # Badges earned in this session — any badge earned after session started
    new_badges = UserBadge.objects.filter(
        user=session.student,
        earned_at__gte=session.started_at,
    ).select_related('badge').order_by('earned_at')
    new_badges_data = UserBadgeSerializer(new_badges, many=True).data

    return {
        'session_id':         session.id,
        'scenario_id':        session.scenario_id,
        'scenario_title':     session.scenario.title,
        'scenario_id_code':   session.scenario.scenario_id,
        'category_name':      session.scenario.category.name,
        'difficulty':         session.scenario.difficulty,
        'status':             session.status,
        'total_xp_earned':    session.total_xp_earned,
        'correct_decisions':  session.correct_decisions,
        'total_decisions':    session.total_decisions,
        'accuracy_percent':   session.accuracy_percentage,
        'is_perfect_score':   session.is_perfect_score,
        'duration_minutes':   session.duration_minutes,
        'started_at':         session.started_at,
        'completed_at':       session.completed_at,
        'decision_review':    decision_review,
        'lessons_learned':    lessons_learned_text,
        'new_badges':         new_badges_data,
    }
