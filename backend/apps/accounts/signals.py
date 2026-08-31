"""
Guardelio — Accounts Signals
Automatically creates a StudentProfile when a new student User is registered.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """
    Creates a StudentProfile automatically when a new student-role User is registered.
    Admin users do not receive a StudentProfile — only students.
    This runs exactly once per registration (created=True guard).
    """
    if created and instance.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)

