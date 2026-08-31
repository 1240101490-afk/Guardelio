"""
Guardelio — Progress Django Admin Registration
"""
from django.contrib import admin
from .models import Badge, UserBadge, SimulationSession, SessionDecision, XPHistory


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'badge_type', 'criteria_type', 'criteria_value', 'is_active')
    list_filter   = ('badge_type', 'criteria_type', 'is_active')
    search_fields = ('name', 'description')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display  = ('user', 'badge', 'earned_at')
    list_filter   = ('badge__badge_type',)
    search_fields = ('user__username', 'badge__name')
    readonly_fields = ('earned_at',)


class SessionDecisionInline(admin.TabularInline):
    model    = SessionDecision
    extra    = 0
    readonly_fields = ('step', 'chosen_option', 'xp_earned_at_step', 'responded_at')
    can_delete = False


@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display  = ('student', 'scenario', 'status', 'total_xp_earned', 'accuracy_percentage', 'started_at', 'completed_at')
    list_filter   = ('status', 'scenario__category', 'scenario__difficulty')
    search_fields = ('student__username', 'scenario__title')
    readonly_fields = ('started_at', 'scenario_version', 'accuracy_percentage', 'duration_minutes')
    inlines       = [SessionDecisionInline]
    ordering      = ('-started_at',)


@admin.register(XPHistory)
class XPHistoryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'amount', 'transaction_type', 'balance_after', 'earned_at')
    list_filter   = ('transaction_type',)
    search_fields = ('user__username', 'description')
    readonly_fields = ('earned_at',)
