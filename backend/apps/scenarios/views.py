"""
Guardelio — Scenarios Views (Public Read-Only)
Serves category and scenario data to authenticated students and admins.

All endpoints are READ-ONLY here.
Write (CRUD) operations are in apps/reports/views.py (admin-only).
"""

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Count, Q

from core.utils import success_response, not_found_response
from core.permissions import IsStudentOrAdmin
from .models import Category, Scenario
from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ScenarioListSerializer,
    ScenarioDetailSerializer,
)


# ─── Categories ────────────────────────────────────────────────────────────────

class CategoryListView(APIView):
    """
    GET /api/v1/categories/
    Returns all active categories, ordered by display_order.
    Accessible to both students and admins.
    """
    permission_classes = [IsStudentOrAdmin]

    def get(self, request):
        categories = (
            Category.objects
            .filter(is_active=True)
            .annotate(active_scenario_count=Count(
                'scenarios', filter=Q(scenarios__is_active=True)
            ))
            .order_by('display_order', 'name')
        )
        serializer = CategoryListSerializer(categories, many=True)
        return success_response(
            data=serializer.data,
            message=f'{categories.count()} categories retrieved.',
        )




class CategoryDetailView(APIView):
    """
    GET /api/v1/categories/<slug>/
    Returns a single category with its full description and nested scenario list (cards).
    """
    permission_classes = [IsStudentOrAdmin]

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug, is_active=True)
        except Category.DoesNotExist:
            return not_found_response(f'Category "{slug}" not found.')

        serializer = CategoryDetailSerializer(category)
        return success_response(
            data=serializer.data,
            message=f'Category "{category.name}" retrieved.',
        )


# ─── Scenarios ─────────────────────────────────────────────────────────────────

class ScenarioListView(APIView):
    """
    GET /api/v1/scenarios/
    Returns active scenarios with optional query param filters:
      ?category=<slug>         — filter by category slug
      ?difficulty=<level>      — beginner | intermediate | advanced
      ?search=<query>          — title or scenario_id search
    """
    permission_classes = [IsStudentOrAdmin]

    def get(self, request):
        queryset = Scenario.objects.filter(is_active=True).select_related('category')

        category_slug = request.query_params.get('category')
        difficulty    = request.query_params.get('difficulty')
        search        = request.query_params.get('search', '').strip()

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if search:
            queryset = queryset.filter(title__icontains=search) | \
                       queryset.filter(scenario_id__icontains=search)

        queryset = queryset.order_by('category__display_order', 'difficulty', 'scenario_id')
        serializer = ScenarioListSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message=f'{queryset.count()} scenarios retrieved.',
        )


class ScenarioDetailView(APIView):
    """
    GET /api/v1/scenarios/<int:pk>/
    Returns the full scenario overview: metadata, learning objectives, NIST phases.
    Does NOT include step content — that is served by the simulation engine.
    """
    permission_classes = [IsStudentOrAdmin]

    def get(self, request, pk):
        try:
            scenario = (
                Scenario.objects
                .select_related('category')
                .prefetch_related('learning_objectives', 'steps')
                .get(pk=pk, is_active=True)
            )
        except Scenario.DoesNotExist:
            return not_found_response(f'Scenario #{pk} not found.')

        serializer = ScenarioDetailSerializer(scenario)
        return success_response(
            data=serializer.data,
            message=f'Scenario "{scenario.title}" retrieved.',
        )
