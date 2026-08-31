# Guardelio — Web-Based Security Incident Training & Simulation System
## Master Implementation Plan · Pre-Development Analysis

> **Status**: Planning Phase · Awaiting approval before any code is written  
> **Framework**: NIST SP 800-61 Incident Response  
> **Stack**: React + Tailwind · Django REST Framework · MySQL · JWT

---

## 1. Executive Summary

Guardelio is a university-level cybersecurity education platform where students practice incident response through branching, decision-based simulations aligned to the NIST SP 800-61 framework. The system is educational-first, not game-first — with lightweight gamification (XP + badges) to sustain motivation without becoming a distraction.

This document captures the combined analysis from all six agents. No code is written yet.

---

## 2. Agent 1 — System Architect: Architecture & Standards

### 2.1 High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React.js)                         │
│   Student Portal  │  Simulation Engine UI  │  Admin Dashboard      │
└────────────────────────────┬───────────────────────────────────────┘
                             │  HTTPS + JWT
┌────────────────────────────▼───────────────────────────────────────┐
│                       BACKEND (Django REST)                        │
│  Auth API │ Scenario API │ Progress API │ Admin API │ Badge API     │
└────────────────────────────┬───────────────────────────────────────┘
                             │  Django ORM
┌────────────────────────────▼───────────────────────────────────────┐
│                        DATABASE (MySQL)                            │
│  Users │ Categories │ Scenarios │ Steps │ Decisions │ Progress     │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Folder Structure

```
guardelio/
├── backend/                        # Django project root
│   ├── config/                     # Django settings, urls, wsgi
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/               # User auth, profiles
│   │   ├── scenarios/              # Categories, scenarios, steps, decisions
│   │   ├── progress/               # Student progress, XP, badges
│   │   └── reports/                # Admin reporting
│   ├── core/                       # Shared utilities, permissions, mixins
│   ├── requirements.txt
│   └── manage.py
│
└── frontend/                       # React project root
    ├── public/
    └── src/
        ├── api/                    # Axios instances & service modules
        ├── assets/                 # Icons, images, static files
        ├── components/             # Reusable UI components
        │   ├── common/             # Buttons, cards, modals, loaders
        │   ├── layout/             # Navbar, sidebar, footer
        │   └── simulation/         # Scenario cards, decision panels
        ├── pages/                  # Route-level page components
        │   ├── auth/               # Login, Register
        │   ├── dashboard/          # Student home
        │   ├── categories/         # Category browser
        │   ├── scenarios/          # Scenario overview + simulation
        │   ├── progress/           # Progress & badges
        │   └── admin/              # Admin portal pages
        ├── context/                # Auth context, simulation context
        ├── hooks/                  # Custom hooks
        ├── utils/                  # Helpers, constants, validators
        └── App.jsx
```

### 2.3 API Naming Conventions

| Resource | Endpoint Pattern |
|---|---|
| Auth | `/api/v1/auth/register/`, `/api/v1/auth/login/`, `/api/v1/auth/refresh/` |
| Categories | `/api/v1/categories/` |
| Scenarios | `/api/v1/scenarios/`, `/api/v1/scenarios/{id}/` |
| Simulation | `/api/v1/scenarios/{id}/start/`, `/api/v1/sessions/{id}/step/` |
| Progress | `/api/v1/progress/`, `/api/v1/progress/badges/` |
| Admin | `/api/v1/admin/users/`, `/api/v1/admin/reports/` |

### 2.4 Project Standards

- **HTTP Methods**: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE
- **Response Format**: `{ success, data, message, errors }`
- **Token Strategy**: Access token (15 min) + Refresh token (7 days), stored in `httpOnly` cookies or `localStorage` with XSS awareness
- **Naming**: `snake_case` in Python/DB, `camelCase` in JS, `PascalCase` for components
- **Git Branching**: `main` → `develop` → `feature/agent-N-feature-name`
- **Error Handling**: Centralized Django exception handler + React error boundary
- **Versioning**: API versioned as `/api/v1/` from day one

### 2.5 Architectural Improvements Identified

> [!IMPORTANT]
> These improvements are recommended over a naive implementation:

1. **Session-based Simulation State**: Rather than stateless step-by-step calls, introduce a `SimulationSession` model that persists a student's position in a scenario. This prevents progress loss on page refresh.
2. **Scenario Versioning**: Add a `version` field to Scenario so content updates don't corrupt in-progress sessions.
3. **Soft Delete Pattern**: Use `is_active` flags instead of hard deletes for Scenarios and Steps — preserves historical data for completed student sessions.
4. **Settings Split**: Separate `development.py` and `production.py` settings from day one. Avoids last-minute deployment scrambles.
5. **CORS from Day 1**: Configure `django-cors-headers` before any frontend integration to prevent wasted debugging time.

---

## 3. Agent 2 — Database & Scenario Designer

### 3.1 Entity Relationship Overview

```
User ──< SimulationSession >── Scenario
                 │
                 └──< StudentStepResponse >── ScenarioStep ──< DecisionOption
                                                   │
                                             (NIST Phase Tag)

User ──< Badge (earned)
Scenario ──< Category
```

### 3.2 Database Schema

#### `accounts_user` (extends AbstractUser)
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| username | VARCHAR(150) | Unique |
| email | VARCHAR(254) | Unique |
| password | VARCHAR(128) | Hashed |
| role | ENUM('student','admin') | Default: student |
| total_xp | INT | Default: 0 |
| date_joined | DATETIME | Auto |
| is_active | BOOLEAN | |

#### `scenarios_category`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| name | VARCHAR(100) | e.g., "Phishing Attack" |
| slug | VARCHAR(120) | URL-friendly |
| description | TEXT | |
| icon_name | VARCHAR(50) | Icon identifier |
| display_order | INT | Manual sort order |
| is_active | BOOLEAN | Soft delete |

#### `scenarios_scenario`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| category | FK → Category | |
| title | VARCHAR(200) | |
| slug | VARCHAR(220) | |
| overview | TEXT | Pre-simulation briefing |
| difficulty | ENUM('beginner','intermediate','advanced') | |
| estimated_duration | INT | Minutes |
| xp_reward | INT | On completion |
| nist_phases_covered | JSON | Array of phase tags |
| version | INT | Default: 1 |
| is_active | BOOLEAN | |
| created_at | DATETIME | |
| updated_at | DATETIME | |

#### `scenarios_scenariostep`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| scenario | FK → Scenario | |
| step_number | INT | Ordered sequence |
| title | VARCHAR(200) | |
| situation_text | TEXT | What the student reads |
| nist_phase | ENUM('preparation','detection','containment','eradication','recovery','post_incident') | |
| step_type | ENUM('info','decision','quiz') | |
| is_final_step | BOOLEAN | |

#### `scenarios_decisionoption`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| step | FK → ScenarioStep | |
| option_text | VARCHAR(500) | The choice shown to student |
| is_correct | BOOLEAN | |
| xp_awarded | INT | 0 if wrong, >0 if correct |
| feedback_text | TEXT | Educational explanation shown after choice |
| next_step | FK → ScenarioStep (nullable) | Branching logic |
| consequence_type | ENUM('positive','negative','neutral') | |

#### `progress_simulationsession`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| student | FK → User | |
| scenario | FK → Scenario | |
| scenario_version | INT | Snapshot at session start |
| status | ENUM('in_progress','completed','abandoned') | |
| current_step | FK → ScenarioStep | |
| total_xp_earned | INT | Running total |
| correct_decisions | INT | |
| total_decisions | INT | |
| started_at | DATETIME | |
| completed_at | DATETIME (nullable) | |

#### `progress_studentstepresponse`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| session | FK → SimulationSession | |
| step | FK → ScenarioStep | |
| chosen_option | FK → DecisionOption (nullable) | Null for info steps |
| responded_at | DATETIME | |

#### `progress_badge`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| name | VARCHAR(100) | e.g., "First Responder" |
| description | TEXT | |
| badge_type | ENUM('bronze','silver','gold') | |
| criteria_type | ENUM('xp_threshold','completion_count','perfect_score') | |
| criteria_value | INT | Threshold value |
| icon_name | VARCHAR(50) | |

#### `progress_userbadge`
| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| user | FK → User | |
| badge | FK → Badge | |
| earned_at | DATETIME | |

### 3.3 Cybersecurity Scenario Categories

| # | Category | Difficulty Range | Scenarios Planned |
|---|---|---|---|
| 1 | Phishing Attack Response | Beginner | 2 |
| 2 | Ransomware Incident | Intermediate | 2 |
| 3 | Insider Threat Detection | Intermediate | 1 |
| 4 | DDoS Attack Mitigation | Intermediate | 1 |
| 5 | Data Breach Response | Advanced | 2 |
| 6 | Malware Infection | Beginner | 1 |

**Total: 9 scenarios minimum for MVP**

### 3.4 Sample Scenario Structure — "Phishing Email Investigation"

```
Scenario: "Phishing Email Investigation"
Category: Phishing Attack Response
Difficulty: Beginner
XP Reward: 100

Step 1 [NIST: Detection] — type: info
  "Your SOC receives an alert. An employee reports receiving a
   suspicious email asking for VPN credentials..."

Step 2 [NIST: Detection] — type: decision
  Situation: "How do you verify if the email is malicious?"
  Options:
    A) "Ask the employee to click the link to check"
       → is_correct: false, xp: 0, consequence: negative
       → Feedback: "Never instruct users to click suspicious links.
                    This could trigger a credential harvest or malware."
       → next_step: Step 3 (negative path)
    B) "Analyze email headers and check sender domain reputation"
       → is_correct: true, xp: 25, consequence: positive
       → Feedback: "Correct. Header analysis and domain reputation
                    tools are the first safe step."
       → next_step: Step 3 (standard path)

Step 3 [NIST: Containment] — type: decision
  ...continues branching...

Step 5 [NIST: Post-Incident] — type: info, is_final_step: true
  "Debrief: Here is what happened, what you did well, and
   what could be improved..."
```

### 3.5 Badge Criteria

| Badge | Type | Criteria |
|---|---|---|
| First Responder | Bronze | Complete first scenario |
| Quick Learner | Bronze | Earn 200 XP |
| Incident Analyst | Silver | Complete 3 scenarios |
| Defender | Silver | Earn 500 XP |
| Cyber Sentinel | Gold | Complete all scenarios with ≥ 80% correct decisions |
| NIST Expert | Gold | Earn 1000 XP |

---

## 4. Agent 3 — Backend Developer: Django API Plan

### 4.1 Django App Structure

| App | Purpose |
|---|---|
| `accounts` | Custom User model, JWT auth, profile |
| `scenarios` | Category, Scenario, ScenarioStep, DecisionOption models + APIs |
| `progress` | SimulationSession, StudentStepResponse, Badge, UserBadge + XP engine |
| `reports` | Admin-only reporting views |
| `core` | Base serializers, permissions, exception handler |

### 4.2 Key Libraries

```
Django==4.2.x
djangorestframework==3.15.x
djangorestframework-simplejwt==5.3.x
django-cors-headers==4.x
mysqlclient==2.x
django-filter==23.x
Pillow==10.x  (if image upload needed)
python-decouple==3.x  (env vars)
```

### 4.3 Authentication Flow

```
Register → POST /api/v1/auth/register/
  ↓ returns: { user_id, username, email }

Login → POST /api/v1/auth/login/
  ↓ returns: { access_token, refresh_token, user }

Refresh → POST /api/v1/auth/refresh/
  ↓ accepts: { refresh_token }
  ↓ returns: { access_token }

All protected routes → Header: Authorization: Bearer <access_token>
```

### 4.4 Simulation Engine Logic

```
1. Student requests: POST /api/v1/scenarios/{id}/start/
   → Creates SimulationSession (status=in_progress, current_step=Step 1)
   → Returns: session_id, first step data

2. Student submits decision: POST /api/v1/sessions/{session_id}/step/
   → Body: { decision_option_id }
   → Creates StudentStepResponse record
   → Awards XP if correct
   → Updates session.current_step to next_step
   → Checks if new step is_final_step
   → If final: sets session.status=completed, triggers badge check
   → Returns: { feedback, xp_earned, next_step, session_status }

3. Badge Check (internal service, not exposed):
   → Runs after every session completion
   → Evaluates all badge criteria against student's updated stats
   → Awards any newly unlocked badges
```

### 4.5 XP Calculation Rules

- Each correct decision awards its `decisionoption.xp_awarded` directly
- Scenario completion bonus: `scenario.xp_reward` added on completion
- `user.total_xp` is updated atomically after each step
- No negative XP — wrong answers simply award 0

### 4.6 Permissions Matrix

| Endpoint | Student | Admin |
|---|---|---|
| Register / Login | ✅ | ✅ |
| Browse Categories | ✅ | ✅ |
| Browse Scenarios | ✅ | ✅ |
| Start Simulation | ✅ | ❌ |
| Submit Decision | ✅ | ❌ |
| View Own Progress | ✅ | ❌ |
| View All Users | ❌ | ✅ |
| Create/Edit Scenario | ❌ | ✅ |
| View Reports | ❌ | ✅ |

---

## 5. Agent 4 — Frontend Developer: React UI Plan

### 5.1 Page Map

| Route | Component | Access |
|---|---|---|
| `/` | Landing / Home | Public |
| `/register` | RegisterPage | Public |
| `/login` | LoginPage | Public |
| `/dashboard` | StudentDashboard | Student |
| `/categories` | CategoriesPage | Student |
| `/categories/:slug` | CategoryDetailPage | Student |
| `/scenarios/:id` | ScenarioOverviewPage | Student |
| `/simulation/:sessionId` | SimulationPage | Student |
| `/simulation/:sessionId/complete` | CompletionPage | Student |
| `/progress` | ProgressPage | Student |
| `/admin` | AdminDashboard | Admin |
| `/admin/scenarios` | AdminScenariosPage | Admin |
| `/admin/users` | AdminUsersPage | Admin |
| `/admin/reports` | AdminReportsPage | Admin |

### 5.2 Component Hierarchy

```
App
├── AuthContext (global auth state)
│
├── PublicLayout
│   ├── LandingPage
│   ├── LoginPage
│   └── RegisterPage
│
├── StudentLayout (requires auth: student)
│   ├── Navbar (logo, nav links, XP counter, avatar)
│   ├── StudentDashboard
│   │   ├── WelcomeBanner
│   │   ├── RecentActivity
│   │   └── ProgressSnapshot
│   ├── CategoriesPage → CategoryCard (×N)
│   ├── ScenarioOverviewPage (briefing + Start button)
│   ├── SimulationPage
│   │   ├── NISTPhaseIndicator (visual phase tracker)
│   │   ├── SituationPanel (scenario text)
│   │   ├── DecisionPanel (option buttons)
│   │   └── FeedbackModal (post-decision feedback)
│   ├── CompletionPage (XP earned, badges awarded, summary)
│   └── ProgressPage
│       ├── XPProgressBar
│       ├── BadgeGrid
│       └── CompletedScenariosList
│
└── AdminLayout (requires auth: admin)
    ├── AdminSidebar
    ├── AdminDashboard (stats overview)
    ├── AdminScenariosPage (CRUD)
    ├── AdminUsersPage
    └── AdminReportsPage
```

### 5.3 State Management Strategy

- **AuthContext**: JWT tokens, current user, login/logout actions
- **SimulationContext**: Active session ID, current step data, XP accumulated this session
- No Redux needed — React Context + `useState`/`useReducer` is sufficient for this scope
- **React Query** (optional but recommended): For data fetching, caching, and background sync of scenario data

### 5.4 Tailwind Design System

```
Color Palette:
  Primary:    Slate Blue     #3B5BDB  (main actions)
  Secondary:  Teal           #0F9B8E  (success, positive)
  Danger:     Red-600        #DC2626  (warnings, wrong answers)
  Neutral:    Slate-800/900  (dark backgrounds)
  Surface:    Slate-700      (cards)
  Text:       Slate-100      (primary text on dark)

Typography:
  Font Family: Inter (Google Fonts)
  Headings: font-semibold, tracking-tight
  Body: font-normal, leading-relaxed

Design Theme: Dark mode by default (appropriate for cybersecurity)
Borders: rounded-xl for cards, rounded-lg for buttons
Shadows: shadow-lg with subtle glow on active elements
```

### 5.5 Key UX Decisions

1. **NIST Phase Indicator**: A horizontal step tracker at the top of SimulationPage shows which phase the student is in (Preparation → Detection → Containment → ...). This makes the framework visible without being overwhelming.
2. **Feedback Modal**: After each decision, a modal slides in showing ✅/❌ icon, the feedback text, and XP earned. Student must acknowledge before proceeding.
3. **Scenario Overview Page**: Between category browsing and simulation start — shows scenario title, difficulty badge, estimated time, NIST phases covered, and XP reward. Student clicks "Begin Simulation" to proceed.
4. **Completion Page**: Shows total XP earned this session, accuracy percentage, any new badges unlocked, and a summary of key decisions.

---

## 6. Agent 5 — Admin & Content Management Plan

### 6.1 Admin Portal Features

| Feature | Description |
|---|---|
| **Dashboard** | Total users, active sessions, completions today, XP distributed |
| **Category Management** | Create, edit, reorder, activate/deactivate categories |
| **Scenario Management** | Create/edit scenarios with all metadata |
| **Step Builder** | Add/edit/reorder steps within a scenario |
| **Decision Editor** | Add decision options per step, set correct answer, write feedback, link next_step |
| **User Management** | View users, see their XP/badges, deactivate accounts |
| **Reports** | Per-scenario completion rates, average accuracy, most-missed decision points |

### 6.2 Admin-Specific API Endpoints

```
GET  /api/v1/admin/dashboard-stats/
GET  /api/v1/admin/users/
GET  /api/v1/admin/users/{id}/
PATCH /api/v1/admin/users/{id}/

GET  /api/v1/admin/scenarios/            (full detail including steps)
POST /api/v1/admin/scenarios/
PUT  /api/v1/admin/scenarios/{id}/
DELETE /api/v1/admin/scenarios/{id}/     (soft delete)

POST /api/v1/admin/scenarios/{id}/steps/
PUT  /api/v1/admin/steps/{id}/

POST /api/v1/admin/steps/{id}/options/
PUT  /api/v1/admin/options/{id}/

GET  /api/v1/admin/reports/scenarios/
GET  /api/v1/admin/reports/users/
```

### 6.3 Content Seeding Strategy

- Provide Django management command: `python manage.py seed_scenarios`
- Seed file in `backend/fixtures/initial_scenarios.json`
- Seeder loads all 9 planned scenarios with full step and decision data
- Admin can add more via the portal

---

## 7. Agent 6 — QA, Integration & Deployment Plan

### 7.1 Integration Checklist (Pre-Testing)

- [ ] CORS configured for `http://localhost:3000` in development
- [ ] JWT tokens correctly stored and sent with every protected request
- [ ] Axios instance configured with base URL + token interceptor + 401 auto-refresh
- [ ] Environment variables separated: `.env` for frontend, `.env` for backend (never committed to Git)

### 7.2 Testing Strategy

| Layer | What to Test | Tool |
|---|---|---|
| Backend Unit | Model methods, XP calculation, badge logic | Django TestCase |
| Backend API | Each endpoint: status codes, response shape, auth | DRF APITestCase / Postman |
| Frontend | Component rendering, form validation | React Testing Library |
| Integration | Full flow: Register → Browse → Simulate → Complete | Manual + Postman |
| Auth Edge Cases | Expired tokens, invalid credentials, role mismatch | Manual |

### 7.3 Postman Collection Plan

Organize into folders:
1. Auth (Register, Login, Refresh)
2. Categories & Scenarios (public)
3. Simulation Flow (protected)
4. Progress & Badges (protected)
5. Admin APIs (admin-only)

### 7.4 Local Deployment Steps

```
Backend:
  cd backend/
  python -m venv venv
  venv\Scripts\activate      (Windows)
  pip install -r requirements.txt
  cp .env.example .env        (fill in MySQL creds)
  python manage.py migrate
  python manage.py seed_scenarios
  python manage.py runserver

Frontend:
  cd frontend/
  npm install
  cp .env.example .env        (set REACT_APP_API_URL)
  npm start
```

### 7.5 Environment Variables

```
Backend (.env):
  SECRET_KEY=...
  DEBUG=True
  DB_NAME=guardelio_db
  DB_USER=root
  DB_PASSWORD=...
  DB_HOST=localhost
  DB_PORT=3306
  ALLOWED_ORIGINS=http://localhost:3000
  ACCESS_TOKEN_LIFETIME_MINUTES=15
  REFRESH_TOKEN_LIFETIME_DAYS=7

Frontend (.env):
  REACT_APP_API_URL=http://localhost:8000/api/v1
```

### 7.6 Final Documentation Artifacts

- `README.md` — Setup instructions, tech stack, team
- `API_DOCS.md` — All endpoints documented
- `SCHEMA.md` — Database ER description
- `USER_GUIDE.md` — Student walkthrough
- `ADMIN_GUIDE.md` — Admin portal guide

---

## 8. Cross-Agent Improvements & Risk Register

### 8.1 Identified Improvements Over Original Spec

| # | Area | Issue | Recommendation |
|---|---|---|---|
| 1 | Simulation State | No mechanism to resume interrupted simulation | Add `SimulationSession` with `current_step` FK |
| 2 | Content Safety | Deleting a scenario with active sessions breaks data | Use soft-delete (`is_active`) |
| 3 | Branching Logic | Linear steps can't represent branching | `next_step` FK on `DecisionOption` enables true branching |
| 4 | Feedback Delivery | Original spec doesn't specify when/how feedback appears | Feedback Modal after each decision (acknowledged, then continue) |
| 5 | Admin Usability | No seed data = empty admin portal on first run | Fixture + seed command for instant demo content |
| 6 | Token Storage | `localStorage` susceptible to XSS | Use `httpOnly` cookies for refresh token; access token in memory |
| 7 | NIST Visibility | Framework invisible to student | NISTPhaseIndicator component makes learning explicit |
| 8 | Scenario Versioning | Content updates corrupt in-progress sessions | `scenario_version` snapshot at session start |

### 8.2 Out of Scope (Explicitly Excluded)

- Real-time multiplayer or collaboration
- Leaderboards
- Email verification (deferred — not required for FYP)
- File upload for scenarios (text-based only for MVP)
- Payment or subscription system
- Mobile app

### 8.3 Potential Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Complex branching logic bugs | Medium | Validate `next_step` references in serializer; admin can preview step flow |
| MySQL connection issues on Windows | Medium | Document exact MySQL + mysqlclient setup steps |
| JWT token race conditions on refresh | Low | Implement single-flight refresh in Axios interceptor |
| Scope creep on admin portal | High | Strict feature freeze — admin portal is CRUD only, no analytics graphs for MVP |

---

## 9. Development Roadmap

### Phase 1 — Foundation (Week 1–2)
- [ ] Django project scaffolding, app structure, settings split
- [ ] Custom User model + JWT auth endpoints
- [ ] MySQL connection and base migration
- [ ] React project scaffolding with Tailwind
- [ ] AuthContext, Axios instance, protected routes
- [ ] Login/Register pages

### Phase 2 — Core Data & APIs (Week 3–4)
- [ ] Category, Scenario, ScenarioStep, DecisionOption models + migrations
- [ ] Admin serializers and CRUD endpoints for content
- [ ] Public read-only endpoints for categories and scenarios
- [ ] Category browser and Scenario Overview pages (React)

### Phase 3 — Simulation Engine (Week 5–6)
- [ ] SimulationSession, StudentStepResponse models
- [ ] Simulation start, step submission, and completion APIs
- [ ] XP award logic + Badge checker service
- [ ] SimulationPage UI: NISTPhaseIndicator, SituationPanel, DecisionPanel, FeedbackModal
- [ ] CompletionPage UI

### Phase 4 — Progress & Admin Portal (Week 7)
- [ ] Progress API + ProgressPage UI (XP bar, badges, history)
- [ ] Admin dashboard stats API + UI
- [ ] Admin CRUD pages for scenarios, steps, decisions
- [ ] User management admin page

### Phase 5 — QA, Polish & Documentation (Week 8)
- [ ] Scenario seeder command + fixture data (all 9 scenarios)
- [ ] Backend unit tests and API tests
- [ ] Frontend smoke testing
- [ ] Full integration walkthrough
- [ ] README, API Docs, User Guide
- [ ] Final bug fixes and UI polish

---

## 10. Agent Sign-Off

| Agent | Role | Status |
|---|---|---|
| Agent 1 | System Architect | ✅ Analysis complete — awaiting approval |
| Agent 2 | Database & Scenario Designer | ✅ Schema and scenarios designed |
| Agent 3 | Backend Developer | ✅ API plan and engine logic defined |
| Agent 4 | Frontend Developer | ✅ Page map and component plan ready |
| Agent 5 | Admin & Content Management | ✅ Admin features and seed strategy defined |
| Agent 6 | QA, Integration & Deployment | ✅ Testing strategy and deployment plan ready |

---

> **Next Step**: Review this plan, provide any corrections or approvals, and send the prompt to begin Phase 1 implementation.
