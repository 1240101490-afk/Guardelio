"""
Guardelio — Badge Service
Evaluates badge criteria and awards newly-earned badges.

Called once after every session completion.
Designed to be idempotent — re-running never duplicates badges.

Badge criteria types (from progress_badge.criteria_type):
  xp_threshold      — User.total_xp >= criteria_value
  completion_count  — COUNT(completed sessions) >= criteria_value
  perfect_score     — COUNT(sessions with is_perfect_score logic) >= criteria_value
  category_complete — All scenarios in criteria_category are completed
  all_categories    — All scenarios across all active categories are completed
"""

from django.db import transaction

from apps.progress.models import Badge, UserBadge, SimulationSession


@transaction.atomic
def check_and_award_badges(user) -> list:
    """
    Evaluates all active badge criteria for a user and awards any newly earned badges.

    Returns:
        list[Badge] — List of newly awarded badges (empty if none earned).
    """
    # IDs of badges the user already holds — skip these in evaluation
    already_earned_ids = set(
        UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    )

    active_badges = Badge.objects.filter(is_active=True).exclude(id__in=already_earned_ids)

    if not active_badges.exists():
        return []

    # Gather user stats once (avoid repeated DB hits inside the loop)
    stats = _gather_user_stats(user)

    newly_awarded = []
    for badge in active_badges:
        if _criteria_met(badge, user, stats):
            UserBadge.objects.create(user=user, badge=badge)
            newly_awarded.append(badge)

    return newly_awarded


def _gather_user_stats(user) -> dict:
    """Collects all stats needed for badge evaluation in one pass."""
    completed_sessions = SimulationSession.objects.filter(
        student=user, status=SimulationSession.Status.COMPLETED
    ).select_related('scenario__category')

    # Completed scenario IDs (distinct — re-completions count as 1)
    completed_scenario_ids = set(
        completed_sessions.values_list('scenario_id', flat=True)
    )

    # Perfect score sessions (all decisions correct, at least one decision step)
    perfect_sessions = [
        s for s in completed_sessions
        if s.total_decisions > 0 and s.correct_decisions == s.total_decisions
    ]
    # Distinct scenarios with perfect score
    perfect_scenario_ids = set(s.scenario_id for s in perfect_sessions)

    # Completed category IDs (categories where all active scenarios are completed)
    from apps.scenarios.models import Category, Scenario
    completed_category_ids = set()
    for category in Category.objects.filter(is_active=True):
        active_scenario_ids = set(
            Scenario.objects.filter(category=category, is_active=True)
            .values_list('id', flat=True)
        )
        if active_scenario_ids and active_scenario_ids.issubset(completed_scenario_ids):
            completed_category_ids.add(category.id)

    return {
        'total_xp':              user.total_xp,
        'completion_count':      len(completed_scenario_ids),
        'perfect_score_count':   len(perfect_scenario_ids),
        'completed_category_ids': completed_category_ids,
        'total_active_categories': Category.objects.filter(is_active=True).count(),
    }


def _criteria_met(badge: Badge, user, stats: dict) -> bool:
    """Returns True if the user meets the badge's earning criteria."""
    ct = badge.criteria_type
    cv = badge.criteria_value

    if ct == Badge.CriteriaType.XP_THRESHOLD:
        return stats['total_xp'] >= cv

    elif ct == Badge.CriteriaType.COMPLETION_COUNT:
        return stats['completion_count'] >= cv

    elif ct == Badge.CriteriaType.PERFECT_SCORE:
        return stats['perfect_score_count'] >= cv

    elif ct == Badge.CriteriaType.CATEGORY_COMPLETE:
        if badge.criteria_category_id:
            return badge.criteria_category_id in stats['completed_category_ids']
        return False

    elif ct == Badge.CriteriaType.ALL_CATEGORIES:
        # All active categories completed
        return (
            stats['total_active_categories'] > 0
            and len(stats['completed_category_ids']) >= stats['total_active_categories']
        )

    return False
