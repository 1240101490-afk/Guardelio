"""
Guardelio — Progress & Simulation Views
Agent 3 (Simulation Engine) + Agent 4 (Progress Tracking)

Simulation endpoints (prefix: /api/v1/simulation/):
  POST   start/                    → Start or resume a simulation
  GET    <session_id>/             → Get current session state (for page refresh resume)
  POST   <session_id>/respond/     → Submit a step response
  GET    <session_id>/result/      → Get completed session results

Progress endpoints (prefix: /api/v1/):
  GET    progress/dashboard/       → Student dashboard summary
  GET    progress/sessions/        → Full session history (paginated)
  GET    progress/badges/          → Earned badges
  GET    progress/xp-history/      → XP transaction history
  GET    progress/stats/           → Learning statistics

All views are restricted to IsStudent role.
"""

from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework import status

from core.utils import (
    success_response, created_response, error_response,
    not_found_response, forbidden_response,
)
from core.permissions import IsStudent
from apps.scenarios.models import Category, Scenario

from .models import SimulationSession, UserBadge, XPHistory, Badge
from .serializers import (
    SessionListSerializer,
    InProgressSessionSerializer,
    UserBadgeSerializer,
    XPHistorySerializer,
    BadgeSerializer,
)
from .services import simulation_service
from apps.scenarios.serializers import ScenarioStepSimulationSerializer


# ─── Simulation Views ──────────────────────────────────────────────────────────

class StartSimulationView(APIView):
    """
    POST /api/v1/simulation/start/
    Starts a new simulation or resumes an in-progress session.

    Request body: { "scenario_id": <int> }

    Response:
      {
        "is_new": bool,                  — True if new session, False if resumed
        "session_id": int,
        "scenario_title": str,
        "current_step": { step data }    — First/current step with options
      }
    """
    permission_classes = [IsStudent]

    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        if not scenario_id:
            return error_response(message='scenario_id is required.')

        try:
            session, is_new = simulation_service.start_simulation(
                student=request.user,
                scenario_id=int(scenario_id),
            )
        except Scenario.DoesNotExist:
            return not_found_response(f'Scenario #{scenario_id} not found or is not available.')
        except ValueError as e:
            return error_response(message=str(e))
        except Exception as e:
            return error_response(
                message='Failed to start simulation. Please try again.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        step_data = (
            ScenarioStepSimulationSerializer(session.current_step).data
            if session.current_step else None
        )

        return success_response(
            data={
                'is_new':         is_new,
                'session_id':     session.id,
                'scenario_id':    session.scenario_id,
                'scenario_title': session.scenario.title,
                'scenario_version': session.scenario_version,
                'session_stats':  {
                    'total_xp_earned':   session.total_xp_earned,
                    'correct_decisions': session.correct_decisions,
                    'total_decisions':   session.total_decisions,
                    'accuracy_percent':  session.accuracy_percentage,
                },
                'current_step': step_data,
            },
            message='Simulation resumed.' if not is_new else 'Simulation started.',
        )


class SessionStateView(APIView):
    """
    GET /api/v1/simulation/<int:session_id>/
    Returns current session state — used to restore simulation on page refresh.
    """
    permission_classes = [IsStudent]

    def get(self, request, session_id):
        try:
            session = (
                SimulationSession.objects
                .select_related('scenario__category', 'current_step')
                .get(pk=session_id, student=request.user)
            )
        except SimulationSession.DoesNotExist:
            return not_found_response(f'Session #{session_id} not found.')

        if session.status == SimulationSession.Status.COMPLETED:
            return success_response(
                data={'session_id': session.id, 'status': 'completed'},
                message='This simulation is already completed. Use the /result/ endpoint.',
            )

        step_data = (
            ScenarioStepSimulationSerializer(session.current_step).data
            if session.current_step else None
        )

        return success_response(
            data={
                'session_id':     session.id,
                'scenario_id':    session.scenario_id,
                'scenario_title': session.scenario.title,
                'status':         session.status,
                'session_stats': {
                    'total_xp_earned':   session.total_xp_earned,
                    'correct_decisions': session.correct_decisions,
                    'total_decisions':   session.total_decisions,
                    'accuracy_percent':  session.accuracy_percentage,
                },
                'current_step': step_data,
            },
            message='Session state retrieved.',
        )


class RespondToStepView(APIView):
    """
    POST /api/v1/simulation/<int:session_id>/respond/

    Processes the student's response to the current step.

    For INFO steps:        request body can be empty {}
    For DECISION/QUIZ:     { "option_id": <int> }

    Response:
      {
        "feedback": {is_correct, feedback_text, xp_earned, consequence_type}
                     (null for info steps)
        "next_step": { step data } | null (null when session is completed)
        "session_status": "in_progress" | "completed"
        "session_data":  { stats }
      }
    """
    permission_classes = [IsStudent]

    def post(self, request, session_id):
        try:
            session = (
                SimulationSession.objects
                .select_related('scenario', 'current_step')
                .get(pk=session_id, student=request.user)
            )
        except SimulationSession.DoesNotExist:
            return not_found_response(f'Session #{session_id} not found.')

        option_id = request.data.get('option_id', None)
        if option_id is not None:
            try:
                option_id = int(option_id)
            except (TypeError, ValueError):
                return error_response(message='option_id must be a valid integer.')

        try:
            result = simulation_service.process_step_response(
                session=session,
                student=request.user,
                option_id=option_id,
            )
        except PermissionError as e:
            return forbidden_response(str(e))
        except ValueError as e:
            return error_response(message=str(e))
        except Exception as e:
            return error_response(
                message='Failed to process your response. Please try again.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return success_response(data=result, message='Response recorded.')


class SessionResultView(APIView):
    """
    GET /api/v1/simulation/<int:session_id>/result/
    Returns the full completion results for the Results page.
    """
    permission_classes = [IsStudent]

    def get(self, request, session_id):
        try:
            result = simulation_service.get_session_result(
                session_id=session_id,
                student=request.user,
            )
        except SimulationSession.DoesNotExist:
            return not_found_response(f'Session #{session_id} not found.')
        except PermissionError as e:
            return forbidden_response(str(e))

        return success_response(data=result, message='Session result retrieved.')


# ─── Progress Tracking Views ───────────────────────────────────────────────────

class DashboardView(APIView):
    """
    GET /api/v1/progress/dashboard/
    Returns the student's complete dashboard summary in a single request.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user

        all_sessions = (
            SimulationSession.objects
            .filter(student=user)
            .select_related('scenario__category')
        )

        completed_sessions  = all_sessions.filter(status=SimulationSession.Status.COMPLETED)
        in_progress_sessions = all_sessions.filter(status=SimulationSession.Status.IN_PROGRESS)

        # Accuracy average (only from completed sessions with decisions)
        avg_accuracy = 0.0
        accuracy_sessions = [
            s for s in completed_sessions if s.total_decisions > 0
        ]
        if accuracy_sessions:
            avg_accuracy = round(
                sum(s.accuracy_percentage for s in accuracy_sessions) / len(accuracy_sessions),
                1,
            )

        # Categories stats
        started_cat_ids = set(
            all_sessions.values_list('scenario__category_id', flat=True)
        )
        completed_scenario_ids = set(
            completed_sessions.values_list('scenario_id', flat=True)
        )
        completed_cat_ids = set()
        for cat in Category.objects.filter(is_active=True):
            active_ids = set(
                Scenario.objects.filter(category=cat, is_active=True).values_list('id', flat=True)
            )
            if active_ids and active_ids.issubset(completed_scenario_ids):
                completed_cat_ids.add(cat.id)

        recent_sessions  = SessionListSerializer(
            completed_sessions.order_by('-completed_at')[:5], many=True
        ).data
        in_progress_data = SessionListSerializer(
            in_progress_sessions.order_by('-started_at'), many=True
        ).data
        recent_badges = UserBadgeSerializer(
            UserBadge.objects.filter(user=user).select_related('badge').order_by('-earned_at')[:5],
            many=True,
        ).data

        return success_response(
            data={
                'total_xp':             user.total_xp,
                'completed_count':      completed_sessions.count(),
                'in_progress_count':    in_progress_sessions.count(),
                'badge_count':          UserBadge.objects.filter(user=user).count(),
                'average_accuracy':     avg_accuracy,
                'categories_started':   len(started_cat_ids),
                'categories_completed': len(completed_cat_ids),
                'recent_sessions':      recent_sessions,
                'recent_badges':        recent_badges,
                'in_progress_sessions': in_progress_data,
            },
            message='Dashboard data retrieved.',
        )


class SessionHistoryView(APIView):
    """
    GET /api/v1/progress/sessions/
    Returns paginated session history with optional filter: ?status=completed|in_progress|abandoned
    """
    permission_classes = [IsStudent]

    def get(self, request):
        status_filter = request.query_params.get('status')
        sessions = (
            SimulationSession.objects
            .filter(student=request.user)
            .select_related('scenario__category')
            .order_by('-started_at')
        )
        if status_filter:
            sessions = sessions.filter(status=status_filter)

        serializer = SessionListSerializer(sessions, many=True)
        return success_response(
            data=serializer.data,
            message=f'{sessions.count()} sessions retrieved.',
        )


class BadgeListView(APIView):
    """
    GET /api/v1/progress/badges/
    Returns all badges earned by the authenticated student.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user_badges = (
            UserBadge.objects
            .filter(user=request.user)
            .select_related('badge')
            .order_by('-earned_at')
        )
        serializer = UserBadgeSerializer(user_badges, many=True)
        return success_response(
            data=serializer.data,
            message=f'{user_badges.count()} badges earned.',
        )


class XPHistoryView(APIView):
    """
    GET /api/v1/progress/xp-history/
    Returns the student's full XP transaction history.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        history = (
            XPHistory.objects
            .filter(user=request.user)
            .select_related('session__scenario')
            .order_by('-earned_at')[:50]   # Last 50 entries
        )
        serializer = XPHistorySerializer(history, many=True)
        return success_response(
            data=serializer.data,
            message='XP history retrieved.',
        )


class LearningStatsView(APIView):
    """
    GET /api/v1/progress/stats/
    Returns per-category and per-NIST-phase statistics for the Progress page.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user

        completed_sessions = (
            SimulationSession.objects
            .filter(student=user, status=SimulationSession.Status.COMPLETED)
            .select_related('scenario__category')
        )

        # ── Per-category breakdown ────────────────────────────────────────────
        category_stats = []
        for cat in Category.objects.filter(is_active=True).order_by('display_order'):
            cat_sessions = [s for s in completed_sessions if s.scenario.category_id == cat.id]
            total_in_cat = Scenario.objects.filter(category=cat, is_active=True).count()

            avg_acc = 0.0
            acc_sessions = [s for s in cat_sessions if s.total_decisions > 0]
            if acc_sessions:
                avg_acc = round(
                    sum(s.accuracy_percentage for s in acc_sessions) / len(acc_sessions), 1
                )

            category_stats.append({
                'category_id':         cat.id,
                'category_name':       cat.name,
                'category_slug':       cat.slug,
                'icon_name':           cat.icon_name,
                'color_theme':         cat.color_theme,
                'completed_scenarios': len(set(s.scenario_id for s in cat_sessions)),
                'total_scenarios':     total_in_cat,
                'average_accuracy':    avg_acc,
            })

        # ── NIST phase performance (average accuracy per phase) ───────────────
        from apps.progress.models import SessionDecision
        from apps.scenarios.models import ScenarioStep
        nist_phase_stats = {}
        for decision in SessionDecision.objects.filter(
            session__student=user,
            session__status=SimulationSession.Status.COMPLETED,
            chosen_option__isnull=False,
        ).select_related('step', 'chosen_option'):
            phase = decision.step.nist_phase
            if phase not in nist_phase_stats:
                nist_phase_stats[phase] = {'correct': 0, 'total': 0, 'label': decision.step.get_nist_phase_display()}
            nist_phase_stats[phase]['total'] += 1
            if decision.chosen_option.is_correct:
                nist_phase_stats[phase]['correct'] += 1

        nist_breakdown = [
            {
                'phase': phase,
                'label': data['label'],
                'accuracy_percent': round((data['correct'] / data['total']) * 100)
                                    if data['total'] > 0 else 0,
                'total_decisions':  data['total'],
                'correct_decisions': data['correct'],
            }
            for phase, data in nist_phase_stats.items()
        ]

        return success_response(
            data={
                'category_breakdown': category_stats,
                'nist_phase_breakdown': nist_breakdown,
                'total_xp':   user.total_xp,
                'total_completed': completed_sessions.count(),
            },
            message='Learning statistics retrieved.',
        )


class AllBadgeCatalogView(APIView):
    """
    GET /api/v1/progress/all-badges/
    Returns the complete badge catalog (all 18 badges) with an is_earned flag
    for the authenticated student.

    Use case: Progress page badge grid — earned badges show full color,
    unearned badges show greyed out with criteria text on hover.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user

        # IDs of badges the student has already earned
        earned_badge_ids = set(
            UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
        )
        # Map badge_id → earned_at for earned badges
        earned_map = {
            ub.badge_id: ub.earned_at
            for ub in UserBadge.objects.filter(user=user).select_related('badge')
        }

        badges = Badge.objects.filter(is_active=True).order_by('badge_type', 'name')

        result = []
        for badge in badges:
            data = BadgeSerializer(badge).data
            data['is_earned']  = badge.id in earned_badge_ids
            data['earned_at']  = earned_map.get(badge.id)
            result.append(data)

        total_earned = len(earned_badge_ids)
        total_badges = badges.count()

        return success_response(
            data={
                'badges':       result,
                'total_earned': total_earned,
                'total_badges': total_badges,
            },
            message=f'{total_earned} of {total_badges} badges earned.',
        )
