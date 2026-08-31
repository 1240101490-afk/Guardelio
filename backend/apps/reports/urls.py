"""
Guardelio — Admin URL Configuration

Prefix: /api/v1/admin/  (included from config/urls.py)

Content Management:
  GET/POST          categories/
  GET/PATCH/DELETE  categories/<int:pk>/
  GET/POST          scenarios/
  GET/PATCH/DELETE  scenarios/<int:pk>/
  GET/POST          scenarios/<int:scenario_pk>/steps/
  GET/PATCH/DELETE  steps/<int:pk>/
  GET/POST          steps/<int:step_pk>/options/
  GET/PATCH/DELETE  options/<int:pk>/
  GET/POST          scenarios/<int:scenario_pk>/objectives/
  PATCH/DELETE      objectives/<int:pk>/

User Management:
  GET               users/
  GET/PATCH         users/<int:pk>/

Analytics:
  GET               stats/
  GET               reports/scenarios/
  GET               reports/users/
"""

from django.urls import path
from .views import (
    AdminDashboardView,
    AdminCategoryListCreateView,
    AdminCategoryDetailView,
    AdminScenarioListCreateView,
    AdminScenarioDetailView,
    AdminStepListCreateView,
    AdminStepDetailView,
    AdminOptionListCreateView,
    AdminOptionDetailView,
    AdminObjectiveListCreateView,
    AdminObjectiveDetailView,
    AdminUserListView,
    AdminUserDetailView,
    AdminScenarioReportView,
    AdminUserReportView,
)

urlpatterns = [
    # ── Dashboard Stats ─────────────────────────────────────────────────────
    path('stats/',                                        AdminDashboardView.as_view(),            name='admin-stats'),

    # ── Category CRUD ────────────────────────────────────────────────────────
    path('categories/',                                   AdminCategoryListCreateView.as_view(),   name='admin-category-list'),
    path('categories/<int:pk>/',                          AdminCategoryDetailView.as_view(),       name='admin-category-detail'),

    # ── Scenario CRUD ────────────────────────────────────────────────────────
    path('scenarios/',                                    AdminScenarioListCreateView.as_view(),   name='admin-scenario-list'),
    path('scenarios/<int:pk>/',                           AdminScenarioDetailView.as_view(),       name='admin-scenario-detail'),

    # ── Step CRUD (nested under scenario for creation, standalone for edit) ──
    path('scenarios/<int:scenario_pk>/steps/',            AdminStepListCreateView.as_view(),       name='admin-step-list'),
    path('steps/<int:pk>/',                               AdminStepDetailView.as_view(),           name='admin-step-detail'),

    # ── Decision Option CRUD ─────────────────────────────────────────────────
    path('steps/<int:step_pk>/options/',                  AdminOptionListCreateView.as_view(),     name='admin-option-list'),
    path('options/<int:pk>/',                             AdminOptionDetailView.as_view(),         name='admin-option-detail'),

    # ── Learning Objective CRUD ──────────────────────────────────────────────
    path('scenarios/<int:scenario_pk>/objectives/',       AdminObjectiveListCreateView.as_view(),  name='admin-objective-list'),
    path('objectives/<int:pk>/',                          AdminObjectiveDetailView.as_view(),      name='admin-objective-detail'),

    # ── User Management ──────────────────────────────────────────────────────
    path('users/',                                        AdminUserListView.as_view(),             name='admin-user-list'),
    path('users/<int:pk>/',                               AdminUserDetailView.as_view(),           name='admin-user-detail'),

    # ── Analytics Reports ────────────────────────────────────────────────────
    path('reports/scenarios/',                            AdminScenarioReportView.as_view(),       name='admin-report-scenarios'),
    path('reports/users/',                                AdminUserReportView.as_view(),           name='admin-report-users'),
]

