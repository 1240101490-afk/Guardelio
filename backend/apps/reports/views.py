"""
Guardelio — Admin Views (Agent 5)
Complete CRUD for all content entities + user management + analytics reports.

All views require IsAdmin permission — students receive HTTP 403.

Prefix: /api/v1/admin/

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
  GET/PATCH/DELETE  objectives/<int:pk>/

User Management:
  GET               users/
  GET/PATCH         users/<int:pk>/

Analytics:
  GET               stats/
  GET               reports/scenarios/
  GET               reports/users/
"""

from django.db.models import Count, Avg, Q
from rest_framework.views import APIView
from rest_framework import status

from core.utils import (
    success_response, created_response, error_response, not_found_response,
)
from core.permissions import IsAdmin

from apps.scenarios.models import (
    Category, Scenario, LearningObjective, ScenarioStep, DecisionOption
)
from apps.scenarios.serializers import (
    CategoryListSerializer, CategoryAdminSerializer,
    ScenarioAdminSerializer, ScenarioListSerializer,
    ScenarioStepAdminSerializer, DecisionOptionAdminSerializer,
    LearningObjectiveSerializer,
)
from apps.accounts.models import User
from apps.progress.models import SimulationSession

from .serializers import (
    AdminCategoryWriteSerializer,
    AdminScenarioWriteSerializer,
    AdminStepWriteSerializer,
    AdminOptionWriteSerializer,
    AdminLearningObjectiveSerializer,
    AdminUserListSerializer,
    AdminUserUpdateSerializer,
    AdminDashboardStatsSerializer,
    ScenarioAnalyticsSerializer,
)


# ─── Admin Dashboard Stats ─────────────────────────────────────────────────────

class AdminDashboardView(APIView):
    """
    GET /api/v1/admin/stats/
    Returns platform-wide statistics for the admin dashboard.
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        completed_qs = SimulationSession.objects.filter(
            status=SimulationSession.Status.COMPLETED
        )
        avg_acc_sessions = [
            s for s in completed_qs.all() if s.total_decisions > 0
        ]
        avg_accuracy = 0.0
        if avg_acc_sessions:
            avg_accuracy = round(
                sum(s.accuracy_percentage for s in avg_acc_sessions) / len(avg_acc_sessions), 1
            )

        # Top scenario by completion count
        top = (
            SimulationSession.objects
            .filter(status=SimulationSession.Status.COMPLETED)
            .values('scenario__title')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        top_title = top['scenario__title'] if top else None

        return success_response(
            data={
                'total_users':        User.objects.count(),
                'active_students':    User.objects.filter(role='student', is_active=True).count(),
                'total_categories':   Category.objects.filter(is_active=True).count(),
                'total_scenarios':    Scenario.objects.filter(is_active=True).count(),
                'total_sessions':     SimulationSession.objects.count(),
                'completed_sessions': completed_qs.count(),
                'average_accuracy':   avg_accuracy,
                'top_scenario_title': top_title,
            },
            message='Admin statistics retrieved.',
        )


# ─── Category CRUD ─────────────────────────────────────────────────────────────

class AdminCategoryListCreateView(APIView):
    """
    GET  /api/v1/admin/categories/ → List ALL categories (including inactive)
    POST /api/v1/admin/categories/ → Create new category
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        categories = Category.objects.all().order_by('display_order')
        serializer = CategoryAdminSerializer(categories, many=True)
        return success_response(data=serializer.data, message=f'{categories.count()} categories.')

    def post(self, request):
        serializer = AdminCategoryWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Category creation failed.',
                errors=serializer.errors,
            )
        category = serializer.save()
        return created_response(
            data=CategoryAdminSerializer(category).data,
            message=f'Category "{category.name}" created successfully.',
        )


class AdminCategoryDetailView(APIView):
    """
    GET    /api/v1/admin/categories/<int:pk>/
    PATCH  /api/v1/admin/categories/<int:pk>/
    DELETE /api/v1/admin/categories/<int:pk>/
    """
    permission_classes = [IsAdmin]

    def _get_category(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self._get_category(pk)
        if not category:
            return not_found_response(f'Category #{pk} not found.')
        return success_response(data=CategoryAdminSerializer(category).data)

    def patch(self, request, pk):
        category = self._get_category(pk)
        if not category:
            return not_found_response(f'Category #{pk} not found.')
        serializer = AdminCategoryWriteSerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Update failed.', errors=serializer.errors)
        category = serializer.save()
        return success_response(
            data=CategoryAdminSerializer(category).data,
            message=f'Category "{category.name}" updated.',
        )

    def delete(self, request, pk):
        category = self._get_category(pk)
        if not category:
            return not_found_response(f'Category #{pk} not found.')
        if Scenario.objects.filter(category=category).exists():
            # Soft-delete instead of hard delete (preserve data integrity)
            category.is_active = False
            category.save(update_fields=['is_active'])
            return success_response(message=f'Category "{category.name}" deactivated (has existing scenarios).')
        category.delete()
        return success_response(message=f'Category deleted.')


# ─── Scenario CRUD ─────────────────────────────────────────────────────────────

class AdminScenarioListCreateView(APIView):
    """
    GET  /api/v1/admin/scenarios/              → List all scenarios
    POST /api/v1/admin/scenarios/              → Create new scenario
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        category_id = request.query_params.get('category')
        scenarios = Scenario.objects.select_related('category').all()
        if category_id:
            scenarios = scenarios.filter(category_id=category_id)
        serializer = ScenarioAdminSerializer(scenarios, many=True)
        return success_response(data=serializer.data, message=f'{scenarios.count()} scenarios.')

    def post(self, request):
        serializer = AdminScenarioWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message='Scenario creation failed.', errors=serializer.errors)
        scenario = serializer.save()
        return created_response(
            data=ScenarioAdminSerializer(scenario).data,
            message=f'Scenario "{scenario.title}" created.',
        )


class AdminScenarioDetailView(APIView):
    """
    GET    /api/v1/admin/scenarios/<int:pk>/
    PATCH  /api/v1/admin/scenarios/<int:pk>/
    DELETE /api/v1/admin/scenarios/<int:pk>/
    """
    permission_classes = [IsAdmin]

    def _get_scenario(self, pk):
        try:
            return Scenario.objects.select_related('category').get(pk=pk)
        except Scenario.DoesNotExist:
            return None

    def get(self, request, pk):
        scenario = self._get_scenario(pk)
        if not scenario:
            return not_found_response(f'Scenario #{pk} not found.')
        return success_response(
            data=ScenarioAdminSerializer(scenario).data,
        )

    def patch(self, request, pk):
        scenario = self._get_scenario(pk)
        if not scenario:
            return not_found_response(f'Scenario #{pk} not found.')
        serializer = AdminScenarioWriteSerializer(scenario, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Update failed.', errors=serializer.errors)
        scenario = serializer.save()
        return success_response(
            data=ScenarioAdminSerializer(scenario).data,
            message=f'Scenario "{scenario.title}" updated.',
        )

    def delete(self, request, pk):
        scenario = self._get_scenario(pk)
        if not scenario:
            return not_found_response(f'Scenario #{pk} not found.')
        if SimulationSession.objects.filter(scenario=scenario).exists():
            scenario.is_active = False
            scenario.save(update_fields=['is_active'])
            return success_response(message=f'Scenario deactivated (has student sessions).')
        scenario.delete()
        return success_response(message='Scenario deleted.')


# ─── Scenario Step CRUD ────────────────────────────────────────────────────────

class AdminStepListCreateView(APIView):
    """
    GET  /api/v1/admin/scenarios/<int:scenario_pk>/steps/
    POST /api/v1/admin/scenarios/<int:scenario_pk>/steps/
    """
    permission_classes = [IsAdmin]

    def _get_scenario(self, scenario_pk):
        try:
            return Scenario.objects.get(pk=scenario_pk)
        except Scenario.DoesNotExist:
            return None

    def get(self, request, scenario_pk):
        scenario = self._get_scenario(scenario_pk)
        if not scenario:
            return not_found_response(f'Scenario #{scenario_pk} not found.')
        steps = scenario.steps.order_by('step_number')
        return success_response(
            data=ScenarioStepAdminSerializer(steps, many=True).data,
            message=f'{steps.count()} steps in "{scenario.title}".',
        )

    def post(self, request, scenario_pk):
        scenario = self._get_scenario(scenario_pk)
        if not scenario:
            return not_found_response(f'Scenario #{scenario_pk} not found.')
        data = {**request.data, 'scenario': scenario.pk}
        serializer = AdminStepWriteSerializer(data=data)
        if not serializer.is_valid():
            return error_response(message='Step creation failed.', errors=serializer.errors)
        step = serializer.save()
        return created_response(
            data=ScenarioStepAdminSerializer(step).data,
            message=f'Step {step.step_number} created.',
        )


class AdminStepDetailView(APIView):
    """
    GET    /api/v1/admin/steps/<int:pk>/
    PATCH  /api/v1/admin/steps/<int:pk>/
    DELETE /api/v1/admin/steps/<int:pk>/
    """
    permission_classes = [IsAdmin]

    def _get_step(self, pk):
        try:
            return ScenarioStep.objects.select_related('scenario').get(pk=pk)
        except ScenarioStep.DoesNotExist:
            return None

    def get(self, request, pk):
        step = self._get_step(pk)
        if not step:
            return not_found_response(f'Step #{pk} not found.')
        return success_response(data=ScenarioStepAdminSerializer(step).data)

    def patch(self, request, pk):
        step = self._get_step(pk)
        if not step:
            return not_found_response(f'Step #{pk} not found.')
        serializer = AdminStepWriteSerializer(step, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Step update failed.', errors=serializer.errors)
        step = serializer.save()
        return success_response(
            data=ScenarioStepAdminSerializer(step).data,
            message=f'Step {step.step_number} updated.',
        )

    def delete(self, request, pk):
        step = self._get_step(pk)
        if not step:
            return not_found_response(f'Step #{pk} not found.')
        step.is_active = False
        step.save(update_fields=['is_active'])
        return success_response(message=f'Step {step.step_number} deactivated.')


# ─── Decision Option CRUD ──────────────────────────────────────────────────────

class AdminOptionListCreateView(APIView):
    """
    GET  /api/v1/admin/steps/<int:step_pk>/options/
    POST /api/v1/admin/steps/<int:step_pk>/options/
    """
    permission_classes = [IsAdmin]

    def _get_step(self, step_pk):
        try:
            return ScenarioStep.objects.get(pk=step_pk)
        except ScenarioStep.DoesNotExist:
            return None

    def get(self, request, step_pk):
        step = self._get_step(step_pk)
        if not step:
            return not_found_response(f'Step #{step_pk} not found.')
        options = step.options.order_by('display_order')
        return success_response(
            data=DecisionOptionAdminSerializer(options, many=True).data,
            message=f'{options.count()} options for step {step.step_number}.',
        )

    def post(self, request, step_pk):
        step = self._get_step(step_pk)
        if not step:
            return not_found_response(f'Step #{step_pk} not found.')
        data = {**request.data, 'step': step.pk}
        serializer = AdminOptionWriteSerializer(data=data)
        if not serializer.is_valid():
            return error_response(message='Option creation failed.', errors=serializer.errors)
        option = serializer.save()
        return created_response(
            data=DecisionOptionAdminSerializer(option).data,
            message='Decision option created.',
        )


class AdminOptionDetailView(APIView):
    """
    GET    /api/v1/admin/options/<int:pk>/
    PATCH  /api/v1/admin/options/<int:pk>/
    DELETE /api/v1/admin/options/<int:pk>/
    """
    permission_classes = [IsAdmin]

    def _get_option(self, pk):
        try:
            return DecisionOption.objects.get(pk=pk)
        except DecisionOption.DoesNotExist:
            return None

    def get(self, request, pk):
        option = self._get_option(pk)
        if not option:
            return not_found_response(f'Option #{pk} not found.')
        return success_response(data=DecisionOptionAdminSerializer(option).data)

    def patch(self, request, pk):
        option = self._get_option(pk)
        if not option:
            return not_found_response(f'Option #{pk} not found.')
        serializer = AdminOptionWriteSerializer(option, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Option update failed.', errors=serializer.errors)
        option = serializer.save()
        return success_response(
            data=DecisionOptionAdminSerializer(option).data,
            message='Option updated.',
        )

    def delete(self, request, pk):
        option = self._get_option(pk)
        if not option:
            return not_found_response(f'Option #{pk} not found.')
        option.delete()
        return success_response(message='Decision option deleted.')


# ─── Learning Objective CRUD ───────────────────────────────────────────────────

class AdminObjectiveListCreateView(APIView):
    """
    GET  /api/v1/admin/scenarios/<int:scenario_pk>/objectives/
    POST /api/v1/admin/scenarios/<int:scenario_pk>/objectives/
    """
    permission_classes = [IsAdmin]

    def _get_scenario(self, pk):
        try:
            return Scenario.objects.get(pk=pk)
        except Scenario.DoesNotExist:
            return None

    def get(self, request, scenario_pk):
        scenario = self._get_scenario(scenario_pk)
        if not scenario:
            return not_found_response(f'Scenario #{scenario_pk} not found.')
        objs = scenario.learning_objectives.order_by('order')
        return success_response(data=LearningObjectiveSerializer(objs, many=True).data)

    def post(self, request, scenario_pk):
        scenario = self._get_scenario(scenario_pk)
        if not scenario:
            return not_found_response(f'Scenario #{scenario_pk} not found.')
        data = {**request.data, 'scenario': scenario.pk}
        serializer = AdminLearningObjectiveSerializer(data=data)
        if not serializer.is_valid():
            return error_response(message='Objective creation failed.', errors=serializer.errors)
        obj = serializer.save()
        return created_response(
            data=LearningObjectiveSerializer(obj).data,
            message='Learning objective created.',
        )


class AdminObjectiveDetailView(APIView):
    """
    PATCH  /api/v1/admin/objectives/<int:pk>/
    DELETE /api/v1/admin/objectives/<int:pk>/
    """
    permission_classes = [IsAdmin]

    def _get_objective(self, pk):
        try:
            return LearningObjective.objects.get(pk=pk)
        except LearningObjective.DoesNotExist:
            return None

    def patch(self, request, pk):
        obj = self._get_objective(pk)
        if not obj:
            return not_found_response(f'Objective #{pk} not found.')
        serializer = AdminLearningObjectiveSerializer(obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Update failed.', errors=serializer.errors)
        obj = serializer.save()
        return success_response(data=LearningObjectiveSerializer(obj).data, message='Objective updated.')

    def delete(self, request, pk):
        obj = self._get_objective(pk)
        if not obj:
            return not_found_response(f'Objective #{pk} not found.')
        obj.delete()
        return success_response(message='Objective deleted.')


# ─── User Management ───────────────────────────────────────────────────────────

class AdminUserListView(APIView):
    """
    GET /api/v1/admin/users/
    Lists all users with basic stats. Optional: ?role=student|admin, ?search=
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        role   = request.query_params.get('role')
        search = request.query_params.get('search', '').strip()

        users = User.objects.all().order_by('-date_joined')
        if role:
            users = users.filter(role=role)
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        serializer = AdminUserListSerializer(users, many=True)
        return success_response(
            data=serializer.data,
            message=f'{users.count()} users retrieved.',
        )


class AdminUserDetailView(APIView):
    """
    GET   /api/v1/admin/users/<int:pk>/
    PATCH /api/v1/admin/users/<int:pk>/  — Update is_active or role only
    """
    permission_classes = [IsAdmin]

    def _get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return not_found_response(f'User #{pk} not found.')
        return success_response(data=AdminUserListSerializer(user).data)

    def patch(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return not_found_response(f'User #{pk} not found.')
        # Prevent admin from deactivating themselves
        if user.pk == request.user.pk and request.data.get('is_active') is False:
            return error_response(message='You cannot deactivate your own account.')
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message='Update failed.', errors=serializer.errors)
        user = serializer.save()
        return success_response(
            data=AdminUserListSerializer(user).data,
            message=f'User "{user.username}" updated.',
        )


# ─── Analytics Reports ─────────────────────────────────────────────────────────

class AdminScenarioReportView(APIView):
    """
    GET /api/v1/admin/reports/scenarios/
    Returns per-scenario analytics: attempts, completions, accuracy, XP.
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        scenarios = (
            Scenario.objects
            .select_related('category')
            .prefetch_related('simulation_sessions')
            .filter(is_active=True)
            .order_by('category__display_order', 'scenario_id')
        )

        report = []
        for scenario in scenarios:
            sessions = scenario.simulation_sessions.all()
            completed = sessions.filter(status=SimulationSession.Status.COMPLETED)
            abandoned = sessions.filter(status=SimulationSession.Status.ABANDONED)

            total_attempts = sessions.count()
            completion_count = completed.count()
            abandonment_rate = round(abandoned.count() / total_attempts * 100, 1) if total_attempts > 0 else 0.0

            acc_sessions = [s for s in completed if s.total_decisions > 0]
            avg_acc = round(
                sum(s.accuracy_percentage for s in acc_sessions) / len(acc_sessions), 1
            ) if acc_sessions else 0.0

            avg_xp = round(
                sum(s.total_xp_earned for s in completed) / completion_count, 1
            ) if completion_count > 0 else 0.0

            report.append({
                'scenario_id':       scenario.scenario_id,
                'scenario_title':    scenario.title,
                'category_name':     scenario.category.name,
                'difficulty':        scenario.difficulty,
                'total_attempts':    total_attempts,
                'completions':       completion_count,
                'abandonment_rate':  abandonment_rate,
                'average_accuracy':  avg_acc,
                'average_xp':        avg_xp,
            })

        return success_response(data=report, message=f'Analytics for {len(report)} scenarios.')


class AdminUserReportView(APIView):
    """
    GET /api/v1/admin/reports/users/
    Returns per-student summary for the admin reports page.
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        students = User.objects.filter(role='student', is_active=True).order_by('-total_xp')[:50]

        report = []
        for student in students:
            sessions = SimulationSession.objects.filter(student=student)
            completed = sessions.filter(status=SimulationSession.Status.COMPLETED)

            acc_sessions = [s for s in completed if s.total_decisions > 0]
            avg_acc = round(
                sum(s.accuracy_percentage for s in acc_sessions) / len(acc_sessions), 1
            ) if acc_sessions else 0.0

            report.append({
                'student_id':         student.pk,
                'username':           student.username,
                'full_name':          student.full_name,
                'email':              student.email,
                'total_xp':           student.total_xp,
                'completed_scenarios': completed.count(),
                'total_sessions':     sessions.count(),
                'average_accuracy':   avg_acc,
                'date_joined':        student.date_joined,
                'last_login':         student.last_login,
            })

        return success_response(data=report, message=f'Report for {len(report)} students.')
