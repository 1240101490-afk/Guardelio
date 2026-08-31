"""
Guardelio — Progress Serializers
Output shapes for SimulationSession, SessionDecision, Badge, XPHistory, and Dashboard.
"""

from rest_framework import serializers
from .models import SimulationSession, SessionDecision, Badge, UserBadge, XPHistory


# ─── Session List ──────────────────────────────────────────────────────────────

class SessionListSerializer(serializers.ModelSerializer):
    """Lightweight session card for the Progress page session history list."""
    scenario_title      = serializers.CharField(source='scenario.title', read_only=True)
    scenario_id_code    = serializers.CharField(source='scenario.scenario_id', read_only=True)
    category_name       = serializers.CharField(source='scenario.category.name', read_only=True)
    difficulty          = serializers.CharField(source='scenario.difficulty', read_only=True)
    difficulty_label    = serializers.CharField(source='scenario.get_difficulty_display', read_only=True)
    status_label        = serializers.CharField(source='get_status_display', read_only=True)
    accuracy_percent    = serializers.IntegerField(source='accuracy_percentage', read_only=True)
    duration_minutes    = serializers.FloatField(read_only=True)
    is_perfect_score    = serializers.BooleanField(read_only=True)

    class Meta:
        model  = SimulationSession
        fields = (
            'id', 'scenario_title', 'scenario_id_code', 'category_name',
            'difficulty', 'difficulty_label',
            'status', 'status_label',
            'total_xp_earned', 'correct_decisions', 'total_decisions',
            'accuracy_percent', 'is_perfect_score', 'duration_minutes',
            'started_at', 'completed_at',
        )


# ─── In-Progress Session (for resume) ─────────────────────────────────────────

class InProgressSessionSerializer(serializers.ModelSerializer):
    """Includes the current step for seamless resume functionality."""
    from apps.scenarios.serializers import ScenarioStepSimulationSerializer
    scenario_title   = serializers.CharField(source='scenario.title', read_only=True)
    scenario_id_code = serializers.CharField(source='scenario.scenario_id', read_only=True)
    category_name    = serializers.CharField(source='scenario.category.name', read_only=True)
    accuracy_percent = serializers.IntegerField(source='accuracy_percentage', read_only=True)

    class Meta:
        model  = SimulationSession
        fields = (
            'id', 'scenario_title', 'scenario_id_code', 'category_name',
            'status', 'total_xp_earned', 'correct_decisions', 'total_decisions',
            'accuracy_percent', 'started_at', 'current_step',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Inline the current step data using the simulation serializer
        if instance.current_step:
            from apps.scenarios.serializers import ScenarioStepSimulationSerializer
            data['current_step'] = ScenarioStepSimulationSerializer(instance.current_step).data
        return data


# ─── Badge ─────────────────────────────────────────────────────────────────────

class BadgeSerializer(serializers.ModelSerializer):
    badge_type_label   = serializers.CharField(source='get_badge_type_display', read_only=True)
    criteria_type_label = serializers.CharField(source='get_criteria_type_display', read_only=True)

    class Meta:
        model  = Badge
        fields = (
            'id', 'name', 'description', 'badge_type', 'badge_type_label',
            'criteria_type', 'criteria_type_label', 'criteria_value', 'icon_name',
        )


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model  = UserBadge
        fields = ('id', 'badge', 'earned_at')


# ─── XP History ────────────────────────────────────────────────────────────────

class XPHistorySerializer(serializers.ModelSerializer):
    transaction_type_label = serializers.CharField(source='get_transaction_type_display', read_only=True)
    scenario_title = serializers.SerializerMethodField()

    class Meta:
        model  = XPHistory
        fields = (
            'id', 'amount', 'transaction_type', 'transaction_type_label',
            'balance_after', 'description', 'scenario_title', 'earned_at',
        )

    def get_scenario_title(self, obj):
        if obj.session and obj.session.scenario:
            return obj.session.scenario.title
        return None


# ─── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardSerializer(serializers.Serializer):
    """
    Student dashboard summary — assembled in the view from multiple queries.
    Not a model serializer; pure output shape.
    """
    total_xp              = serializers.IntegerField()
    completed_count       = serializers.IntegerField()
    in_progress_count     = serializers.IntegerField()
    badge_count           = serializers.IntegerField()
    average_accuracy      = serializers.FloatField()
    categories_started    = serializers.IntegerField()
    categories_completed  = serializers.IntegerField()
    recent_sessions       = SessionListSerializer(many=True)
    recent_badges         = UserBadgeSerializer(many=True)
    in_progress_sessions  = SessionListSerializer(many=True)
