"""
Guardelio — Accounts Views
Handles: Register, Login, Logout, Token Refresh, Profile GET/PATCH.

Design:
  - Views contain NO business logic — they delegate to services/serializers.
  - Every response uses the Guardelio envelope from core.utils.
  - JWT tokens are issued via simplejwt; logout blacklists the refresh token.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from core.utils import success_response, created_response, error_response
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from .services import get_user_profile


# ─── Register ──────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    """
    POST /api/v1/auth/register/
    Public endpoint. Creates a new student account.
    Returns the new user's public profile (no tokens — must login separately).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Registration failed. Please check the provided data.',
                errors=serializer.errors,
            )
        user = serializer.save()
        profile_data = UserProfileSerializer(user).data
        return created_response(
            data=profile_data,
            message='Account created successfully. Please log in.',
        )


# ─── Login ─────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Public endpoint. Authenticates user, returns JWT access + refresh tokens.

    Request body: { "username": "...", "password": "..." }
    Response:     { access, refresh, user: { ...profile } }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return error_response(
                message='Username and password are required.',
                errors={'non_field_errors': ['Both fields are required.']},
            )

        # Authenticate (handles both username and email)
        user = authenticate(request, username=username, password=password)

        # Also try by email if username auth fails
        if user is None:
            from .models import User as UserModel
            try:
                user_obj = UserModel.objects.get(email__iexact=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except UserModel.DoesNotExist:
                pass

        if user is None:
            return error_response(
                message='Invalid credentials. Please check your username and password.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return error_response(
                message='Your account has been deactivated. Please contact support.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        profile = get_user_profile(user)

        return success_response(
            data={
                'access':  str(refresh.access_token),
                'refresh': str(refresh),
                'user':    UserProfileSerializer(profile).data,
            },
            message='Login successful.',
        )


# ─── Token Refresh ─────────────────────────────────────────────────────────────

class TokenRefreshView(APIView):
    """
    POST /api/v1/auth/refresh/
    Public endpoint. Accepts a refresh token and returns a new access token.

    Request body: { "refresh": "<refresh_token>" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh', '')
        if not refresh_token:
            return error_response(
                message='Refresh token is required.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            return success_response(
                data={'access': str(token.access_token)},
                message='Token refreshed successfully.',
            )
        except TokenError as e:
            return error_response(
                message='Invalid or expired refresh token. Please log in again.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


# ─── Logout ────────────────────────────────────────────────────────────────────

class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Authenticated. Blacklists the provided refresh token, invalidating the session.

    Request body: { "refresh": "<refresh_token>" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh', '')
        if not refresh_token:
            return error_response(message='Refresh token is required.')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(message='Logged out successfully.')
        except TokenError:
            # Token may already be blacklisted — treat as success
            return success_response(message='Logged out successfully.')


# ─── Profile ───────────────────────────────────────────────────────────────────

class ProfileView(APIView):
    """
    GET  /api/v1/auth/me/  — Returns authenticated user's full profile.
    PATCH /api/v1/auth/me/ — Partially updates name, password, or nested profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_profile(request.user)
        return success_response(
            data=UserProfileSerializer(user).data,
            message='Profile retrieved successfully.',
        )

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if not serializer.is_valid():
            return error_response(
                message='Profile update failed.',
                errors=serializer.errors,
            )
        user = serializer.save()
        return success_response(
            data=UserProfileSerializer(user).data,
            message='Profile updated successfully.',
        )
