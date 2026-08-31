"""
Guardelio — Scenarios URL Configuration

Prefix: /api/v1/  (included from config/urls.py)

Routes:
  GET  categories/          → List all active categories
  GET  categories/<slug>/   → Category detail + nested scenario cards
  GET  scenarios/           → List scenarios (filterable: ?category=, ?difficulty=, ?search=)
  GET  scenarios/<int:pk>/  → Scenario detail (overview + objectives)
"""

from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    ScenarioListView,
    ScenarioDetailView,
)

urlpatterns = [
    path('categories/',              CategoryListView.as_view(),   name='category-list'),
    path('categories/<slug:slug>/',  CategoryDetailView.as_view(), name='category-detail'),
    path('scenarios/',               ScenarioListView.as_view(),   name='scenario-list'),
    path('scenarios/<int:pk>/',      ScenarioDetailView.as_view(), name='scenario-detail'),
]
