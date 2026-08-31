"""
Guardelio — Core Utilities
Shared response helpers used across all app views.
"""

from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message='Success.', status_code=http_status.HTTP_200_OK):
    """Returns a standardised success envelope."""
    return Response(
        {'success': True, 'data': data, 'message': message},
        status=status_code,
    )


def created_response(data=None, message='Created successfully.'):
    """Convenience wrapper for HTTP 201."""
    return Response(
        {'success': True, 'data': data, 'message': message},
        status=http_status.HTTP_201_CREATED,
    )


def error_response(message='An error occurred.', errors=None,
                   status_code=http_status.HTTP_400_BAD_REQUEST):
    """Returns a standardised error envelope."""
    return Response(
        {'success': False, 'data': None, 'message': message, 'errors': errors},
        status=status_code,
    )


def not_found_response(message='Resource not found.'):
    return error_response(message=message, status_code=http_status.HTTP_404_NOT_FOUND)


def forbidden_response(message='You do not have permission to perform this action.'):
    return error_response(message=message, status_code=http_status.HTTP_403_FORBIDDEN)


def conflict_response(message='Conflict.', errors=None):
    return error_response(message=message, errors=errors,
                          status_code=http_status.HTTP_409_CONFLICT)
