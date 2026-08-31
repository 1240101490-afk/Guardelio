"""
Guardelio — Admin Reports Serializers
Write serializers for admin CRUD + read-only reporting serializers.
"""

from rest_framework import serializers

from apps.scenarios.models import (
    Category, Scenario, LearningObjective, ScenarioStep, DecisionOption
)
from apps.accounts.models import User
from apps.progress.models import SimulationSession


# ─── Write Serializers (for admin CRUD) ───────────────────────────────────────

class AdminCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = (
            'id', 'name', 'short_summary', 'description',
            'icon_name', 'color_theme', 'display_order', 'is_active',
        )
        read_only_fields = ('id',)

    def validate_name(self, value):
        qs = Category.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A category with this name already exists.')
        return value


class AdminLearningObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LearningObjective
        fields = ('id', 'scenario', 'order', 'objective_text')
        read_only_fields = ('id',)


class AdminScenarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Scenario
        fields = (
            'id', 'scenario_id', 'category', 'title', 'student_role', 'overview',
            'difficulty', 'estimated_duration_minutes',
            'xp_completion_bonus', 'xp_perfect_score_bonus',
            'version', 'is_active',
        )
        read_only_fields = ('id',)

    def validate_scenario_id(self, value):
        qs = Scenario.objects.filter(scenario_id__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f'Scenario ID "{value}" is already in use.')
        return value.upper()


class AdminStepWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ScenarioStep
        fields = (
            'id', 'scenario', 'step_number', 'title', 'situation_text',
            'nist_phase', 'step_type', 'is_final_step', 'is_active',
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        scenario    = attrs.get('scenario', getattr(self.instance, 'scenario', None))
        step_number = attrs.get('step_number', getattr(self.instance, 'step_number', None))
        if scenario and step_number is not None:
            qs = ScenarioStep.objects.filter(scenario=scenario, step_number=step_number)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'step_number': f'Step number {step_number} already exists in this scenario.'}
                )
        return attrs


class AdminOptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DecisionOption
        fields = (
            'id', 'step', 'option_text', 'is_correct', 'xp_awarded',
            'feedback_text', 'consequence_type', 'next_step', 'display_order',
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        # XP should only be > 0 for correct options
        if attrs.get('xp_awarded', 0) > 0 and not attrs.get('is_correct', False):
            raise serializers.ValidationError(
                {'xp_awarded': 'XP can only be awarded for correct options (is_correct=True).'}
            )
        return attrs


# ─── Admin User Management Serializers ────────────────────────────────────────

class AdminUserListSerializer(serializers.ModelSerializer):
    full_name    = serializers.CharField(read_only=True)
    role_label   = serializers.CharField(source='get_role_display', read_only=True)
    session_count = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = (
            'id', 'username', 'email', 'full_name', 'role', 'role_label',
            'total_xp', 'is_active', 'date_joined', 'last_login', 'session_count',
        )

    def get_session_count(self, obj):
        return SimulationSession.objects.filter(student=obj).count()


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Admin can only toggle is_active and change role. Cannot change password via this endpoint."""
    class Meta:
        model  = User
        fields = ('is_active', 'role')


# ─── Reporting Serializers ─────────────────────────────────────────────────────

class ScenarioAnalyticsSerializer(serializers.Serializer):
    """Per-scenario analytics for the admin reports page."""
    scenario_id    = serializers.CharField()
    scenario_title = serializers.CharField()
    category_name  = serializers.CharField()
    difficulty     = serializers.CharField()
    total_attempts = serializers.IntegerField()
    completions    = serializers.IntegerField()
    abandonment_rate = serializers.FloatField()
    average_accuracy  = serializers.FloatField()
    average_xp        = serializers.FloatField()


class AdminDashboardStatsSerializer(serializers.Serializer):
    total_users         = serializers.IntegerField()
    active_students     = serializers.IntegerField()
    total_categories    = serializers.IntegerField()
    total_scenarios     = serializers.IntegerField()
    total_sessions      = serializers.IntegerField()
    completed_sessions  = serializers.IntegerField()
    average_accuracy    = serializers.FloatField()
    top_scenario_title  = serializers.CharField(allow_null=True)
