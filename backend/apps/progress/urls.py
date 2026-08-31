"""
Guardelio — Progress & Simulation URL Configuration

Included at two separate prefixes in config/urls.py:
  path('api/v1/simulation/', include((simulation_urlpatterns, 'simulation')))
  path('api/v1/progress/',   include((progress_urlpatterns, 'progress')))

Simulation routes (via /api/v1/simulation/):
  POST   start/                    → Start or resume a simulation
  GET    <int:session_id>/         → Get current session state
  POST   <int:session_id>/respond/ → Submit step response
  GET    <int:session_id>/result/  → Get session result

Progress routes (via /api/v1/progress/):
  GET    dashboard/                → Student dashboard summary
  GET    sessions/                 → Full session history
  GET    badges/                   → Earned badges only
  GET    all-badges/               → Full badge catalog with is_earned flag
  GET    xp-history/               → XP transaction history
  GET    stats/                    → Learning statistics
"""

from django.urls import path
from .views import (
    StartSimulationView,
    SessionStateView,
    RespondToStepView,
    SessionResultView,
    DashboardView,
    SessionHistoryView,
    BadgeListView,
    AllBadgeCatalogView,
    XPHistoryView,
    LearningStatsView,
)

simulation_urlpatterns = [
    path('start/',                           StartSimulationView.as_view(),  name='sim-start'),
    path('<int:session_id>/',                SessionStateView.as_view(),     name='sim-state'),
    path('<int:session_id>/respond/',        RespondToStepView.as_view(),    name='sim-respond'),
    path('<int:session_id>/result/',         SessionResultView.as_view(),    name='sim-result'),
]

progress_urlpatterns = [
    path('dashboard/',   DashboardView.as_view(),          name='progress-dashboard'),
    path('sessions/',    SessionHistoryView.as_view(),      name='progress-sessions'),
    path('badges/',      BadgeListView.as_view(),           name='progress-badges'),
    path('all-badges/',  AllBadgeCatalogView.as_view(),     name='progress-all-badges'),
    path('xp-history/',  XPHistoryView.as_view(),           name='progress-xp-history'),
    path('stats/',       LearningStatsView.as_view(),       name='progress-stats'),
]

# urlpatterns used if this module is included directly (legacy fallback)
urlpatterns = simulation_urlpatterns + progress_urlpatterns

