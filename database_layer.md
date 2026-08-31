# Guardelio — Database Layer Documentation
## Phase 4: Complete Database Design & Django Models

> **Status**: ✅ Database layer implemented — models ready for migration  
> **Location**: `backend/` directory  
> **Stack**: MySQL + Django ORM + Django REST Framework

---

## Agent 1 — Complete Entity Relationship Diagram

### 11 Database Tables

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GUARDELIO DATABASE (MySQL)                          │
│                                                                          │
│  ┌──────────────────┐         ┌──────────────────┐                      │
│  │  accounts_user   │────1:1──│accounts_student  │                      │
│  │  ───────────     │         │profile           │                      │
│  │  PK id           │         │  ─────────────   │                      │
│  │  username        │         │  PK id           │                      │
│  │  email (UNIQUE)  │         │  FK user_id      │                      │
│  │  password        │         │  institution     │                      │
│  │  role            │         │  bio             │                      │
│  │  total_xp        │         │  avatar_name     │                      │
│  │  is_active       │         │  last_active     │                      │
│  └──────────┬───────┘         └──────────────────┘                      │
│             │                                                            │
│             │ 1:N (sessions)       1:N (xp history)   1:N (badges)      │
│             │                                                            │
│  ┌──────────▼───────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ progress_simulation      │  │progress_xp   │  │progress_userbadge │  │
│  │ session                  │  │history       │  │  ─────────────    │  │
│  │  ─────────────────────   │  │  ─────────   │  │  PK id            │  │
│  │  PK id                   │  │  PK id       │  │  FK user_id       │  │
│  │  FK student_id           │  │  FK user_id  │  │  FK badge_id      │  │
│  │  FK scenario_id          │  │  FK session  │  │  earned_at        │  │
│  │  FK current_step_id      │  │  amount      │  └────────┬──────────┘  │
│  │  scenario_version        │  │  type        │           │             │
│  │  status                  │  │  balance_    │  ┌────────▼──────────┐  │
│  │  total_xp_earned         │  │  after       │  │  progress_badge   │  │
│  │  correct_decisions       │  └──────────────┘  │  ─────────────    │  │
│  │  total_decisions         │                    │  PK id            │  │
│  │  started_at              │                    │  name (UNIQUE)    │  │
│  │  completed_at            │                    │  badge_type       │  │
│  └──────────┬───────────────┘                    │  criteria_type    │  │
│             │                                    │  criteria_value   │  │
│             │ 1:N                                │  FK category_id   │  │
│             │                                    └───────────────────┘  │
│  ┌──────────▼────────────────┐                                          │
│  │ progress_sessiondecision  │                                          │
│  │  ──────────────────────   │                                          │
│  │  PK id                    │                                          │
│  │  FK session_id            │                                          │
│  │  FK step_id               │                                          │
│  │  FK chosen_option_id      │                                          │
│  │  xp_earned_at_step        │                                          │
│  │  responded_at             │                                          │
│  └───────────────────────────┘                                          │
│                                                                          │
│  ┌─────────────────┐  1:N  ┌──────────────────┐  1:N                   │
│  │scenarios_category│──────│scenarios_scenario │──────────┐             │
│  │  ─────────────  │       │  ─────────────── │           │             │
│  │  PK id          │       │  PK id           │           │             │
│  │  name (UNIQUE)  │       │  FK category_id  │  ┌────────▼──────────┐  │
│  │  slug (UNIQUE)  │       │  scenario_id     │  │ scenarios_learning │  │
│  │  description    │       │  title           │  │ objective         │  │
│  │  short_summary  │       │  slug            │  │  ──────────────   │  │
│  │  icon_name      │       │  student_role    │  │  PK id            │  │
│  │  color_theme    │       │  overview        │  │  FK scenario_id   │  │
│  │  display_order  │       │  difficulty      │  │  objective_text   │  │
│  │  is_active      │       │  xp_bonus        │  │  order            │  │
│  └─────────────────┘       │  version         │  └───────────────────┘  │
│                            │  is_active       │                          │
│                            └──────────┬───────┘                          │
│                                       │ 1:N                              │
│                            ┌──────────▼──────────────────┐              │
│                            │  scenarios_scenariostep      │              │
│                            │  ───────────────────────     │              │
│                            │  PK id                       │              │
│                            │  FK scenario_id              │              │
│                            │  step_number                 │              │
│                            │  title                       │              │
│                            │  situation_text              │              │
│                            │  nist_phase                  │              │
│                            │  step_type                   │              │
│                            │  is_final_step               │              │
│                            │  is_active                   │              │
│                            └──────────┬──────────────────┘              │
│                                       │ 1:N                              │
│                            ┌──────────▼──────────────────┐              │
│                            │  scenarios_decisionoption    │              │
│                            │  ────────────────────────    │              │
│                            │  PK id                       │              │
│                            │  FK step_id                  │              │
│                            │  option_text                 │              │
│                            │  is_correct                  │              │
│                            │  xp_awarded                  │              │
│                            │  feedback_text               │              │
│                            │  consequence_type            │              │
│                            │  FK next_step_id ──────────┐ │              │
│                            │  display_order              │ │              │
│                            └─────────────────────────────┼─┘              │
│                              (self-ref → ScenarioStep)  │                │
└─────────────────────────────────────────────────────────┘                │
```

---

## Agent 2 — Django Models Summary

### Files Created

| File | Models Defined | Lines |
|---|---|---|
| [`accounts/models.py`](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/accounts/models.py) | `User`, `StudentProfile` | ~115 |
| [`scenarios/models.py`](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/scenarios/models.py) | `Category`, `Scenario`, `LearningObjective`, `ScenarioStep`, `DecisionOption` | ~350 |
| [`progress/models.py`](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/progress/models.py) | `Badge`, `UserBadge`, `SimulationSession`, `SessionDecision`, `XPHistory` | ~320 |

### Key Design Decisions

| Decision | Rationale |
|---|---|
| `User.total_xp` denormalized | Avoids `SUM()` query on every navbar render. Updated atomically by XPService |
| `LearningObjective` as separate table | Enables per-objective admin editing vs. unmaintainable JSON blob |
| `DecisionOption.next_step` self-FK | Full branching without schema or code changes |
| `SimulationSession.current_step` FK | Enables browser-refresh resume — student never loses progress |
| `SessionDecision` immutable audit log | Source of truth for results, reports, badge criteria; never modified |
| `XPHistory` separate table | Full XP audit trail; supports future breakdown/timeline features |
| Soft delete (`is_active`) | Historical sessions never break when content is updated/removed |
| `scenario_version` snapshot | Detects content drift in in-progress sessions |

---

## Agent 3 — Dynamic Scenario Engine: Data Flow

```
No scenario content is hardcoded anywhere in the application.

Content hierarchy in database:

Category (6 rows seeded)
    └── Scenario (30 rows — 5 per category)
            ├── LearningObjective (3–4 rows per scenario)
            └── ScenarioStep (5–7 rows per scenario)
                    └── DecisionOption (2–4 rows per decision step)
                            └── next_step FK → ScenarioStep (branching)

Simulation Engine reads:
    1. Session.current_step → fetch ScenarioStep row
    2. ScenarioStep.step_type → decide if decision panel shown
    3. ScenarioStep.options → fetch all DecisionOption rows
    4. Student selects option → create SessionDecision row
    5. chosen_option.next_step → determine next step
       (NULL = linear, FK = branching jump)
    6. chosen_option.is_final_step → trigger completion
    7. Service awards XP → updates Session + User.total_xp + XPHistory
    8. BadgeService.check_and_award_badges(user) → checks all criteria
```

---

## Agent 4 — User Progress: State Machine

```
SIMULATIONSESSION STATUS LIFECYCLE:

     [Student clicks Begin]
             │
             ▼
      ┌─────────────────┐
      │   IN_PROGRESS   │◄──── Page refresh resumes via
      │                 │      current_step FK
      └────────┬────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
  [is_final_step]  [Student gives up /
       │            admin action]
       │                │
       ▼                ▼
  ┌──────────┐    ┌───────────┐
  │ COMPLETED│    │ ABANDONED │
  └──────────┘    └───────────┘
        │
        ▼
  BadgeService.check_and_award_badges()
  XPService.award_completion_bonus()
  XPService.award_perfect_score_bonus() (if applicable)
```

---

## Agent 5 — Admin Capabilities (No Code Required)

All of the following are achievable through the Django Admin portal at `/django-admin/`:

| Action | Admin Model | Zero Code Required? |
|---|---|---|
| Create new category | `Category` | ✅ |
| Edit category icon/color | `Category` | ✅ |
| Create new scenario | `Scenario` | ✅ |
| Add learning objectives | `LearningObjective` (inline) | ✅ |
| Add steps to scenario | `ScenarioStep` (inline) | ✅ |
| Add decision options with feedback | `DecisionOption` (inline) | ✅ |
| Configure branching (next_step) | `DecisionOption.next_step` dropdown | ✅ |
| Set XP per decision | `DecisionOption.xp_awarded` | ✅ |
| Activate/deactivate content | `is_active` toggle | ✅ |
| Create new badges | `Badge` admin | ✅ |
| View student sessions | `SimulationSession` admin | ✅ |

---

## Agent 6 — Database Review Checklist

### Normalization Verification

| Normal Form | Status | Notes |
|---|---|---|
| 1NF | ✅ PASS | All atomic values. No repeating groups. |
| 2NF | ✅ PASS | No partial dependencies on composite keys. |
| 3NF | ✅ PASS | No transitive dependencies. |
| BCNF | ✅ PASS | All determinants are candidate keys. |

### Documented Denormalizations

| Field | Reason | Acceptable? |
|---|---|---|
| `User.total_xp` | Avoids SUM() on every page load | ✅ Yes — updated atomically |
| `SessionDecision.xp_earned_at_step` | Snapshot prevents retroactive XP changes affecting historical records | ✅ Yes — by design |
| `SimulationSession.scenario_version` | Snapshot for content drift detection | ✅ Yes — by design |

### Relationship Integrity Check

| Relationship | ON DELETE | Correct? |
|---|---|---|
| Category → Scenario | PROTECT | ✅ Cannot delete category with scenarios |
| Scenario → ScenarioStep | CASCADE | ✅ Steps deleted with scenario |
| ScenarioStep → DecisionOption | CASCADE | ✅ Options deleted with step |
| DecisionOption.next_step → ScenarioStep | SET_NULL | ✅ Branching nulled, not broken |
| User → SimulationSession | CASCADE | ✅ Sessions deleted if user deleted |
| Scenario → SimulationSession | PROTECT | ✅ Cannot delete scenario with sessions |
| SimulationSession → SessionDecision | CASCADE | ✅ Decisions deleted with session |
| User → UserBadge | CASCADE | ✅ Badge records deleted with user |
| User → XPHistory | CASCADE | ✅ History deleted with user |

### Index Review

| Table | Index | Purpose |
|---|---|---|
| `accounts_user` | `email` (UNIQUE), `username` (UNIQUE) | Auth lookups |
| `scenarios_category` | `slug` (UNIQUE) | URL routing |
| `scenarios_scenario` | `slug` (UNIQUE), `scenario_id` (UNIQUE), `difficulty`, `is_active` | Filtering |
| `scenarios_scenariostep` | `(scenario, step_number)` UNIQUE | Step ordering |
| `progress_simulationsession` | `(student, scenario, status)` composite | Active session lookup |
| `progress_userbadge` | `(user, badge)` UNIQUE | Badge deduplication |
| `progress_sessiondecision` | `(session, step)` UNIQUE | One response per step |

### Query Efficiency Assessment

| Common Query | Efficient? | How |
|---|---|---|
| Get active categories | ✅ | `is_active` indexed |
| Get scenarios by category+difficulty | ✅ | Both indexed |
| Find active session for student+scenario | ✅ | Composite index |
| Get all steps for a scenario (ordered) | ✅ | `step_number` ordering |
| Get XP for navbar display | ✅ | `User.total_xp` — single field read, no join |
| Get student badge count | ✅ | COUNT on `UserBadge` — small table |

---

## Migration Strategy

### Step 1: Create Database
```sql
CREATE DATABASE guardelio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 2: Run Migrations
```bash
cd backend/
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Fill in your MySQL credentials
python manage.py makemigrations accounts
python manage.py makemigrations scenarios
python manage.py makemigrations progress
python manage.py makemigrations reports
python manage.py migrate
```

### Step 3: Seed Data
```bash
python manage.py seed_guardelio
```

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
# Then set role='admin' in Django admin or shell
```

### Step 5: Start Server
```bash
python manage.py runserver
# Admin portal: http://localhost:8000/django-admin/
```

---

## Generated Files

| File | Purpose |
|---|---|
| [requirements.txt](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/requirements.txt) | Python dependencies |
| [config/settings/base.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/config/settings/base.py) | Shared Django settings |
| [config/settings/development.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/config/settings/development.py) | Dev environment settings |
| [config/urls.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/config/urls.py) | Root URL configuration |
| [core/exceptions.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/core/exceptions.py) | Global exception handler |
| [core/permissions.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/core/permissions.py) | IsStudent, IsAdmin, IsStudentOrAdmin |
| [core/pagination.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/core/pagination.py) | Standard paginated responses |
| [apps/accounts/models.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/accounts/models.py) | User, StudentProfile |
| [apps/accounts/signals.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/accounts/signals.py) | Auto-create StudentProfile on register |
| [apps/accounts/admin.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/accounts/admin.py) | User admin registration |
| [apps/scenarios/models.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/scenarios/models.py) | Category, Scenario, LearningObjective, ScenarioStep, DecisionOption |
| [apps/scenarios/admin.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/scenarios/admin.py) | Full content management admin |
| [apps/progress/models.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/progress/models.py) | Badge, UserBadge, SimulationSession, SessionDecision, XPHistory |
| [apps/progress/admin.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/progress/admin.py) | Progress and session admin |
| [apps/scenarios/management/commands/seed_guardelio.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/apps/scenarios/management/commands/seed_guardelio.py) | Seeds all 6 categories, 18 badges, S-MAL-01 complete scenario |
| [.env.example](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/.env.example) | Environment variable template |
| [manage.py](file:///c:/Users/Ahsan/OneDrive/Desktop/24-July-2026/backend/manage.py) | Django CLI entry point |

---

> **Next Phase (Prompt 5)**: REST API Implementation — serializers, views, URL routes, and business logic service layer for all endpoints.
