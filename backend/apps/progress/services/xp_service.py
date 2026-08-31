"""
Guardelio — XP Service
Handles all XP award operations atomically.
Called by SimulationService — never called directly from views.

All XP writes use F() expressions to prevent race conditions on
concurrent requests (extremely unlikely in a FYP but correct practice).
"""

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.progress.models import XPHistory, SimulationSession


@transaction.atomic
def award_xp(user, amount: int, session: SimulationSession,
             transaction_type: str, description: str = '') -> int:
    """
    Awards XP to a user atomically.

    Steps:
      1. Increment user.total_xp using F() (atomic, prevents race conditions)
      2. Refresh from DB to get the new balance
      3. Create an XPHistory record for the full audit trail
      4. Return the XP amount awarded

    Args:
        user            — The User instance to award XP to
        amount          — Positive integer XP to add
        session         — The SimulationSession that generated this XP
        transaction_type — XPHistory.TransactionType value
        description     — Human-readable note for the history record

    Returns:
        int — The amount of XP awarded (same as input, for convenience)
    """
    if amount <= 0:
        return 0

    # Atomic increment — safe under concurrent requests
    user.__class__.objects.filter(pk=user.pk).update(total_xp=F('total_xp') + amount)

    # Refresh to get the new balance for the history record
    user.refresh_from_db(fields=['total_xp'])

    XPHistory.objects.create(
        user=user,
        session=session,
        amount=amount,
        transaction_type=transaction_type,
        balance_after=user.total_xp,
        description=description or _build_description(transaction_type, session),
    )

    return amount


def _build_description(transaction_type: str, session: SimulationSession) -> str:
    """Generates a human-readable description for an XP history entry."""
    scenario_title = session.scenario.title if session and session.scenario else 'Unknown scenario'
    descriptions = {
        XPHistory.TransactionType.STEP_CORRECT:  f'Correct decision in "{scenario_title}"',
        XPHistory.TransactionType.COMPLETION:    f'Completed "{scenario_title}"',
        XPHistory.TransactionType.PERFECT_SCORE: f'Perfect score in "{scenario_title}"',
    }
    return descriptions.get(transaction_type, f'XP earned in "{scenario_title}"')
