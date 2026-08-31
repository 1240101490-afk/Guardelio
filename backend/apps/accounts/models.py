"""
Guardelio — Accounts Models
Agent 2 (Django Model Designer) + Agent 4 (User Progress Models)

Models:
    User            — Custom user extending AbstractUser. Single source of truth
                      for authentication, role, and lifetime XP.
    StudentProfile  — Extended profile data for student-role users.

Design Decisions:
    - AbstractUser is extended (not replaced) so Django's auth system remains intact.
    - 'role' field on User avoids a separate Group table for a two-role system.
    - 'total_xp' is a denormalized cache on User for fast navbar display.
      It is updated atomically via XPService after every correct decision.
    - StudentProfile is a separate 1-to-1 model to keep User lean and allow
      profile data to be fetched independently when needed.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Custom User model — the single authentication entity for Guardelio.

    Roles:
        student  — Can browse categories, run simulations, view their own progress.
        admin    — Can manage all content and view reports. Cannot run simulations.

    Fields inherited from AbstractUser:
        username, email, password, first_name, last_name,
        is_active, is_staff, is_superuser, date_joined, last_login
    """

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN   = 'admin',   'Administrator'

    # Override email to enforce uniqueness — used as secondary login identifier
    email = models.EmailField(
        unique=True,
        verbose_name='Email Address',
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        verbose_name='User Role',
    )

    # Denormalized XP total — updated atomically by XPService
    # Avoids expensive SUM() query on every profile/navbar load
    total_xp = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Total XP Earned',
    )

    # Require email field during user creation
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table  = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN


class StudentProfile(models.Model):
    """
    Extended profile data for student-role users.

    Kept separate from User to:
    - Maintain a lean User model focused on authentication
    - Allow profile data to evolve independently
    - Support future profile features without touching core auth

    Relationship: One-to-One with User (created automatically on student registration)
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User Account',
    )

    # Institution or university name (optional, for university context)
    institution = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Institution / University',
    )

    # Short bio or description (optional)
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='Short Bio',
    )

    # Profile avatar stored as a filename/icon reference (not file upload for MVP)
    avatar_name = models.CharField(
        max_length=100,
        blank=True,
        default='default_avatar',
        verbose_name='Avatar Identifier',
    )

    # Tracks the last time the student was active in any simulation
    last_active = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Last Active At',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table     = 'accounts_studentprofile'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f'Profile — {self.user.username}'
