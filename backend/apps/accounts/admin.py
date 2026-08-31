"""
Guardelio — Accounts Django Admin Registration
Provides admin interface for user management.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fields = ('institution', 'bio', 'avatar_name', 'last_active')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline,)
    list_display  = ('username', 'email', 'full_name', 'role', 'total_xp', 'is_active', 'date_joined')
    list_filter   = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Guardelio Fields', {'fields': ('role', 'total_xp')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Guardelio Fields', {'fields': ('email', 'first_name', 'last_name', 'role')}),
    )
