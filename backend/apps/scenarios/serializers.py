"""
Guardelio — Scenarios Serializers
Output shapes for Category, Scenario, Step, and Option data.

Two serializer depths are used:
  List serializers  — lightweight, for category/scenario cards
  Detail serializers — full nested data, for overview and simulation pages
"""

from rest_framework import serializers
from .models import Category, Scenario, LearningObjective, ScenarioStep, DecisionOption


# ─── Decision Option ───────────────────────────────────────────────────────────

class DecisionOptionSimulationSerializer(serializers.ModelSerializer):
    """
    Used during an active simulation — shows options WITHOUT revealing which is correct.
    The frontend never receives is_correct or feedback_text before a selection is made.
    """
    class Meta:
        model  = DecisionOption
        fields = ('id', 'option_text', 'display_order')


class DecisionOptionResultSerializer(serializers.ModelSerializer):
    """
    Used on the Completion/Results page — shows full option data including correctness.
    """
    class Meta:
        model  = DecisionOption
        fields = ('id', 'option_text', 'is_correct', 'xp_awarded',
                  'feedback_text', 'consequence_type', 'display_order')


class DecisionOptionAdminSerializer(serializers.ModelSerializer):
    """Full option data for admin CRUD operations."""
    class Meta:
        model  = DecisionOption
        fields = ('id', 'step', 'option_text', 'is_correct', 'xp_awarded',
                  'feedback_text', 'consequence_type', 'next_step', 'display_order')


# ─── Scenario Step ─────────────────────────────────────────────────────────────

class ScenarioStepSimulationSerializer(serializers.ModelSerializer):
    """
    Used when serving a step during an active simulation.
    Includes decision options (without answer hints).
    """
    options     = DecisionOptionSimulationSerializer(many=True, read_only=True)
    nist_phase_label = serializers.CharField(source='get_nist_phase_display', read_only=True)
    step_type_label  = serializers.CharField(source='get_step_type_display', read_only=True)

    class Meta:
        model  = ScenarioStep
        fields = (
            'id', 'step_number', 'title', 'situation_text',
            'nist_phase', 'nist_phase_label',
            'step_type', 'step_type_label',
            'is_final_step', 'options',
        )


class ScenarioStepAdminSerializer(serializers.ModelSerializer):
    """Full step data for admin management."""
    options = DecisionOptionAdminSerializer(many=True, read_only=True)

    class Meta:
        model  = ScenarioStep
        fields = (
            'id', 'scenario', 'step_number', 'title', 'situation_text',
            'nist_phase', 'step_type', 'is_final_step', 'is_active', 'options',
        )


# ─── Learning Objective ────────────────────────────────────────────────────────

class LearningObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LearningObjective
        fields = ('id', 'order', 'objective_text')


# ─── Scenario ─────────────────────────────────────────────────────────────────

class ScenarioListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for scenario cards on the Category Detail page.
    Does NOT include steps — just the card-level metadata.
    """
    difficulty_label = serializers.CharField(source='get_difficulty_display', read_only=True)
    category_name    = serializers.CharField(source='category.name', read_only=True)
    category_slug    = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model  = Scenario
        fields = (
            'id', 'scenario_id', 'title', 'slug', 'overview', 'category_name', 'category_slug',
            'difficulty', 'difficulty_label', 'estimated_duration_minutes',
            'xp_completion_bonus', 'xp_perfect_score_bonus', 'total_steps',
            'decision_step_count',
        )


class ScenarioDetailSerializer(serializers.ModelSerializer):
    """
    Full scenario data for the Scenario Overview page.
    Includes learning objectives and NIST phases covered.
    Does NOT include step content (that comes from simulation endpoints).
    """
    difficulty_label    = serializers.CharField(source='get_difficulty_display', read_only=True)
    category_name       = serializers.CharField(source='category.name', read_only=True)
    category_slug       = serializers.CharField(source='category.slug', read_only=True)
    learning_objectives = LearningObjectiveSerializer(many=True, read_only=True)
    total_xp_available  = serializers.IntegerField(read_only=True)
    nist_phases_in_scenario = serializers.SerializerMethodField()

    class Meta:
        model  = Scenario
        fields = (
            'id', 'scenario_id', 'title', 'slug', 'student_role', 'overview',
            'category_name', 'category_slug',
            'difficulty', 'difficulty_label',
            'estimated_duration_minutes',
            'xp_completion_bonus', 'xp_perfect_score_bonus',
            'total_xp_available', 'total_steps', 'decision_step_count',
            'nist_phases_in_scenario',
            'learning_objectives',
            'version',
        )

    def get_nist_phases_in_scenario(self, obj):
        """Returns ordered unique NIST phases covered by this scenario's steps."""
        phases = (
            obj.steps.filter(is_active=True)
            .order_by('step_number')
            .values_list('nist_phase', flat=True)
            .distinct()
        )
        # Map codes to labels for the frontend
        phase_map = dict(ScenarioStep.NISTPhase.choices)
        seen = []
        for p in phases:
            if p not in seen:
                seen.append(p)
        return [{'code': p, 'label': phase_map.get(p, p)} for p in seen]


class ScenarioAdminSerializer(serializers.ModelSerializer):
    """Full scenario data for admin CRUD including write fields."""
    learning_objectives = LearningObjectiveSerializer(many=True, read_only=True)

    class Meta:
        model  = Scenario
        fields = (
            'id', 'scenario_id', 'category', 'title', 'slug', 'student_role',
            'overview', 'difficulty', 'estimated_duration_minutes',
            'xp_completion_bonus', 'xp_perfect_score_bonus',
            'version', 'is_active', 'created_at', 'updated_at',
            'learning_objectives',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


# ─── Category ─────────────────────────────────────────────────────────────────

class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category cards on the Categories page."""
    active_scenario_count = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Category
        fields = (
            'id', 'name', 'slug', 'short_summary', 'description',
            'icon_name', 'color_theme', 'display_order',
            'active_scenario_count',
        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Full category data with nested scenario list (cards only).
    Used on the Category Detail page.
    """
    scenarios = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = (
            'id', 'name', 'slug', 'short_summary', 'description',
            'icon_name', 'color_theme', 'display_order', 'scenarios',
        )

    def get_scenarios(self, obj):
        """Returns active scenarios grouped by difficulty."""
        active_scenarios = obj.scenarios.filter(is_active=True).order_by('difficulty', 'scenario_id')
        return ScenarioListSerializer(active_scenarios, many=True).data


class CategoryAdminSerializer(serializers.ModelSerializer):
    """Full category data for admin CRUD."""
    class Meta:
        model  = Category
        fields = (
            'id', 'name', 'slug', 'short_summary', 'description',
            'icon_name', 'color_theme', 'display_order', 'is_active',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')
