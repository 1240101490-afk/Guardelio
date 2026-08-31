"""
Guardelio — Custom Exception Handler
Converts all Django/DRF exceptions into the standard Guardelio response envelope.

Standard Success:  { "success": true,  "data": {...},  "message": "..." }
Standard Error:    { "success": false, "data": null,  "message": "...", "errors": {...} }
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated


# Friendly messages for common HTTP status codes
_STATUS_MESSAGES = {
    400: 'Invalid request data.',
    401: 'Authentication required. Please log in.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    405: 'Method not allowed.',
    429: 'Too many requests. Please slow down.',
    500: 'An unexpected internal error occurred. Please try again.',
}


def guardelio_exception_handler(exc, context):
    """
    Central exception handler registered in REST_FRAMEWORK settings.
    Wraps every error response in the Guardelio envelope format.
    """
    # Let DRF handle the exception first to get its Response
    response = exception_handler(exc, context)

    if response is not None:
        # Override message for auth errors to be user-friendly
        if isinstance(exc, NotAuthenticated):
            message = 'Authentication required. Please log in to continue.'
            errors  = None
        elif isinstance(exc, AuthenticationFailed):
            message = 'Invalid credentials. Please check your username and password.'
            errors  = None
        else:
            error_data = response.data
            if isinstance(error_data, dict):
                # Use 'detail' if present, else compose from first field error
                detail = error_data.get('detail')
                if detail:
                    message = str(detail)
                    errors  = {k: v for k, v in error_data.items() if k != 'detail'} or None
                else:
                    # Validation errors — show field-level errors
                    message = _STATUS_MESSAGES.get(response.status_code, 'An error occurred.')
                    errors  = error_data
            elif isinstance(error_data, list):
                message = str(error_data[0]) if error_data else 'An error occurred.'
                errors  = None
            else:
                message = str(error_data)
                errors  = None

        response.data = {
            'success': False,
            'data':    None,
            'message': message,
            'errors':  errors,
        }
        return response

    # Unhandled exception (500) — return sanitized message, never expose stack trace
    return Response(
        {
            'success': False,
            'data':    None,
            'message': 'An unexpected internal error occurred. Please try again.',
            'errors':  None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

