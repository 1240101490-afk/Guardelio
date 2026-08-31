"""
Guardelio — Accounts URL Configuration

Prefix: /api/v1/auth/

Routes:
  POST   register/   → Create student account
  POST   login/      → Authenticate, receive JWT tokens
  POST   refresh/    → Get new access token from refresh token
  POST   logout/     → Blacklist refresh token
  GET    me/         → Retrieve current user profile
  PATCH  me/         → Update current user profile
"""

from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView, LogoutView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(),      name='auth-register'),
    path('login/',    LoginView.as_view(),          name='auth-login'),
    path('refresh/',  TokenRefreshView.as_view(),   name='auth-refresh'),
    path('logout/',   LogoutView.as_view(),          name='auth-logout'),
    path('me/',       ProfileView.as_view(),         name='auth-profile'),
]
