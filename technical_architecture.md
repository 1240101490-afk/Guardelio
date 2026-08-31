# Guardelio — Complete Technical Architecture
## Phase 2: Architecture Design · All Six Agents

> **Status**: Architecture Design Phase — No code generated  
> **Builds on**: Phase 1 Implementation Plan (approved)  
> **Purpose**: Finalize every architectural decision before database design and scenario implementation begins

---

# AGENT 1 — System Architect
## Software Architecture, Layers, Flows & Standards

---

## 1.1 Architectural Pattern: Layered Client–Server

Guardelio follows a **three-tier layered architecture** with a clear separation between Presentation, Application, and Data layers. This was chosen because:

- It maps directly to the React + Django + MySQL stack
- Each layer can be developed, tested, and modified independently
- Students and reviewers can understand the architecture at a glance
- It avoids over-engineering while remaining fully scalable

```
╔══════════════════════════════════════════════════════════════════╗
║              TIER 1 — PRESENTATION (React.js)                   ║
║  Student UI │ Admin UI │ Simulation Engine UI │ Auth Pages       ║
╚══════════════════════════╦═══════════════════════════════════════╝
                           ║  HTTPS / REST API / JSON + JWT
╔══════════════════════════╩═══════════════════════════════════════╗
║              TIER 2 — APPLICATION (Django REST)                  ║
║   ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────────┐  ║
║   │   Auth   │ │ Scenarios │ │ Progress │ │  Admin / Reports │  ║
║   │  Module  │ │  Module   │ │  Module  │ │     Module       │  ║
║   └──────────┘ └───────────┘ └──────────┘ └──────────────────┘  ║
║             Business Logic │ Service Layer │ Validators           ║
╚══════════════════════════╦═══════════════════════════════════════╝
                           ║  Django ORM
╔══════════════════════════╩═══════════════════════════════════════╗
║              TIER 3 — DATA (MySQL)                              ║
║   Users │ Categories │ Scenarios │ Steps │ Sessions │ Badges    ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why REST over GraphQL?**
REST is simpler to implement, easier to test with Postman, and more appropriate for a FYP scope. GraphQL would add unnecessary complexity.

**Why Django REST Framework?**
Django offers the fastest path from model to API in Python, has excellent JWT library support, and is well-documented for university projects.

---

## 1.2 Application Layers (Backend)

Each backend Django app is internally organized into the following layers. This ensures no business logic leaks into views and no data logic leaks into serializers.

```
Request → URL Router
             ↓
         View / ViewSet        (HTTP handling only — no business logic)
             ↓
         Serializer            (validation, input/output shape)
             ↓
         Service Layer         (all business logic lives here)
             ↓
         Repository / ORM      (database queries only)
             ↓
         Model                 (schema definition only)
             ↓
         Database (MySQL)
```

| Layer | Responsibility | Must NOT Do |
|---|---|---|
| View/ViewSet | Parse request, call service, return response | Contain business logic |
| Serializer | Validate data, serialize/deserialize | Call services or write to DB directly |
| Service | Orchestrate business rules, XP, badges | Directly access `request` object |
| Model | Define schema, basic model methods | Business logic, complex queries |

---

## 1.3 Module Breakdown

| Module | Owned By | Purpose |
|---|---|---|
| **Authentication** | accounts app | Register, login, JWT refresh, user profile |
| **Dashboard** | Frontend page | Student home, summary widgets |
| **Categories** | scenarios app | Browse incident categories |
| **Scenarios** | scenarios app | Scenario listing, overview, metadata |
| **Simulation Engine** | progress app | Session management, step sequencing |
| **Decision Engine** | progress app | Decision processing, XP award, branching |
| **Results** | progress app | Completion data, session summary |
| **Progress Tracking** | progress app | Historical data, XP totals |
| **Profile** | accounts app | Student profile view |
| **Admin** | admin endpoints | All content and user management |
| **Reports** | reports app | Admin analytics |

---

## 1.4 Folder Organization

```
guardelio/
│
├── backend/                            ← Django project root
│   ├── config/                         ← Project-level configuration
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 ← Shared settings
│   │   │   ├── development.py          ← Dev overrides (DEBUG=True, etc.)
│   │   │   └── production.py           ← Prod overrides
│   │   ├── urls.py                     ← Root URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── apps/
│   │   ├── accounts/                   ← Auth module
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py             ← Auth business logic
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   ├── scenarios/                  ← Content module
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── admin.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   ├── progress/                   ← Simulation & tracking module
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── simulation_service.py
│   │   │   │   ├── xp_service.py
│   │   │   │   └── badge_service.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   └── reports/                    ← Admin reporting module
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   ├── core/                           ← Shared utilities
│   │   ├── __init__.py
│   │   ├── permissions.py              ← IsStudent, IsAdmin permission classes
│   │   ├── exceptions.py              ← Custom exception handler
│   │   ├── pagination.py
│   │   └── utils.py
│   │
│   ├── fixtures/
│   │   └── initial_scenarios.json     ← Seed data
│   │
│   ├── management/
│   │   └── commands/
│   │       └── seed_scenarios.py
│   │
│   ├── .env.example
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/                           ← React project root
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   └── src/
│       ├── api/                        ← All backend communication
│       │   ├── axiosInstance.js        ← Base Axios config + interceptors
│       │   ├── authService.js
│       │   ├── categoryService.js
│       │   ├── scenarioService.js
│       │   ├── simulationService.js
│       │   ├── progressService.js
│       │   └── adminService.js
│       │
│       ├── assets/
│       │   ├── icons/
│       │   └── images/
│       │
│       ├── components/
│       │   ├── common/                 ← Reusable primitives
│       │   │   ├── Button.jsx
│       │   │   ├── Card.jsx
│       │   │   ├── Modal.jsx
│       │   │   ├── Badge.jsx
│       │   │   ├── Loader.jsx
│       │   │   ├── Alert.jsx
│       │   │   └── ProgressBar.jsx
│       │   │
│       │   ├── layout/
│       │   │   ├── StudentLayout.jsx
│       │   │   ├── AdminLayout.jsx
│       │   │   ├── PublicLayout.jsx
│       │   │   ├── Navbar.jsx
│       │   │   ├── Sidebar.jsx
│       │   │   └── Footer.jsx
│       │   │
│       │   └── simulation/             ← Simulation-specific components
│       │       ├── NISTPhaseBar.jsx
│       │       ├── SituationPanel.jsx
│       │       ├── DecisionPanel.jsx
│       │       ├── FeedbackModal.jsx
│       │       └── ResultsSummary.jsx
│       │
│       ├── context/
│       │   ├── AuthContext.jsx
│       │   └── SimulationContext.jsx
│       │
│       ├── hooks/
│       │   ├── useAuth.js
│       │   ├── useSimulation.js
│       │   └── useFetch.js
│       │
│       ├── pages/
│       │   ├── auth/
│       │   │   ├── LoginPage.jsx
│       │   │   └── RegisterPage.jsx
│       │   ├── dashboard/
│       │   │   └── StudentDashboard.jsx
│       │   ├── categories/
│       │   │   ├── CategoriesPage.jsx
│       │   │   └── CategoryDetailPage.jsx
│       │   ├── scenarios/
│       │   │   └── ScenarioOverviewPage.jsx
│       │   ├── simulation/
│       │   │   ├── SimulationPage.jsx
│       │   │   └── CompletionPage.jsx
│       │   ├── progress/
│       │   │   └── ProgressPage.jsx
│       │   ├── profile/
│       │   │   └── ProfilePage.jsx
│       │   └── admin/
│       │       ├── AdminDashboard.jsx
│       │       ├── ManageCategoriesPage.jsx
│       │       ├── ManageScenariosPage.jsx
│       │       ├── ManageStepsPage.jsx
│       │       ├── ManageOptionsPage.jsx
│       │       ├── ManageUsersPage.jsx
│       │       └── ReportsPage.jsx
│       │
│       ├── routes/
│       │   ├── AppRouter.jsx
│       │   ├── StudentRoute.jsx        ← Protected route for students
│       │   └── AdminRoute.jsx          ← Protected route for admins
│       │
│       ├── utils/
│       │   ├── constants.js
│       │   ├── validators.js
│       │   └── formatters.js
│       │
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
├── docs/                               ← Project documentation
│   ├── README.md
│   ├── API_DOCS.md
│   ├── SCHEMA.md
│   ├── USER_GUIDE.md
│   └── ADMIN_GUIDE.md
│
├── .gitignore
└── README.md
```

---

## 1.5 Naming Conventions

| Context | Convention | Example |
|---|---|---|
| Python files/variables | `snake_case` | `simulation_service.py`, `xp_awarded` |
| Python classes | `PascalCase` | `SimulationSession`, `BadgeService` |
| Django URL names | `kebab-case` | `/api/v1/scenarios/` |
| React components | `PascalCase` | `NISTPhaseBar.jsx`, `FeedbackModal.jsx` |
| React hooks | `camelCase` with `use` prefix | `useSimulation`, `useAuth` |
| React pages | `PascalCase` + `Page` suffix | `SimulationPage.jsx` |
| JS variables/functions | `camelCase` | `fetchScenarios()`, `sessionId` |
| CSS classes | Tailwind utility classes (no custom names) | |
| Database columns | `snake_case` | `total_xp`, `created_at` |
| API endpoints | `kebab-case`, plural nouns | `/api/v1/simulation-sessions/` |
| Environment variables | `UPPER_SNAKE_CASE` | `DB_PASSWORD`, `SECRET_KEY` |
| Git branches | `type/agent-N-description` | `feature/agent3-simulation-api` |

---

## 1.6 Authentication Flow

```
                    STUDENT/ADMIN
                         │
                    ┌────▼────┐
                    │  Login  │  POST /api/v1/auth/login/
                    └────┬────┘
                         │  { access_token (15min), refresh_token (7d), user }
                         │
              ┌──────────▼──────────────┐
              │   Frontend stores:      │
              │   access_token → memory │
              │   refresh_token → cookie│
              │   user info → context   │
              └──────────┬──────────────┘
                         │
              ┌──────────▼──────────────┐
              │  Every API request:     │
              │  Authorization: Bearer  │
              │  <access_token>         │
              └──────────┬──────────────┘
                         │
              ┌──────────▼──────────────┐
              │  Token expired (401)?   │
              │  Auto-call /auth/refresh│
              │  Get new access_token   │
              └──────────┬──────────────┘
                         │
              ┌──────────▼──────────────┐
              │  Refresh also expired?  │
              │  Force logout → /login  │
              └─────────────────────────┘
```

---

## 1.7 Navigation Flow

### Student Flow
```
Landing Page (/)
      │
      ├──→ Register (/register) ─→ Login
      └──→ Login (/login)
                  │
                  ▼
         Student Dashboard (/dashboard)
           │           │
           ▼           ▼
      Categories    Progress (/progress)
      (/categories)    │
           │           └──→ Badges, History
           ▼
   Category Detail (/categories/:slug)
           │
           ▼
   Scenario Overview (/scenarios/:id)
   [Title, Difficulty, Duration, XP Reward, NIST Phases]
           │
       [Begin Simulation]
           │
           ▼
   Simulation Page (/simulation/:sessionId)
   [NIST Phase Bar → Situation → Decision Options]
           │
       [Submit Decision]
           │
           ▼
   Feedback Modal (inline)
   [✅/❌ + Educational Explanation + XP Earned]
           │
       [Continue]
           │
           ▼
   Next Step (loops back to Simulation Page)
           │
   [Final Step Reached]
           │
           ▼
   Completion Page (/simulation/:sessionId/complete)
   [Session XP, Accuracy %, New Badges, Key Decisions Summary]
           │
       [Return to Dashboard]
           │
           ▼
   Student Dashboard
```

### Admin Flow
```
Admin Login (/login with role=admin)
      │
      ▼
Admin Dashboard (/admin)
[Total Users, Sessions Today, Completions, XP Distributed]
      │
      ├──→ Manage Categories (/admin/categories)
      │         └──→ Create / Edit / Deactivate
      │
      ├──→ Manage Scenarios (/admin/scenarios)
      │         └──→ Create / Edit / Deactivate
      │                   └──→ Manage Steps (/admin/scenarios/:id/steps)
      │                             └──→ Manage Options (/admin/steps/:id/options)
      │
      ├──→ Manage Users (/admin/users)
      │         └──→ View Profile / Deactivate
      │
      └──→ Reports (/admin/reports)
                └──→ Scenario Stats / User Stats
```

---

## 1.8 Development Roadmap

| Phase | Week | Focus |
|---|---|---|
| **Phase 1: Foundation** | Week 1–2 | Project scaffolding, auth, base layouts |
| **Phase 2: Content Layer** | Week 3–4 | Category/Scenario models, public APIs, browse UI |
| **Phase 3: Simulation Engine** | Week 5–6 | Session management, decision engine, simulation UI |
| **Phase 4: Progress & Admin** | Week 7 | XP, badges, progress page, full admin portal |
| **Phase 5: QA & Polish** | Week 8 | Seeding, testing, documentation, final polish |

---

---

# AGENT 2 — Database & Scenario Designer
## Complete Database Architecture

---

## 2.1 Entity Inventory

| Entity | Table Name | Description |
|---|---|---|
| User | `accounts_user` | Students and admins |
| Category | `scenarios_category` | Incident type groupings |
| Scenario | `scenarios_scenario` | An individual simulation |
| ScenarioStep | `scenarios_scenariostep` | A single step within a scenario |
| DecisionOption | `scenarios_decisionoption` | A selectable choice on a decision step |
| SimulationSession | `progress_simulationsession` | A student's active/completed run of a scenario |
| StudentStepResponse | `progress_studentstepresponse` | Records each choice made per step per session |
| Badge | `progress_badge` | Badge definitions |
| UserBadge | `progress_userbadge` | Awards (user ↔ badge junction) |

**Total: 9 entities** — lean and purpose-built.

---

## 2.2 Entity Relationship Diagram (Textual)

```
accounts_user
    │
    ├──< progress_simulationsession >── scenarios_scenario ──< scenarios_category
    │               │
    │               └──< progress_studentstepresponse >── scenarios_scenariostep
    │                                                            │
    │                                                   < scenarios_decisionoption
    │                                                   (next_step FK → scenariostep)
    │
    └──< progress_userbadge >── progress_badge

Legend:  ──< = one-to-many   >──< = many-to-many via junction
```

---

## 2.3 Entity Definitions

### Entity 1: `accounts_user`

**Purpose**: Stores all system users (both student and admin roles).  
**Extends**: Django's `AbstractUser` (inherits username, email, password, is_active, date_joined).

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| username | VARCHAR(150) | UNIQUE, NOT NULL | |
| email | VARCHAR(254) | UNIQUE, NOT NULL | |
| password | VARCHAR(128) | NOT NULL | Bcrypt hashed |
| first_name | VARCHAR(150) | | |
| last_name | VARCHAR(150) | | |
| role | ENUM | NOT NULL, DEFAULT 'student' | Values: student, admin |
| total_xp | INT | NOT NULL, DEFAULT 0 | Running lifetime total |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft disable |
| date_joined | DATETIME | AUTO | |

**Why no separate Profile table?** For FYP scope, embedding profile fields directly on User avoids an unnecessary join on every profile request. Easily separable later if needed.

---

### Entity 2: `scenarios_category`

**Purpose**: Groups scenarios into named cybersecurity incident types.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| name | VARCHAR(100) | NOT NULL, UNIQUE | e.g., "Phishing Attack Response" |
| slug | VARCHAR(120) | NOT NULL, UNIQUE | URL-safe, e.g., "phishing-attack" |
| description | TEXT | NOT NULL | Student-visible summary |
| icon_name | VARCHAR(50) | | Icon identifier for UI |
| display_order | INT | NOT NULL, DEFAULT 0 | Controls card sort on frontend |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft delete |
| created_at | DATETIME | AUTO | |

---

### Entity 3: `scenarios_scenario`

**Purpose**: Defines a complete learnable incident simulation.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| category | FK → Category | NOT NULL, ON DELETE RESTRICT | |
| title | VARCHAR(200) | NOT NULL | |
| slug | VARCHAR(220) | NOT NULL, UNIQUE | |
| overview | TEXT | NOT NULL | Pre-simulation student briefing |
| difficulty | ENUM | NOT NULL | Values: beginner, intermediate, advanced |
| estimated_duration_minutes | INT | NOT NULL, DEFAULT 15 | |
| xp_reward | INT | NOT NULL, DEFAULT 50 | Completion bonus |
| nist_phases_covered | JSON | | Array of phase strings |
| version | INT | NOT NULL, DEFAULT 1 | Incremented on content edit |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft delete |
| created_at | DATETIME | AUTO | |
| updated_at | DATETIME | AUTO | |

---

### Entity 4: `scenarios_scenariostep`

**Purpose**: A single unit within a scenario. Can be informational, a decision point, or a quiz.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| scenario | FK → Scenario | NOT NULL, ON DELETE CASCADE | |
| step_number | INT | NOT NULL | Ordering within scenario |
| title | VARCHAR(200) | NOT NULL | Short step heading |
| situation_text | TEXT | NOT NULL | The scenario narrative shown to student |
| nist_phase | ENUM | NOT NULL | preparation / detection / containment / eradication / recovery / post_incident |
| step_type | ENUM | NOT NULL | info / decision / quiz |
| is_final_step | BOOLEAN | NOT NULL, DEFAULT FALSE | Triggers session completion |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

**Composite unique constraint**: (`scenario`, `step_number`) — no duplicate step numbers within a scenario.

---

### Entity 5: `scenarios_decisionoption`

**Purpose**: A selectable answer for a `decision` or `quiz` step. Includes branching logic.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| step | FK → ScenarioStep | NOT NULL, ON DELETE CASCADE | |
| option_text | VARCHAR(500) | NOT NULL | The choice shown to student |
| is_correct | BOOLEAN | NOT NULL, DEFAULT FALSE | |
| xp_awarded | INT | NOT NULL, DEFAULT 0 | 0 for wrong, >0 for correct |
| feedback_text | TEXT | NOT NULL | Educational explanation shown post-choice |
| consequence_type | ENUM | NOT NULL | positive / negative / neutral |
| next_step | FK → ScenarioStep | NULLABLE | NULL = advance to step_number+1 |
| display_order | INT | NOT NULL, DEFAULT 0 | Option sort order |

**Why nullable `next_step`?** For linear scenarios, `next_step=NULL` means "go to next step by order." For branching scenarios, an admin sets a specific target step without writing code.

---

### Entity 6: `progress_simulationsession`

**Purpose**: Tracks one student's attempt at one scenario. Persists state across page refreshes.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| student | FK → User | NOT NULL, ON DELETE CASCADE | |
| scenario | FK → Scenario | NOT NULL, ON DELETE RESTRICT | |
| scenario_version | INT | NOT NULL | Snapshot of version at start time |
| status | ENUM | NOT NULL, DEFAULT 'in_progress' | in_progress / completed / abandoned |
| current_step | FK → ScenarioStep | NULLABLE | NULL when completed |
| total_xp_earned | INT | NOT NULL, DEFAULT 0 | Running total for this session |
| correct_decisions | INT | NOT NULL, DEFAULT 0 | |
| total_decisions | INT | NOT NULL, DEFAULT 0 | |
| started_at | DATETIME | AUTO | |
| completed_at | DATETIME | NULLABLE | Set when status=completed |

**Unique together**: (`student`, `scenario`) with `status=in_progress` — a student can only have one active session per scenario at a time.

---

### Entity 7: `progress_studentstepresponse`

**Purpose**: Immutable audit log of every decision a student made within a session.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| session | FK → SimulationSession | NOT NULL, ON DELETE CASCADE | |
| step | FK → ScenarioStep | NOT NULL | |
| chosen_option | FK → DecisionOption | NULLABLE | NULL for info steps (no choice) |
| responded_at | DATETIME | AUTO | |

**Why immutable?** These records are the source of truth for reports, accuracy scores, and result pages. They must never be modified after creation.

---

### Entity 8: `progress_badge`

**Purpose**: Defines available badges and their earning criteria.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| name | VARCHAR(100) | NOT NULL, UNIQUE | e.g., "Cyber Sentinel" |
| description | TEXT | NOT NULL | |
| badge_type | ENUM | NOT NULL | bronze / silver / gold |
| criteria_type | ENUM | NOT NULL | xp_threshold / completion_count / perfect_score |
| criteria_value | INT | NOT NULL | The threshold number |
| icon_name | VARCHAR(50) | | |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | |

---

### Entity 9: `progress_userbadge`

**Purpose**: Junction table recording which badges each user has earned.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | |
| user | FK → User | NOT NULL, ON DELETE CASCADE | |
| badge | FK → Badge | NOT NULL | |
| earned_at | DATETIME | AUTO | |

**Unique together**: (`user`, `badge`) — a badge can only be earned once per user.

---

## 2.4 Normalization Analysis

| NF | Status | Notes |
|---|---|---|
| 1NF | ✅ | All fields are atomic. JSON column for `nist_phases_covered` is intentional and documented |
| 2NF | ✅ | No partial dependencies on composite keys |
| 3NF | ✅ | No transitive dependencies. XP total on User is a computed-cache (acceptable trade-off for query performance) |
| BCNF | ✅ | All determinants are candidate keys |

**The `total_xp` denormalization on `User`**: Keeping a running total on the user row avoids an expensive `SUM(xp_awarded)` across all sessions on every profile load. This is an intentional, documented trade-off — updated atomically after every step response.

---

## 2.5 Indexing Strategy

| Table | Index | Type | Reason |
|---|---|---|---|
| `accounts_user` | email, username | UNIQUE | Auth lookup |
| `scenarios_category` | slug | UNIQUE | URL routing |
| `scenarios_scenario` | slug, category_id | UNIQUE/INDEX | URL routing, filtering |
| `scenarios_scenariostep` | (scenario_id, step_number) | COMPOSITE UNIQUE | Step ordering |
| `scenarios_decisionoption` | step_id | INDEX | Option lookup by step |
| `progress_simulationsession` | (student_id, scenario_id, status) | COMPOSITE INDEX | Active session lookup |
| `progress_userbadge` | (user_id, badge_id) | COMPOSITE UNIQUE | Badge deduplication |

---

## 2.6 Future Scalability Provisions

| Concern | Provision |
|---|---|
| More scenario types | `step_type` ENUM is extensible |
| More badge criteria | `criteria_type` ENUM is extensible |
| Branching scenarios | `next_step` FK already supports full branching |
| Content versioning | `scenario.version` + `session.scenario_version` already in place |
| Soft deletes everywhere | `is_active` on Category, Scenario, Step — history never broken |
| Multiple attempts | No unique constraint preventing a student from re-doing a completed scenario |

---

---

# AGENT 3 — Backend Architect
## REST API Design, Service Layers & Standards

---

## 3.1 API Design Principles

1. **RESTful Resources**: All endpoints represent nouns (resources), not verbs
2. **Versioned from Day 1**: All endpoints prefixed `/api/v1/`
3. **Consistent Response Envelope**: Every response follows the same wrapper shape
4. **HTTP Semantics**: Correct use of GET, POST, PUT, PATCH, DELETE
5. **Stateless**: No server-side session state — JWT provides identity on every request

---

## 3.2 Standard Response Envelope

Every API response follows this shape. This makes frontend error handling consistent.

```
Success Response:
{
    "success": true,
    "data": { ... },
    "message": "Operation completed successfully"
}

Error Response:
{
    "success": false,
    "data": null,
    "message": "Validation failed",
    "errors": {
        "email": ["This field is required."],
        "password": ["Must be at least 8 characters."]
    }
}

Paginated Response:
{
    "success": true,
    "data": {
        "count": 24,
        "next": "/api/v1/scenarios/?page=2",
        "previous": null,
        "results": [ ... ]
    }
}
```

---

## 3.3 HTTP Status Codes Used

| Code | Meaning | When Used |
|---|---|---|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (new resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Valid token, wrong role |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate (e.g., email already registered) |
| 500 | Internal Server Error | Unhandled exception |

---

## 3.4 Complete REST API Blueprint

### Authentication Module — `/api/v1/auth/`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register/` | No | Create new student account |
| POST | `/api/v1/auth/login/` | No | Authenticate, receive tokens |
| POST | `/api/v1/auth/refresh/` | No (refresh token) | Get new access token |
| POST | `/api/v1/auth/logout/` | Yes | Blacklist refresh token |
| GET | `/api/v1/auth/me/` | Yes | Get current user info |
| PATCH | `/api/v1/auth/me/` | Yes | Update profile (name, password) |

---

### Categories Module — `/api/v1/categories/`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/api/v1/categories/` | Yes | Any | List all active categories |
| GET | `/api/v1/categories/:slug/` | Yes | Any | Get category + its scenarios |
| POST | `/api/v1/categories/` | Yes | Admin | Create category |
| PUT | `/api/v1/categories/:id/` | Yes | Admin | Update category |
| PATCH | `/api/v1/categories/:id/` | Yes | Admin | Partial update |
| DELETE | `/api/v1/categories/:id/` | Yes | Admin | Soft deactivate |

---

### Scenarios Module — `/api/v1/scenarios/`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/api/v1/scenarios/` | Yes | Any | List active scenarios (with filter) |
| GET | `/api/v1/scenarios/:id/` | Yes | Any | Get scenario detail + steps overview |
| POST | `/api/v1/scenarios/` | Yes | Admin | Create scenario |
| PUT | `/api/v1/scenarios/:id/` | Yes | Admin | Update scenario |
| DELETE | `/api/v1/scenarios/:id/` | Yes | Admin | Soft deactivate |
| GET | `/api/v1/scenarios/:id/steps/` | Yes | Admin | List all steps for scenario |
| POST | `/api/v1/scenarios/:id/steps/` | Yes | Admin | Add step to scenario |
| PUT | `/api/v1/steps/:id/` | Yes | Admin | Update step |
| DELETE | `/api/v1/steps/:id/` | Yes | Admin | Soft deactivate step |
| GET | `/api/v1/steps/:id/options/` | Yes | Admin | List options for step |
| POST | `/api/v1/steps/:id/options/` | Yes | Admin | Add option to step |
| PUT | `/api/v1/options/:id/` | Yes | Admin | Update option |
| DELETE | `/api/v1/options/:id/` | Yes | Admin | Delete option |

---

### Simulation Module — `/api/v1/simulation/`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| POST | `/api/v1/simulation/start/` | Yes | Student | Start a new session for a scenario |
| GET | `/api/v1/simulation/:sessionId/` | Yes | Student | Get current session state |
| POST | `/api/v1/simulation/:sessionId/respond/` | Yes | Student | Submit a decision for current step |
| GET | `/api/v1/simulation/:sessionId/result/` | Yes | Student | Get completed session summary |

**Body for `/start/`**: `{ "scenario_id": 3 }`  
**Body for `/respond/`**: `{ "option_id": 12 }` OR `{ "step_id": 7 }` (for info steps, no option needed)

---

### Progress Module — `/api/v1/progress/`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/api/v1/progress/` | Yes | Student | Get student's XP, sessions, badges |
| GET | `/api/v1/progress/sessions/` | Yes | Student | List all completed sessions |
| GET | `/api/v1/progress/badges/` | Yes | Student | List all earned badges |

---

### Admin Module — `/api/v1/admin/`

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/api/v1/admin/stats/` | Yes | Admin | Dashboard stats |
| GET | `/api/v1/admin/users/` | Yes | Admin | List all users |
| GET | `/api/v1/admin/users/:id/` | Yes | Admin | Get user detail |
| PATCH | `/api/v1/admin/users/:id/` | Yes | Admin | Activate/deactivate user |
| GET | `/api/v1/admin/reports/scenarios/` | Yes | Admin | Per-scenario analytics |
| GET | `/api/v1/admin/reports/users/` | Yes | Admin | Per-user analytics |

---

## 3.5 Service Layer Architecture

Each Django app exposes a service module. Views call services; services call models. No business logic in views or serializers.

### `accounts/services.py`
- `register_user(validated_data)` → creates user, returns user object
- `get_user_profile(user_id)` → returns user + XP + badge count
- `update_user_profile(user, validated_data)` → updates allowed fields

### `progress/services/simulation_service.py`
- `start_simulation(student, scenario_id)` → validates no active session, creates SimulationSession, returns first step
- `process_step_response(session, option_id=None, step_id=None)` → records response, calls XP service, advances step, checks for completion
- `get_session_result(session_id, student)` → aggregates session data for result page

### `progress/services/xp_service.py`
- `award_xp(user, amount)` → atomically increments user.total_xp
- `award_completion_bonus(user, scenario)` → awards scenario.xp_reward on completion

### `progress/services/badge_service.py`
- `check_and_award_badges(user)` → called after every session completion; compares user stats against all badge criteria; awards any newly earned badges

---

## 3.6 Error Handling Strategy

Centralized in `core/exceptions.py`. A single custom exception handler is registered in Django settings and converts all exceptions to the standard envelope.

```
Custom Exception Types (defined in core/exceptions.py):
  - GuardelioValidationError (400)
  - GuardelioAuthenticationError (401)
  - GuardelioPermissionError (403)
  - GuardelioNotFoundError (404)
  - GuardelioConflictError (409)
```

Any unhandled Django or Python exception falls through to a generic 500 handler that logs the error and returns a sanitized message to the client (never a stack trace in production).

---

## 3.7 Validation Strategy

| Layer | Validation Type |
|---|---|
| Serializer | Field-level: required, type, length, format |
| Service | Business-level: "can this student start a new session?", "does this step belong to this session?" |
| Model | Database-level: unique constraints, NOT NULL |

Never rely on only one layer. Defense in depth.

---

## 3.8 Authentication Strategy

- **Library**: `djangorestframework-simplejwt`
- **Access Token**: 15 minute lifetime, sent in `Authorization: Bearer` header
- **Refresh Token**: 7 day lifetime, stored in `httpOnly` cookie (prevents XSS access)
- **Blacklisting**: SimpleJWT's token blacklist app enabled — logout invalidates refresh tokens
- **Role Enforcement**: Custom `IsStudent` and `IsAdmin` permission classes in `core/permissions.py`

---

---

# AGENT 4 — Frontend Architect
## React Routing, Components, State & UI Architecture

---

## 4.1 Routing Structure

All routes defined in `src/routes/AppRouter.jsx` using React Router v6.

```
/                           → LandingPage (public)
/login                      → LoginPage (public)
/register                   → RegisterPage (public)

[StudentRoute wrapper — requires role=student]
/dashboard                  → StudentDashboard
/categories                 → CategoriesPage
/categories/:slug           → CategoryDetailPage
/scenarios/:id              → ScenarioOverviewPage
/simulation/:sessionId      → SimulationPage
/simulation/:sessionId/complete → CompletionPage
/progress                   → ProgressPage
/profile                    → ProfilePage

[AdminRoute wrapper — requires role=admin]
/admin                      → AdminDashboard
/admin/categories           → ManageCategoriesPage
/admin/scenarios            → ManageScenariosPage
/admin/scenarios/:id/steps  → ManageStepsPage
/admin/steps/:id/options    → ManageOptionsPage
/admin/users                → ManageUsersPage
/admin/reports              → ReportsPage

* (catch-all)               → NotFoundPage
```

**Route Guard Logic**:
- `StudentRoute`: Checks `AuthContext.user.role === 'student'`. Redirects to `/login` if not authenticated.
- `AdminRoute`: Checks `AuthContext.user.role === 'admin'`. Redirects to `/login` if not authenticated or wrong role.

---

## 4.2 Component Hierarchy

```
App.jsx
├── AuthContext.Provider
│   └── SimulationContext.Provider
│       └── AppRouter
│           │
│           ├── PublicLayout
│           │   ├── LandingPage
│           │   ├── LoginPage         → [LoginForm]
│           │   └── RegisterPage      → [RegisterForm]
│           │
│           ├── StudentLayout
│           │   ├── Navbar            → [XPCounter] [UserAvatar]
│           │   │
│           │   ├── StudentDashboard
│           │   │   ├── WelcomeBanner
│           │   │   ├── QuickStats    → [StatCard ×3]
│           │   │   └── RecentActivity → [SessionCard ×N]
│           │   │
│           │   ├── CategoriesPage
│           │   │   └── CategoryCard ×N
│           │   │
│           │   ├── CategoryDetailPage
│           │   │   ├── CategoryHeader
│           │   │   └── ScenarioCard ×N → [DifficultyBadge] [XPLabel]
│           │   │
│           │   ├── ScenarioOverviewPage
│           │   │   ├── ScenarioMeta  → [DifficultyBadge] [DurationLabel] [XPLabel]
│           │   │   ├── NISTPhasesList
│           │   │   └── BeginButton
│           │   │
│           │   ├── SimulationPage
│           │   │   ├── NISTPhaseBar  (visual phase indicator)
│           │   │   ├── SituationPanel → [StepTitle] [NarrativeText]
│           │   │   ├── DecisionPanel  → [OptionButton ×N]
│           │   │   └── FeedbackModal  → [ResultIcon] [FeedbackText] [XPGained] [ContinueButton]
│           │   │
│           │   ├── CompletionPage
│           │   │   ├── ResultsSummary → [TotalXP] [AccuracyRing] [TimeTaken]
│           │   │   ├── NewBadges      → [BadgeCard ×N]
│           │   │   └── DecisionReview → [StepResult ×N]
│           │   │
│           │   ├── ProgressPage
│           │   │   ├── XPProgressBar
│           │   │   ├── BadgeGrid     → [BadgeCard ×N]
│           │   │   └── HistoryList   → [CompletedSessionRow ×N]
│           │   │
│           │   └── ProfilePage
│           │       └── [ProfileCard] [EditForm]
│           │
│           └── AdminLayout
│               ├── AdminSidebar
│               │
│               ├── AdminDashboard  → [StatWidget ×4]
│               ├── ManageCategoriesPage → [DataTable] [CategoryForm Modal]
│               ├── ManageScenariosPage  → [DataTable] [ScenarioForm Modal]
│               ├── ManageStepsPage      → [StepList] [StepForm Modal]
│               ├── ManageOptionsPage    → [OptionList] [OptionForm Modal]
│               ├── ManageUsersPage      → [DataTable]
│               └── ReportsPage          → [ReportTable ×2]
```

---

## 4.3 Layout System

| Layout | Used By | Contains |
|---|---|---|
| `PublicLayout` | Landing, Login, Register | Minimal header, centered content |
| `StudentLayout` | All student pages | Navbar with XP counter + sidebar-free wide layout |
| `AdminLayout` | All admin pages | Sidebar navigation + content area |

Each layout wraps a React Router `<Outlet />` — pages slot into the layout automatically via nested routes.

---

## 4.4 State Management Strategy

**No Redux**. React Context + hooks are sufficient for this scope.

| Store | Location | What It Holds |
|---|---|---|
| `AuthContext` | Global | `user` object, `accessToken`, `login()`, `logout()`, `isAuthenticated` |
| `SimulationContext` | Simulation scope | `sessionId`, `currentStep`, `sessionXP`, `phaseHistory` |
| Local state (`useState`) | Per component | Form inputs, modal open/close, loading states |

**Data Fetching Strategy**: Custom `useFetch` hook wraps Axios calls with loading/error state. For frequently-accessed, cacheable data (categories, scenario list), data is fetched once on mount and held in local component state.

---

## 4.5 API Communication Layer

```
src/api/axiosInstance.js
  └── Base URL: process.env.REACT_APP_API_URL
  └── Request Interceptor: Attaches Authorization: Bearer <accessToken>
  └── Response Interceptor:
        On 401 → call /auth/refresh/ → retry original request
        On 403 → redirect to /login
        On 500 → show global error toast

src/api/authService.js       → login(), register(), logout(), getMe()
src/api/categoryService.js   → getCategories(), getCategoryBySlug()
src/api/scenarioService.js   → getScenarios(), getScenarioById()
src/api/simulationService.js → startSession(), respondToStep(), getResult()
src/api/progressService.js   → getProgress(), getSessions(), getBadges()
src/api/adminService.js      → all admin CRUD + stats + reports
```

Each service module exports plain async functions. Components call services via custom hooks.

---

## 4.6 Shared Components (Design System)

| Component | Props | Purpose |
|---|---|---|
| `Button` | variant (primary/secondary/danger), size, disabled, loading | All clickable actions |
| `Card` | children, className | Consistent card container |
| `Modal` | isOpen, onClose, title, children | Feedback modal, form modal |
| `Badge` | type (bronze/silver/gold/difficulty) | Visual label chips |
| `Loader` | fullPage, size | Spinner for loading states |
| `Alert` | type (success/error/info), message | Inline notifications |
| `ProgressBar` | current, max, label | XP bar |
| `DataTable` | columns, data, actions | Admin CRUD tables |

All shared components live in `src/components/common/` and are imported everywhere. No inline styles — Tailwind classes only.

---

## 4.7 Tailwind Configuration & Design Tokens

```
Design System:
  Colors:
    --primary:    #3B5BDB  (Slate Blue — CTAs, active states)
    --secondary:  #0F9B8E  (Teal — correct answers, success)
    --danger:     #DC2626  (Red — wrong answers, warnings)
    --surface:    #1E2A3A  (Dark card backgrounds)
    --background: #111827  (Page background)
    --text-primary: #F1F5F9 (Main text)
    --text-muted:   #94A3B8 (Secondary text)

  Typography:
    Font: Inter (via Google Fonts)
    H1: text-3xl font-bold
    H2: text-2xl font-semibold
    Body: text-base font-normal leading-relaxed

  Spacing: Tailwind default scale (consistent 4px base)
  Borders: rounded-xl (cards), rounded-lg (buttons), rounded-full (badges)
  Shadows: shadow-md on cards, shadow-lg on modals
```

---

---

# AGENT 5 — Admin Architecture
## Administrator Module Design

---

## 5.1 Admin Module Philosophy

The admin module is a **content management system**, not a separate application. It is served by the same React frontend with role-gated routes and communicates with dedicated admin-prefixed API endpoints.

**Core Principle**: An administrator must be able to create a complete new cybersecurity scenario (with all steps, decision options, and educational feedback) without ever touching the application code.

---

## 5.2 Admin Capabilities Matrix

| Module | List | Create | Edit | Delete/Deactivate |
|---|---|---|---|---|
| Categories | ✅ | ✅ | ✅ | ✅ (soft) |
| Scenarios | ✅ | ✅ | ✅ | ✅ (soft) |
| Scenario Steps | ✅ | ✅ | ✅ | ✅ (soft) |
| Decision Options | ✅ | ✅ | ✅ | ✅ (hard) |
| Users | ✅ | ❌ | Activate/Deactivate only | ❌ |
| Reports | ✅ (read-only) | — | — | — |
| Badges | ✅ | ✅ | ✅ | ✅ |

---

## 5.3 Content Creation Workflow (No Code Required)

```
Admin creates a new scenario without code:

Step 1: Create/select a Category
        (Admin Dashboard → Manage Categories → + New)

Step 2: Create a Scenario under that Category
        (Manage Scenarios → + New)
        [Title, Overview, Difficulty, Duration, XP Reward, NIST Phases]

Step 3: Add Scenario Steps in order
        (Scenario row → Manage Steps → + Add Step)
        [Step Number, Title, Situation Text, NIST Phase, Step Type, Is Final?]

Step 4: For each decision/quiz step, add Decision Options
        (Step row → Manage Options → + Add Option)
        [Option Text, Is Correct, XP Awarded, Feedback Text,
         Consequence Type, Next Step (dropdown of existing steps)]

Step 5: Activate the Scenario
        (Toggle is_active = true)
        → Scenario is immediately available to students
```

---

## 5.4 Admin Dashboard Widgets

| Widget | Data Source | Description |
|---|---|---|
| Total Registered Students | `accounts_user` count | |
| Active Simulations Today | `progress_simulationsession` where started_at=today | |
| Completions This Week | Sessions with status=completed | |
| Total XP Distributed | SUM(total_xp_earned) across all sessions | |
| Most Attempted Scenario | GROUP BY scenario, ORDER BY count DESC | |
| Lowest Accuracy Scenario | AVG(correct/total) per scenario, ASC | |

---

## 5.5 Reports Design

### Report 1: Scenario Performance Report
- Columns: Scenario Name | Total Attempts | Completion Rate | Avg Accuracy | Avg XP Earned
- Filter: By category, by date range
- Use: Identify which scenarios are too easy or too hard

### Report 2: User Progress Report
- Columns: Username | Total XP | Scenarios Completed | Badges Earned | Last Active
- Filter: By role, by activity date
- Use: Monitor student engagement

### Report 3: Decision Point Analysis *(future enhancement)*
- Shows which decision options students choose most and least
- Identifies commonly missed steps

---

## 5.6 Admin UI Design Patterns

| Pattern | Implementation |
|---|---|
| CRUD Tables | `DataTable` component with Edit/Delete action buttons per row |
| Create/Edit Forms | Modal dialog with form inside (no separate page navigation) |
| Confirmation Dialogs | Modal for any delete/deactivate — prevent accidental data loss |
| Breadcrumb Navigation | Scenario → Steps → Options (nested content is clear) |
| Inline Validation | Form shows errors without page reload |
| Status Indicators | Active/Inactive chip on every row |

---

---

# AGENT 6 — Integration Architect
## Frontend ↔ Backend Integration, Auth Lifecycle & Deployment

---

## 6.1 Integration Architecture

```
FRONTEND (React, port 3000)          BACKEND (Django, port 8000)
        │                                       │
        │   HTTP Request                        │
        │   GET /api/v1/categories/             │
        │   Authorization: Bearer <token>  ───► │
        │                                       │  django-cors-headers
        │                                       │  validates origin
        │                                       │
        │                                  ◄─── │  JSON Response
        │   { success: true, data: [...] }       │
        │                                       │
```

**CORS Configuration (development)**:
- `ALLOWED_ORIGINS = ["http://localhost:3000"]`
- Credentials allowed: `True` (for cookie-based refresh tokens)
- Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS

**CORS Configuration (production)**:
- `ALLOWED_ORIGINS` = actual deployed frontend domain only

---

## 6.2 Complete Auth Lifecycle

```
1. REGISTER
   Frontend: POST /api/v1/auth/register/ { username, email, password }
   Backend:  Validates → creates user → returns 201 { user }
   Frontend: Auto-redirect to /login

2. LOGIN
   Frontend: POST /api/v1/auth/login/ { username, password }
   Backend:  Validates → returns { access_token, refresh_token, user }
   Frontend: Stores access_token in memory (AuthContext)
             Stores refresh_token in httpOnly cookie
             Stores user in AuthContext
             Redirects to /dashboard

3. AUTHENTICATED REQUEST
   Frontend: Every Axios request → interceptor adds Authorization header
   Backend:  JWT middleware validates token → passes user to view

4. ACCESS TOKEN EXPIRY (15 min)
   Frontend: Receives 401 response
             Axios interceptor calls POST /api/v1/auth/refresh/
             Backend returns new access_token
             Interceptor retries original request with new token
             (Student sees nothing — transparent refresh)

5. REFRESH TOKEN EXPIRY (7 days)
   Frontend: /auth/refresh/ returns 401
             AuthContext.logout() called
             user, token cleared from context
             Redirect to /login with "Session expired" message

6. LOGOUT
   Frontend: POST /api/v1/auth/logout/ { refresh_token }
   Backend:  Blacklists refresh_token
   Frontend: Clears context and cookie → redirect to /login
```

---

## 6.3 Simulation API Lifecycle

```
1. START SESSION
   POST /api/v1/simulation/start/ { scenario_id: 3 }
   ← { session_id: 47, current_step: { id, title, situation_text,
       step_type, nist_phase, options: [...] } }
   Frontend: Stores session_id in SimulationContext
             Renders SimulationPage with first step

2. INFO STEP (no decision)
   POST /api/v1/simulation/47/respond/ { step_id: 12 }
   ← { next_step: { ... }, session_status: "in_progress", xp_earned: 0 }
   Frontend: Renders next step directly (no modal needed for info steps)

3. DECISION STEP
   POST /api/v1/simulation/47/respond/ { option_id: 22 }
   ← { feedback: { is_correct, feedback_text, xp_earned, consequence_type },
       next_step: { ... } or null,
       session_status: "in_progress" | "completed" }
   Frontend: Opens FeedbackModal with feedback data
             On [Continue]: renders next_step or redirects to /complete

4. SESSION COMPLETE
   GET /api/v1/simulation/47/result/
   ← { total_xp_earned, correct_decisions, total_decisions,
       accuracy_percent, new_badges: [...], step_responses: [...] }
   Frontend: Renders CompletionPage
```

---

## 6.4 Local Development Workflow

```
ENVIRONMENT SETUP (one-time):

Backend:
  1. Install Python 3.11+, MySQL Server
  2. Create database: guardelio_db
  3. cd backend/
  4. python -m venv venv && venv\Scripts\activate
  5. pip install -r requirements.txt
  6. Copy .env.example → .env (fill in credentials)
  7. python manage.py migrate
  8. python manage.py seed_scenarios
  9. python manage.py createsuperuser

Frontend:
  1. Install Node.js 18+
  2. cd frontend/
  3. npm install
  4. Copy .env.example → .env

DAILY DEVELOPMENT:

Terminal 1 (Backend):
  cd backend/ && venv\Scripts\activate
  python manage.py runserver

Terminal 2 (Frontend):
  cd frontend/
  npm start

API Testing:
  Open Postman → Import Guardelio.postman_collection.json
```

---

## 6.5 Environment Variables Plan

```
backend/.env:
  DJANGO_SECRET_KEY=
  DJANGO_DEBUG=True
  DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
  DJANGO_SETTINGS_MODULE=config.settings.development
  DB_NAME=guardelio_db
  DB_USER=root
  DB_PASSWORD=
  DB_HOST=127.0.0.1
  DB_PORT=3306
  CORS_ALLOWED_ORIGINS=http://localhost:3000
  JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
  JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

frontend/.env:
  REACT_APP_API_URL=http://localhost:8000/api/v1
  REACT_APP_APP_NAME=Guardelio
```

---

## 6.6 Integration Testing Strategy

Testing is organized in three tiers:

### Tier 1: Backend Unit Tests (Django TestCase)
- Model validation (constraints, unique together, defaults)
- Service layer logic (XP award, badge check, session start logic)
- Serializer validation (required fields, type checks)

### Tier 2: Backend API Tests (DRF APITestCase)
- Every endpoint: correct status code, response shape
- Auth edge cases: no token, expired token, wrong role
- Simulation flow: start → respond → complete (full sequence)

### Tier 3: Integration Testing (Manual + Postman)
| Flow | Steps |
|---|---|
| Full Student Journey | Register → Login → Browse → Start Sim → Complete → View Progress |
| Admin Content Workflow | Login → Create Category → Create Scenario → Add Steps → Add Options → Activate |
| Session Recovery | Start sim → close browser → reopen → resume from current_step |
| Role Enforcement | Try accessing /admin/users/ as student → expect 403 |
| Token Refresh | Wait 15 min → make request → verify transparent refresh |

---

## 6.7 Deployment Structure (Local/Development)

```
┌─────────────────────────────────────────────────────┐
│              Developer Machine                       │
│                                                      │
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │  React Dev      │    │  Django Dev Server      │  │
│  │  localhost:3000 │◄──►│  localhost:8000         │  │
│  │  npm start      │    │  manage.py runserver    │  │
│  └─────────────────┘    └───────────┬─────────────┘  │
│                                     │                 │
│                          ┌──────────▼──────────┐      │
│                          │   MySQL Server      │      │
│                          │   localhost:3306    │      │
│                          │   guardelio_db      │      │
│                          └─────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

---

# CROSS-AGENT ARCHITECTURE DECISIONS

## Summary of Key Decisions & Rationale

| Decision | Rationale |
|---|---|
| Django + DRF | Fast model-to-API development, excellent JWT support, FYP-appropriate |
| React + Tailwind | Component reusability, utility-first styling, avoids CSS sprawl |
| MySQL | Relational data with foreign keys; well-understood by most students |
| JWT (not sessions) | Stateless, scalable, works naturally with React SPA |
| Access token in memory | XSS resistant; not stored in localStorage |
| Refresh token in httpOnly cookie | XSS cannot steal it; CSRF protected by SameSite=Lax |
| Soft deletes | Historical student session data never breaks from content changes |
| Service layer pattern | Business logic testable independently of HTTP layer |
| No Redux | Context + hooks sufficient for this scope; less boilerplate |
| Dark mode UI | Appropriate for cybersecurity; premium feel |
| `next_step` FK on DecisionOption | Enables branching without code changes |
| Seed command | Admin portal immediately usable from day one |
| API versioning from day one | `/api/v1/` — no breaking changes when v2 comes |

---

## Agent Sign-Off — Architecture Phase Complete

| Agent | Domain | Status |
|---|---|---|
| Agent 1 | System Architecture, Layers, Flows | ✅ Complete |
| Agent 2 | Database Entities, Relationships, Normalization | ✅ Complete |
| Agent 3 | REST API Blueprint, Service Layers, Error Handling | ✅ Complete |
| Agent 4 | Frontend Routing, Components, State, Design System | ✅ Complete |
| Agent 5 | Admin Module, Content Workflow, Reports | ✅ Complete |
| Agent 6 | Integration, Auth Lifecycle, Deployment, Testing Plan | ✅ Complete |

---

> **Next Phase**: Cybersecurity Simulation & Scenario Architecture Design  
> All agents are fully aligned. Implementation begins only after scenario architecture is approved.
