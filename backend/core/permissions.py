"""
Guardelio — Core Permission Classes
Role-based access control for student and admin roles.
"""

from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Allows access only to authenticated users with role='student'.
    """
    message = 'Access restricted to student accounts.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'student'
        )


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users with role='admin'.
    """
    message = 'Access restricted to administrator accounts.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsStudentOrAdmin(BasePermission):
    """
    Allows access to both students and admins.
    Used for read-only endpoints like category/scenario browsing.
    """
    message = 'Authentication required.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('student', 'admin')
        )
