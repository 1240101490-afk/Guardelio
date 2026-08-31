"""
Guardelio — Scenarios Django Admin Registration
Allows administrators to manage all content without touching source code.

Admin capabilities:
- Create/edit/delete Categories
- Create/edit/delete Scenarios with full metadata
- Add/edit/delete Learning Objectives per Scenario
- Add/edit/delete Steps per Scenario
- Add/edit/delete Decision Options per Step (with branching config)
"""
from django.contrib import admin
from .models import Category, Scenario, LearningObjective, ScenarioStep, DecisionOption


class LearningObjectiveInline(admin.TabularInline):
    model   = LearningObjective
    extra   = 3
    fields  = ('order', 'objective_text')
    ordering = ('order',)


class DecisionOptionInline(admin.TabularInline):
    model   = DecisionOption
    fk_name = 'step'
    extra   = 2
    fields  = ('display_order', 'option_text', 'is_correct', 'xp_awarded', 'consequence_type', 'next_step', 'feedback_text')
    ordering = ('display_order',)



class ScenarioStepInline(admin.StackedInline):
    model   = ScenarioStep
    extra   = 1
    fields  = ('step_number', 'title', 'nist_phase', 'step_type', 'situation_text', 'is_final_step', 'is_active')
    ordering = ('step_number',)
    show_change_link = True   # Link to full step edit page where options are managed


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'display_order', 'active_scenario_count', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order',)


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display  = ('scenario_id', 'title', 'category', 'difficulty', 'xp_completion_bonus', 'is_active')
    list_filter   = ('difficulty', 'category', 'is_active')
    search_fields = ('scenario_id', 'title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LearningObjectiveInline, ScenarioStepInline]
    readonly_fields = ('created_at', 'updated_at', 'total_xp_available', 'total_steps')
    ordering = ('category', 'difficulty', 'scenario_id')

    fieldsets = (
        ('Identity', {'fields': ('scenario_id', 'title', 'slug', 'category', 'difficulty', 'version')}),
        ('Content', {'fields': ('student_role', 'overview')}),
        ('Settings', {'fields': ('estimated_duration_minutes', 'xp_completion_bonus', 'xp_perfect_score_bonus', 'is_active')}),
        ('Read Only', {'fields': ('total_xp_available', 'total_steps', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(ScenarioStep)
class ScenarioStepAdmin(admin.ModelAdmin):
    list_display  = ('scenario', 'step_number', 'title', 'nist_phase', 'step_type', 'is_final_step', 'is_active')
    list_filter   = ('nist_phase', 'step_type', 'is_final_step', 'scenario__category')
    search_fields = ('title', 'situation_text', 'scenario__title')
    inlines       = [DecisionOptionInline]
    ordering      = ('scenario', 'step_number')


@admin.register(DecisionOption)
class DecisionOptionAdmin(admin.ModelAdmin):
    list_display  = ('step', 'option_text_short', 'is_correct', 'xp_awarded', 'consequence_type')
    list_filter   = ('is_correct', 'consequence_type')
    search_fields = ('option_text', 'feedback_text')

    def option_text_short(self, obj):
        return obj.option_text[:60]
    option_text_short.short_description = 'Option Text'
