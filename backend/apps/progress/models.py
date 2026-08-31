"""
Guardelio — Progress Models
Agent 4 (User Progress Models) + Agent 2 (Django Model Designer)

Models:
    Badge             — Defines an achievable badge with its earning criteria.
    UserBadge         — Records which badges a user has earned (junction table).
    SimulationSession — Tracks one student's attempt at one scenario.
                        Persists state across page refreshes and browser closes.
    SessionDecision   — Immutable audit log of every decision made in a session.
    XPHistory         — Immutable record of every XP transaction for a user.

Design Decisions:
    - SimulationSession.current_step FK enables seamless resume on page reload.
    - SessionDecision is write-once (never updated) — it is the forensic record
      used by the results page, reports, and badge criteria evaluation.
    - XPHistory creates a full audit trail of XP changes — supports future
      features like XP breakdown views without altering User.total_xp logic.
    - Badge criteria stored dynamically — new badge types don't require code changes,
      only a new Badge row inserted via the admin portal.
    - unique_together on (student, scenario) with status='in_progress' is enforced
      at the service layer (not DB level) to allow re-attempts after completion.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from apps.scenarios.models import Scenario, ScenarioStep, DecisionOption


# ─── Badge Models ─────────────────────────────────────────────────────────────

class Badge(models.Model):
    """
    Defines an achievable badge and its earning criteria.

    All badge criteria are stored dynamically in the database.
    New badges can be added via the admin portal without code changes.

    Criteria Types:
        xp_threshold      — Earn a total of criteria_value XP
        completion_count  — Complete criteria_value scenarios
        perfect_score     — Score 100% on criteria_value scenarios
        category_complete — Complete all scenarios in a specific category
        all_categories    — Complete all scenarios across all categories

    Badge Tiers: Bronze → Silver → Gold (cosmetic only — no functional difference)

    Relationship: One Badge → Many UserBadges
    """

    class BadgeType(models.TextChoices):
        BRONZE = 'bronze', 'Bronze'
        SILVER = 'silver', 'Silver'
        GOLD   = 'gold',   'Gold'

    class CriteriaType(models.TextChoices):
        XP_THRESHOLD      = 'xp_threshold',      'XP Threshold'
        COMPLETION_COUNT  = 'completion_count',   'Scenario Completion Count'
        PERFECT_SCORE     = 'perfect_score',      'Perfect Score Count'
        CATEGORY_COMPLETE = 'category_complete',  'Category Fully Completed'
        ALL_CATEGORIES    = 'all_categories',     'All Categories Completed'

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Badge Name',
    )

    description = models.TextField(
        verbose_name='Description',
        help_text='Student-facing explanation of what this badge represents.',
    )

    badge_type = models.CharField(
        max_length=10,
        choices=BadgeType.choices,
        db_index=True,
        verbose_name='Badge Tier',
    )

    criteria_type = models.CharField(
        max_length=25,
        choices=CriteriaType.choices,
        verbose_name='Criteria Type',
        help_text='The condition that must be met to earn this badge.',
    )

    # Numeric threshold for xp_threshold, completion_count, perfect_score
    # For category_complete, store category ID as string in criteria_category
    criteria_value = models.PositiveIntegerField(
        default=1,
        verbose_name='Criteria Value',
        help_text='The required number (XP threshold, count, etc.).',
    )

    # For category_complete criteria — references the category by ID
    criteria_category = models.ForeignKey(
        'scenarios.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_badges',
        verbose_name='Required Category',
        help_text='Set only for category_complete criteria type.',
    )

    icon_name = models.CharField(
        max_length=50,
        default='badge',
        verbose_name='Icon Name',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table     = 'progress_badge'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['badge_type', 'name']

    def __str__(self):
        return f'{self.get_badge_type_display()} Badge: {self.name}'


class UserBadge(models.Model):
    """
    Records a badge award — which user earned which badge and when.

    Junction table enforcing the many-to-many relationship between
    User and Badge. The unique_together constraint ensures a user
    can only earn each badge once.

    Relationship: One User → Many UserBadges
                  One Badge → Many UserBadges
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='earned_badges',
        verbose_name='User',
    )

    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='award_records',
        verbose_name='Badge Earned',
    )

    earned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Earned At',
    )

    class Meta:
        db_table       = 'progress_userbadge'
        verbose_name   = 'User Badge Award'
        verbose_name_plural = 'User Badge Awards'
        # Each badge can only be awarded once per user
        unique_together = [['user', 'badge']]
        ordering = ['-earned_at']

    def __str__(self):
        return f'{self.user.username} earned "{self.badge.name}" on {self.earned_at.date()}'


# ─── Simulation Session Models ────────────────────────────────────────────────

class SimulationSession(models.Model):
    """
    Tracks one student's complete attempt at one scenario.

    This is the central model of the progress system. It:
    - Persists the student's position (current_step) so they can resume after closing the browser
    - Accumulates XP during the session (total_xp_earned)
    - Records correct/total decision counts for accuracy calculation
    - Stores a snapshot of scenario_version to detect content drift

    Status lifecycle:
        in_progress → completed (normal completion)
        in_progress → abandoned (student gives up / admin marks abandoned)

    Relationship: One User → Many SimulationSessions
                  One Scenario → Many SimulationSessions
                  One SimulationSession → Many SessionDecisions
    """

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED   = 'completed',   'Completed'
        ABANDONED   = 'abandoned',   'Abandoned'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='simulation_sessions',
        verbose_name='Student',
    )

    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.PROTECT,          # Never delete a scenario with sessions
        related_name='simulation_sessions',
        verbose_name='Scenario',
    )

    # Snapshot of the scenario version at session start.
    # If the admin increments scenario.version while a session is in progress,
    # the session records the version it was started on for accurate reporting.
    scenario_version = models.PositiveIntegerField(
        verbose_name='Scenario Version (Snapshot)',
        help_text='Version of the scenario when this session was started.',
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
        db_index=True,
        verbose_name='Session Status',
    )

    # Points to the step the student is currently on — enables resume functionality
    # NULL when the session is completed (no active step)
    current_step = models.ForeignKey(
        ScenarioStep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_sessions',
        verbose_name='Current Step',
        help_text='The step the student is currently on. Null when completed.',
    )

    # Running total of XP earned in this session (updated after every step)
    total_xp_earned = models.PositiveIntegerField(
        default=0,
        verbose_name='Total XP Earned This Session',
    )

    # Decision tracking for accuracy calculation
    correct_decisions = models.PositiveIntegerField(
        default=0,
        verbose_name='Correct Decisions',
    )

    total_decisions = models.PositiveIntegerField(
        default=0,
        verbose_name='Total Decision Steps Encountered',
    )

    started_at  = models.DateTimeField(auto_now_add=True, verbose_name='Started At')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Completed At',
        help_text='Set when status changes to completed or abandoned.',
    )

    class Meta:
        db_table     = 'progress_simulationsession'
        verbose_name = 'Simulation Session'
        verbose_name_plural = 'Simulation Sessions'
        ordering = ['-started_at']
        indexes = [
            # Fast lookup of active session for a student on a specific scenario
            models.Index(fields=['student', 'scenario', 'status'], name='idx_session_stu_scen_status'),
        ]

    def __str__(self):
        return (
            f'{self.student.username} → {self.scenario.scenario_id} '
            f'[{self.get_status_display()}]'
        )

    @property
    def accuracy_percentage(self):
        """Returns accuracy as a rounded integer percentage (0–100)."""
        if self.total_decisions == 0:
            return 0
        return round((self.correct_decisions / self.total_decisions) * 100)

    @property
    def is_perfect_score(self):
        """True if the student answered every decision correctly."""
        return (
            self.status == self.Status.COMPLETED
            and self.total_decisions > 0
            and self.correct_decisions == self.total_decisions
        )

    @property
    def duration_minutes(self):
        """Returns session duration in minutes, or None if not completed."""
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            return round(delta.total_seconds() / 60, 1)
        return None


class SessionDecision(models.Model):
    """
    Immutable audit record of every student response during a simulation.

    One record is created for EVERY step the student encounters:
    - For info steps: chosen_option is None (no decision required)
    - For decision/quiz steps: chosen_option references the selected DecisionOption

    This model is WRITE-ONCE — records are never modified after creation.
    It provides the source of truth for:
    - The Results/Completion page (showing what the student chose)
    - Admin reports (decision analysis, commonly-missed questions)
    - Historical session review

    Relationship: One SimulationSession → Many SessionDecisions
                  One SessionDecision → One ScenarioStep
                  One SessionDecision → One DecisionOption (nullable)
    """

    session = models.ForeignKey(
        SimulationSession,
        on_delete=models.CASCADE,
        related_name='decisions',
        verbose_name='Simulation Session',
    )

    step = models.ForeignKey(
        ScenarioStep,
        on_delete=models.PROTECT,
        related_name='student_responses',
        verbose_name='Scenario Step',
    )

    # None for info steps where no selection is made
    chosen_option = models.ForeignKey(
        DecisionOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selection_records',
        verbose_name='Option Selected',
    )

    # Denormalized snapshot of XP awarded at the time of decision
    # Prevents XP inconsistency if an admin later changes option XP values
    xp_earned_at_step = models.PositiveIntegerField(
        default=0,
        verbose_name='XP Earned at This Step',
    )

    responded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Responded At',
    )

    class Meta:
        db_table     = 'progress_sessiondecision'
        verbose_name = 'Session Decision'
        verbose_name_plural = 'Session Decisions'
        ordering = ['session', 'step__step_number']
        # A session should only have one response per step
        unique_together = [['session', 'step']]

    def __str__(self):
        option_label = self.chosen_option.option_text[:40] if self.chosen_option else 'No choice (info step)'
        return f'Session {self.session_id} | Step {self.step.step_number} | "{option_label}"'

    @property
    def was_correct(self):
        """Returns True if the chosen option was the correct one."""
        if self.chosen_option is None:
            return None     # Info steps have no correct/incorrect
        return self.chosen_option.is_correct


# ─── XP History Model ─────────────────────────────────────────────────────────

class XPHistory(models.Model):
    """
    Immutable record of every XP transaction for a user.

    Created alongside every User.total_xp increment — provides a full
    audit trail of how a student earned their XP.

    Transaction types:
        step_correct    — XP from a correct decision on a step
        completion      — Scenario completion bonus
        perfect_score   — Perfect score bonus

    This model is WRITE-ONCE. XP is never subtracted.

    Relationship: One User → Many XPHistory records
    """

    class TransactionType(models.TextChoices):
        STEP_CORRECT  = 'step_correct',  'Correct Decision'
        COMPLETION    = 'completion',    'Scenario Completion Bonus'
        PERFECT_SCORE = 'perfect_score', 'Perfect Score Bonus'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='xp_history',
        verbose_name='User',
    )

    # Link to the session that generated this XP (for full traceability)
    session = models.ForeignKey(
        SimulationSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='xp_transactions',
        verbose_name='Related Session',
    )

    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='XP Amount',
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name='Transaction Type',
    )

    # Running total at the time of this transaction — useful for XP timeline charts
    balance_after = models.PositiveIntegerField(
        verbose_name='XP Balance After Transaction',
    )

    description = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Description',
        help_text='Human-readable note about this XP award.',
    )

    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='Earned At')

    class Meta:
        db_table     = 'progress_xphistory'
        verbose_name = 'XP History Record'
        verbose_name_plural = 'XP History Records'
        ordering = ['-earned_at']

    def __str__(self):
        return f'{self.user.username} +{self.amount} XP [{self.get_transaction_type_display()}] → {self.balance_after} XP'
