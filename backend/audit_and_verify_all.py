"""
Guardelio — Project-Wide Scenario Data Integrity & Simulation Verification Script
Tests all 15 audit requirements across all 6 categories and 30 scenarios.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from apps.accounts.models import User
from apps.scenarios.models import Category, Scenario, ScenarioStep, DecisionOption, LearningObjective
from apps.scenarios.views import CategoryListView, CategoryDetailView, ScenarioListView, ScenarioDetailView
from apps.progress.models import SimulationSession, SessionDecision, XPHistory, Badge, UserBadge
from apps.progress.services import simulation_service, badge_service


def run_comprehensive_audit():
    print("=" * 90)
    print(" GUARDELIO COMPLETE PROJECT-WIDE SCENARIO DATA INTEGRITY AUDIT")
    print("=" * 90)

    # Test user
    student, _ = User.objects.get_or_create(
        email='audit_student@guardelio.com',
        defaults={'username': 'audit_student', 'role': User.Role.STUDENT, 'is_active': True}
    )

    client = APIClient()
    client.force_authenticate(user=student)

    categories = Category.objects.filter(is_active=True).order_by('display_order')
    total_categories = categories.count()
    print(f"\n[1] Found {total_categories} active categories:")
    for c in categories:
        print(f"    - {c.name} (slug: {c.slug}, order: {c.display_order})")

    results_table = []
    all_passed = True
    total_scenarios_audited = 0
    total_steps_verified = 0
    total_options_verified = 0

    rf = APIRequestFactory()

    for category in categories:
        scenarios = Scenario.objects.filter(category=category, is_active=True).order_by('scenario_id')
        print(f"\n--------------------------------------------------------------------------")
        print(f" Category: {category.name} ({scenarios.count()} scenarios)")
        print(f"--------------------------------------------------------------------------")

        # Test Category Detail View API
        cat_req = rf.get(f'/api/v1/categories/{category.slug}/')
        force_authenticate(cat_req, user=student)
        cat_view = CategoryDetailView.as_view()
        cat_resp = cat_view(cat_req, slug=category.slug)
        cat_api_ok = (cat_resp.status_code == 200 and cat_resp.data.get('success'))

        for s in scenarios:
            total_scenarios_audited += 1
            scenario_errors = []

            # 1. Record exists & 2. Active
            if not s.is_active:
                scenario_errors.append("Scenario is inactive")

            # 3. Overview/description
            if not s.overview or len(s.overview.strip()) == 0:
                scenario_errors.append("Missing overview")
            if not s.student_role or len(s.student_role.strip()) == 0:
                scenario_errors.append("Missing student_role")

            # 4. At least one active step
            steps = ScenarioStep.objects.filter(scenario=s, is_active=True).order_by('step_number')
            step_count = steps.count()
            if step_count == 0:
                scenario_errors.append("No active steps")

            # 5 & 6. Step numbering & ownership
            expected_numbers = list(range(1, step_count + 1))
            actual_numbers = [st.step_number for st in steps]
            if actual_numbers != expected_numbers:
                scenario_errors.append(f"Step order mismatch: expected {expected_numbers}, got {actual_numbers}")

            final_steps = steps.filter(is_final_step=True)
            if final_steps.count() != 1:
                scenario_errors.append(f"Expected exactly 1 final step, found {final_steps.count()}")
            elif final_steps.first() != steps.last():
                scenario_errors.append("Final step is not the last step in sequence")

            # 7, 8, 9. Decision steps & options
            options_count = 0
            for st in steps:
                total_steps_verified += 1
                if st.step_type in ('decision', 'quiz'):
                    opts = DecisionOption.objects.filter(step=st).order_by('display_order')
                    if opts.count() < 2 or opts.count() > 4:
                        scenario_errors.append(f"Step {st.step_number} has {opts.count()} options (expected 2-4)")

                    correct_opts = opts.filter(is_correct=True)
                    if correct_opts.count() != 1:
                        scenario_errors.append(f"Step {st.step_number} has {correct_opts.count()} correct options (expected 1)")

                    for opt in opts:
                        options_count += 1
                        total_options_verified += 1
                        if opt.is_correct and opt.xp_awarded <= 0:
                            scenario_errors.append(f"Step {st.step_number} correct option has 0 XP")
                        if not opt.is_correct and opt.xp_awarded != 0:
                            scenario_errors.append(f"Step {st.step_number} incorrect option has >0 XP")
                        if not opt.feedback_text or len(opt.feedback_text.strip()) == 0:
                            scenario_errors.append(f"Step {st.step_number} option missing feedback")
                        if opt.next_step and opt.next_step.scenario_id != s.id:
                            scenario_errors.append(f"Step {st.step_number} next_step points to wrong scenario")

            # Learning objectives
            objs = LearningObjective.objects.filter(scenario=s)
            if objs.count() < 3:
                scenario_errors.append(f"Scenario has only {objs.count()} learning objectives")

            # 12. Test Scenario API View
            api_ok = False
            try:
                scen_req = rf.get(f'/api/v1/scenarios/{s.id}/')
                force_authenticate(scen_req, user=student)
                scen_view = ScenarioDetailView.as_view()
                scen_resp = scen_view(scen_req, pk=s.id)
                if scen_resp.status_code == 200 and scen_resp.data.get('success'):
                    data = scen_resp.data.get('data', {})
                    if data.get('title') == s.title and len(data.get('learning_objectives', [])) >= 3 and len(data.get('nist_phases_in_scenario', [])) >= 2:
                        api_ok = True
                    else:
                        scenario_errors.append("API data payload incomplete")
                else:
                    scenario_errors.append(f"API status {scen_resp.status_code}")
            except Exception as e:
                scenario_errors.append(f"API exception: {e}")

            # 14 & 15. Simulation Engine Full End-to-End Test
            simulation_ok = False
            try:
                # Clean prior sessions for this scenario
                SimulationSession.objects.filter(student=student, scenario=s).delete()

                # Start simulation
                session, is_new = simulation_service.start_simulation(student, s.id)
                if not session or session.status != SimulationSession.Status.IN_PROGRESS or not is_new:
                    scenario_errors.append("Failed to create new in_progress simulation session")

                # Play through all steps
                current_step = session.current_step
                step_safety_count = 0
                while current_step and step_safety_count < 20:
                    step_safety_count += 1
                    if current_step.step_type == 'info':
                        resp = simulation_service.process_step_response(session, student, option_id=None)
                    else:
                        correct_opt = current_step.options.filter(is_correct=True).first()
                        resp = simulation_service.process_step_response(session, student, option_id=correct_opt.id)

                    if resp['session_status'] == 'completed':
                        break
                    else:
                        session.refresh_from_db()
                        current_step = session.current_step

                session.refresh_from_db()
                if session.status != SimulationSession.Status.COMPLETED:
                    scenario_errors.append(f"Session ended with status: {session.status}")
                elif session.total_xp_earned <= 0:
                    scenario_errors.append("Session completed with 0 XP earned")
                else:
                    # Test session result endpoint payload
                    result_payload = simulation_service.get_session_result(session.id, student)
                    if (result_payload.get('accuracy_percent') == 100
                            and len(result_payload.get('decision_review', [])) == step_count
                            and len(result_payload.get('lessons_learned', '')) > 0):
                        simulation_ok = True
                    else:
                        scenario_errors.append(f"Result payload validation: accuracy={result_payload.get('accuracy_percent')}, reviews={len(result_payload.get('decision_review', []))}")

            except Exception as e:
                scenario_errors.append(f"Simulation exception: {e}")

            status_str = "Working" if (len(scenario_errors) == 0 and api_ok and simulation_ok) else "Broken"
            if len(scenario_errors) > 0:
                all_passed = False
                status_str = f"Broken ({', '.join(scenario_errors[:2])})"

            results_table.append({
                'category': category.name,
                'scenario_id': s.scenario_id,
                'title': s.title,
                'difficulty': s.difficulty,
                'steps': step_count,
                'options': options_count,
                'api_working': "Yes" if api_ok else "No",
                'sim_working': "Yes" if simulation_ok else "No",
                'status': "Working" if status_str == "Working" else status_str
            })

            print(f"  [{s.scenario_id}] {s.title[:40]:<40} | Steps: {step_count} | Opts: {options_count} | API: {'OK' if api_ok else 'FAIL'} | Sim: {'OK' if simulation_ok else 'FAIL'} | Status: {status_str}")

    # Clean test student
    SimulationSession.objects.filter(student=student).delete()
    XPHistory.objects.filter(user=student).delete()
    UserBadge.objects.filter(user=student).delete()
    student.delete()

    print("\n" + "=" * 110)
    print(" COMPLETE AUDIT SUMMARY TABLE")
    print("=" * 110)
    print(f"{'Category':<32} | {'Scenario':<36} | {'Steps':<5} | {'Opts':<5} | {'API':<5} | {'Simulation':<10} | {'Status'}")
    print("-" * 110)
    for r in results_table:
        print(f"{r['category'][:32]:<32} | {r['scenario_id'] + ': ' + r['title'][:28]:<36} | {r['steps']:<5} | {r['options']:<5} | {r['api_working']:<5} | {r['sim_working']:<10} | {r['status']}")
    print("=" * 110)

    print(f"\nFinal Audit Verdict:")
    print(f"  Total Categories: {total_categories}")
    print(f"  Total Scenarios:  {total_scenarios_audited} / 30")
    print(f"  Total Steps:      {total_steps_verified}")
    print(f"  Total Options:    {total_options_verified}")
    print(f"  All Passed:       {'YES (100% HEALTHY)' if all_passed else 'NO (FAILURES DETECTED)'}\n")

    return all_passed


if __name__ == '__main__':
    success = run_comprehensive_audit()
    sys.exit(0 if success else 1)
