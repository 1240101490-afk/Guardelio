"""
Guardelio — Scenarios Models
Agent 2 (Django Model Designer) + Agent 3 (Scenario Data Structure) + Agent 5 (Admin Models)

Models:
    Category          — Groups scenarios by cybersecurity incident type.
    Scenario          — A complete learnable simulation unit.
    LearningObjective — Individual objectives listed on the Scenario Overview.
    ScenarioStep      — A single step (info or decision) within a scenario.
    DecisionOption    — A selectable choice for decision-type steps, with branching.

Design Decisions:
    - Difficulty is a field on Scenario (not a separate table) — it is a property
      of the scenario, not a standalone entity with its own data.
    - LearningObjective is a separate table (not a JSON field) — enables per-objective
      ordering, editing by admin, and clean normalization.
    - DecisionOption.next_step FK enables full branching without code changes.
      NULL next_step means "advance to next step by step_number order" (linear flow).
    - Soft deletes (is_active) on Category, Scenario, and ScenarioStep prevent
      historical student session data from breaking when content is updated.
    - nist_phase on ScenarioStep is stored as a CharField with choices — this
      drives the NISTPhaseBar UI component on the frontend.
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Represents a cybersecurity incident type (e.g., 'Malware Infection Response').

    Categories group scenarios and provide the top-level navigation for students.
    Admins manage categories entirely through the admin portal — no code changes needed.

    Relationship: One Category → Many Scenarios
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Category Name',
        help_text='e.g., Malware Infection Response',
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,               # Auto-generated from name on save
        verbose_name='URL Slug',
        help_text='Auto-generated. Used in frontend URLs.',
    )

    description = models.TextField(
        verbose_name='Category Description',
        help_text='Student-facing description shown on the Category Overview page.',
    )

    # Short summary shown on category cards before the student opens the category
    short_summary = models.CharField(
        max_length=200,
        verbose_name='Short Summary',
        help_text='One-line summary shown on category selection cards.',
    )

    # Icon identifier for the frontend — maps to an icon component/name
    icon_name = models.CharField(
        max_length=50,
        default='shield',
        verbose_name='Icon Name',
        help_text='Icon identifier for the frontend UI component.',
    )

    # Color theme token for the frontend (maps to Tailwind color class)
    color_theme = models.CharField(
        max_length=50,
        default='blue',
        verbose_name='Color Theme',
        help_text='Tailwind color name for this category\'s card styling.',
    )

    # Admin-controlled display order on the category listing page
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Lower number appears first. Controls card order.',
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Is Active',
        help_text='Inactive categories are hidden from students.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table     = 'scenarios_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not set
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def active_scenario_count(self):
        if hasattr(self, '_active_scenario_count'):
            return self._active_scenario_count
        return self.scenarios.filter(is_active=True).count()

    @active_scenario_count.setter
    def active_scenario_count(self, value):
        self._active_scenario_count = value


class Scenario(models.Model):
    """
    A complete cybersecurity incident simulation.

    Every scenario belongs to one Category and has a difficulty level.
    It contains: overview, learning objectives (related model), steps, and XP reward.

    Admins create and manage scenarios entirely through the admin portal.

    Relationship: One Category → Many Scenarios
                  One Scenario → Many LearningObjectives
                  One Scenario → Many ScenarioSteps
                  One Scenario → Many SimulationSessions
    """

    class Difficulty(models.TextChoices):
        BEGINNER     = 'beginner',     'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED     = 'advanced',     'Advanced'

    # Scenario identifier — used in seed data and admin reference
    scenario_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Scenario ID',
        help_text='Unique code e.g. S-MAL-01. Used for internal reference.',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,         # Prevent deleting a category with scenarios
        related_name='scenarios',
        verbose_name='Category',
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Scenario Title',
        help_text='Full title shown on scenario cards and overview.',
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name='URL Slug',
    )

    # Student-facing role description shown on overview page
    # e.g., "You are a Junior Security Analyst at Nexus Financial Services."
    student_role = models.CharField(
        max_length=200,
        verbose_name='Student Role',
        help_text='Describes who the student is playing in this scenario.',
    )

    # Full scenario overview / background context shown before simulation starts
    overview = models.TextField(
        verbose_name='Overview',
        help_text='Scenario context shown on the Scenario Overview page.',
    )

    difficulty = models.CharField(
        max_length=15,
        choices=Difficulty.choices,
        db_index=True,
        verbose_name='Difficulty Level',
    )

    estimated_duration_minutes = models.PositiveIntegerField(
        default=15,
        validators=[MinValueValidator(5), MaxValueValidator(60)],
        verbose_name='Estimated Duration (minutes)',
    )

    # XP awarded on scenario completion (the completion bonus, in addition to per-step XP)
    xp_completion_bonus = models.PositiveIntegerField(
        default=25,
        validators=[MinValueValidator(0)],
        verbose_name='XP Completion Bonus',
        help_text='Awarded when student finishes the scenario.',
    )

    # XP awarded if the student achieves 100% correct decisions
    xp_perfect_score_bonus = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(0)],
        verbose_name='XP Perfect Score Bonus',
        help_text='Additional XP for 100% correct decisions.',
    )

    # Scenario version — incremented when admin makes significant content edits.
    # SimulationSession stores the version snapshot to detect content drift.
    version = models.PositiveIntegerField(
        default=1,
        verbose_name='Content Version',
        help_text='Increment when making significant content changes.',
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Is Active',
        help_text='Inactive scenarios are hidden from students.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table     = 'scenarios_scenario'
        verbose_name = 'Scenario'
        verbose_name_plural = 'Scenarios'
        ordering = ['category', 'difficulty', 'scenario_id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.scenario_id}] {self.title} ({self.get_difficulty_display()})'

    @property
    def total_xp_available(self):
        """Maximum XP a student can earn from this scenario."""
        step_xp = sum(
            opt.xp_awarded
            for step in self.steps.filter(step_type='decision')
            for opt in step.options.filter(is_correct=True)
        )
        return step_xp + self.xp_completion_bonus + self.xp_perfect_score_bonus

    @property
    def total_steps(self):
        return self.steps.filter(is_active=True).count()

    @property
    def decision_step_count(self):
        return self.steps.filter(step_type='decision', is_active=True).count()


class LearningObjective(models.Model):
    """
    A single learning objective for a scenario.

    Stored as individual rows (not a JSON field) to allow:
    - Per-objective admin editing
    - Consistent ordering
    - Clean 3NF normalization

    Relationship: One Scenario → Many LearningObjectives
    """

    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='learning_objectives',
        verbose_name='Scenario',
    )

    # The objective text: "By completing this scenario, you will be able to..."
    objective_text = models.CharField(
        max_length=300,
        verbose_name='Objective Text',
    )

    # Display order on the overview page
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
    )

    class Meta:
        db_table     = 'scenarios_learningobjective'
        verbose_name = 'Learning Objective'
        verbose_name_plural = 'Learning Objectives'
        ordering = ['scenario', 'order']
        # No two objectives can have the same order within a scenario
        unique_together = [['scenario', 'order']]

    def __str__(self):
        return f'{self.scenario.scenario_id} — Objective {self.order}: {self.objective_text[:60]}'


class ScenarioStep(models.Model):
    """
    A single step within a cybersecurity incident simulation.

    Step types:
        info     — Narrative text only. Student clicks "Continue." No decision.
        decision — Student selects from 2–4 options. Feedback shown after selection.
        quiz     — Multiple-choice recall question. Treated identically to decision in engine.

    NIST Phase Tags:
        preparation  — Context-setting, tool inventory (usually Step 1, type=info)
        detection    — Identifying and analysing the threat
        containment  — Stopping active damage
        eradication  — Removing the root cause
        recovery     — Restoring systems safely
        post_incident — Debrief, documentation, lessons learned (usually final step)

    Relationship: One Scenario → Many ScenarioSteps
                  One ScenarioStep → Many DecisionOptions
    """

    class StepType(models.TextChoices):
        INFO     = 'info',     'Informational'
        DECISION = 'decision', 'Decision Point'
        QUIZ     = 'quiz',     'Knowledge Quiz'

    class NISTPhase(models.TextChoices):
        PREPARATION   = 'preparation',   'Preparation'
        DETECTION     = 'detection',     'Detection & Analysis'
        CONTAINMENT   = 'containment',   'Containment'
        ERADICATION   = 'eradication',   'Eradication'
        RECOVERY      = 'recovery',      'Recovery'
        POST_INCIDENT = 'post_incident', 'Post-Incident Activity'

    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name='Parent Scenario',
    )

    # Sequential step number within the scenario (1-indexed)
    step_number = models.PositiveIntegerField(
        verbose_name='Step Number',
        help_text='Order within the scenario. Must be unique per scenario.',
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Step Title',
        help_text='Short heading shown above the situation narrative.',
    )

    # The full incident narrative text presented to the student
    situation_text = models.TextField(
        verbose_name='Situation Text',
        help_text='The scenario narrative shown to the student at this step.',
    )

    nist_phase = models.CharField(
        max_length=20,
        choices=NISTPhase.choices,
        db_index=True,
        verbose_name='NIST Phase',
        help_text='Maps this step to a NIST SP 800-61 phase for the phase indicator UI.',
    )

    step_type = models.CharField(
        max_length=10,
        choices=StepType.choices,
        default=StepType.DECISION,
        verbose_name='Step Type',
    )

    # Marks the final step in the scenario — triggers session completion when reached
    is_final_step = models.BooleanField(
        default=False,
        verbose_name='Is Final Step',
        help_text='Set True on the last step to trigger session completion.',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
    )

    class Meta:
        db_table     = 'scenarios_scenariostep'
        verbose_name = 'Scenario Step'
        verbose_name_plural = 'Scenario Steps'
        ordering = ['scenario', 'step_number']
        # Enforce unique step numbers within a scenario
        unique_together = [['scenario', 'step_number']]

    def __str__(self):
        return (
            f'{self.scenario.scenario_id} — Step {self.step_number}: '
            f'{self.title} [{self.get_step_type_display()}]'
        )

    @property
    def has_decisions(self):
        return self.step_type in ('decision', 'quiz')

    def get_next_step(self):
        """
        Returns the next sequential step by step_number.
        Used as fallback when a DecisionOption.next_step is None.
        """
        return (
            ScenarioStep.objects
            .filter(
                scenario=self.scenario,
                step_number__gt=self.step_number,
                is_active=True,
            )
            .order_by('step_number')
            .first()
        )


class DecisionOption(models.Model):
    """
    A selectable choice presented to the student on a decision or quiz step.

    Every option contains:
    - The text shown to the student (option_text)
    - Whether it is the correct choice (is_correct)
    - XP awarded if selected (0 for incorrect, >0 for correct)
    - Educational feedback explaining WHY it is correct or incorrect (feedback_text)
    - The consequence type (positive/negative/neutral) — drives UI icon
    - Optional next_step FK for branching scenarios

    Branching Logic:
        next_step = NULL  → Advance to the next step by step_number (linear flow)
        next_step = <id>  → Jump directly to that specific step (branching flow)
        This allows admins to create non-linear scenarios without code changes.

    Relationship: One ScenarioStep → Many DecisionOptions
                  One DecisionOption → One ScenarioStep (next_step, nullable)
    """

    class ConsequenceType(models.TextChoices):
        POSITIVE = 'positive', 'Positive (Best Practice)'
        NEGATIVE = 'negative', 'Negative (Harmful Action)'
        NEUTRAL  = 'neutral',  'Neutral (Suboptimal but not harmful)'

    step = models.ForeignKey(
        ScenarioStep,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Parent Step',
    )

    # The text of the choice shown as a button to the student
    option_text = models.CharField(
        max_length=500,
        verbose_name='Option Text',
        help_text='The selectable choice shown to the student.',
    )

    # Exactly one option per step should have is_correct=True
    is_correct = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Is Correct Answer',
    )

    # XP awarded when student selects this option (0 for incorrect answers)
    xp_awarded = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='XP Awarded',
        help_text='Set >0 for correct options only.',
    )

    # Educational explanation shown in the Feedback Modal after selection
    # Must follow the standardized feedback format (see scenario_architecture.md)
    feedback_text = models.TextField(
        verbose_name='Feedback Text',
        help_text='Educational explanation shown to the student after selecting this option.',
    )

    consequence_type = models.CharField(
        max_length=10,
        choices=ConsequenceType.choices,
        default=ConsequenceType.NEUTRAL,
        verbose_name='Consequence Type',
        help_text='Drives the icon and color shown in the Feedback Modal.',
    )

    # Branching: NULL = advance linearly; set FK to jump to a specific step
    next_step = models.ForeignKey(
        ScenarioStep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_options',    # Reverse: which options lead to this step
        verbose_name='Next Step (Branching)',
        help_text='Leave blank for linear progression. Set to jump to a specific step.',
    )

    # Display order of options on the decision panel (prevents consistent ordering bias)
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
    )

    class Meta:
        db_table     = 'scenarios_decisionoption'
        verbose_name = 'Decision Option'
        verbose_name_plural = 'Decision Options'
        ordering = ['step', 'display_order']

    def __str__(self):
        correct_label = '✓' if self.is_correct else '✗'
        return (
            f'{correct_label} [{self.step.scenario.scenario_id} '
            f'Step {self.step.step_number}] {self.option_text[:60]}'
        )
