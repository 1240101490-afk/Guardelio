"""
Guardelio — Accounts Service Layer
Business logic for auth and user management, isolated from HTTP views.
"""

from django.utils import timezone
from .models import User, StudentProfile


def register_student(validated_data: dict) -> User:
    """
    Creates a new student User.
    Called by RegisterView after serializer validation passes.
    StudentProfile is auto-created via the post_save signal in signals.py.
    """
    password  = validated_data.pop('password')
    validated_data.pop('password2', None)
    user = User(**validated_data, role=User.Role.STUDENT)
    user.set_password(password)
    user.save()
    return user


def get_user_profile(user: User) -> User:
    """
    Returns the user instance; ensures StudentProfile exists for students.
    The profile is fetched via the `profile` related name (1-to-1).
    """
    if user.is_student:
        StudentProfile.objects.get_or_create(user=user)
    return user


def update_last_active(user: User) -> None:
    """Updates the StudentProfile.last_active timestamp. Called after simulation steps."""
    if user.is_student and hasattr(user, 'profile'):
        user.profile.last_active = timezone.now()
        user.profile.save(update_fields=['last_active'])
