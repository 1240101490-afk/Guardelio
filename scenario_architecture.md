# Guardelio — Complete Learning Architecture & Scenario Design
## Phase 3: Scenario System, Learning Framework & Simulation Design

> **Status**: Scenario Architecture Phase — No application code generated  
> **Builds on**: Phase 1 (Implementation Plan) + Phase 2 (Technical Architecture)  
> **Purpose**: Define the complete scenario system that drives all backend models and frontend UI

---

# AGENT 1 — Learning Framework Designer
## Complete Student Learning Workflow

---

## 1.1 Core Learning Philosophy

Guardelio is a **decision-based learning environment**, not a quiz or a game. Every interaction is built around a single pedagogical principle:

> **"Place the student inside a real incident. Force a decision. Explain the consequence. Build understanding through doing — not reading."**

The learning flow mirrors how real incident responders think: receive a situation, assess the threat, make a time-pressured decision, observe the outcome, and reflect. This pattern — **Observe → Decide → Reflect** — repeats at every step of every simulation.

---

## 1.2 The 11-Stage Learning Workflow

Every student journey through a scenario follows this exact sequence, without exception:

```
╔═════════════════════════════════════════════════════════════╗
║                   STUDENT LEARNING JOURNEY                  ║
╠═════════════════════════════════════════════════════════════╣
║  Stage 1   │  CATEGORY SELECTION                            ║
║            │  Student browses incident categories           ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 2   │  CATEGORY OVERVIEW                             ║
║            │  Context: what this incident type is, why it   ║
║            │  matters, real-world impact                     ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 3   │  LEARNING OBJECTIVES                           ║
║            │  3–4 bullet points: what student will learn    ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 4   │  SCENARIO SELECTION                            ║
║            │  Choose from Beginner / Intermediate / Advanced ║
║            │  Cards show: title, XP, duration, difficulty   ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 5   │  SCENARIO INTRODUCTION                         ║
║            │  Scene-setting briefing: who the student is,   ║
║            │  their role, what has happened so far          ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 6   │  INCIDENT SIMULATION (loops per step)          ║
║            │  Present situation → student makes a decision  ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 7   │  IMMEDIATE FEEDBACK                            ║
║            │  After every decision: correct/incorrect +     ║
║            │  educational explanation + XP awarded          ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 8   │  NEXT STEP (loop back to Stage 6)              ║
║            │  Simulation continues to next step             ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 9   │  SCENARIO COMPLETION                           ║
║            │  Final informational step — incident resolved  ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 10  │  FINAL RESULTS                                 ║
║            │  XP earned, accuracy %, time taken, badges     ║
╠════════════╪════════════════════════════════════════════════╣
║  Stage 11  │  LESSONS LEARNED                               ║
║            │  3–5 key takeaways tied to NIST phases +       ║
║            │  real-world best practices                      ║
╚════════════╧════════════════════════════════════════════════╝
```

---

## 1.3 Stage-by-Stage Design Specification

### Stage 1 — Category Selection
- Student sees all active categories as visual cards
- Each card shows: icon, name, brief description, number of scenarios, difficulty range
- No login wall before browsing categories (but simulation requires login)
- Categories are ordered by `display_order` (admin-controlled)

### Stage 2 — Category Overview
- Dedicated page per category (not a modal)
- Sections: "What is this incident type?", "Real-World Impact", "What You Will Practice"
- Tone: professional but accessible — like a university module introduction
- Does NOT list NIST phases by name — the framework is internal scaffolding

### Stage 3 — Learning Objectives
- Displayed as 3–4 concise bullet points on the Category Overview page
- Written in student-facing language: "By the end of these scenarios, you will be able to..."
- Objectives are consistent per category — all scenarios within a category share the same category-level objectives
- Scenario-specific objectives appear on the Scenario Overview page

### Stage 4 — Scenario Selection
- Cards within the category page filtered by difficulty
- Each card shows: scenario title, difficulty badge, estimated duration, XP reward
- Completed scenarios show a ✅ checkmark but remain accessible for replay
- Student can attempt any difficulty — no enforced gating (they choose their own level)

### Stage 5 — Scenario Introduction
- Full-page briefing before the first step
- Written in second person: *"You are a junior security analyst at Meridian Bank. At 09:15 AM, your SIEM dashboard flags an alert..."*
- Shows: NIST phases this scenario will cover (as readable labels, not codes)
- Contains a prominent "Begin Simulation" button
- Estimated time reminder shown here

### Stage 6 — Incident Simulation (Core Loop)
- The **Observe → Decide → Reflect** loop (see 1.4 below)
- NIST Phase Bar at top always shows current phase
- Step title + narrative situation text presented first
- For `info` steps: a "Continue" button advances automatically (no decision)
- For `decision` steps: 2–4 option buttons presented

### Stage 7 — Immediate Feedback
- Triggered immediately after student selects an option
- Displayed as a modal overlay on the simulation page
- Contains: ✅ or ❌ icon, consequence label (Good choice / Risky decision), feedback text, XP earned this step
- Student must click "Continue" to acknowledge — feedback cannot be skipped

### Stage 8 — Next Step
- After modal is dismissed, simulation advances to the next step
- No page reload — state managed in SimulationContext
- NIST Phase Bar updates to reflect new phase if phase changes

### Stage 9 — Scenario Completion
- A final `info`-type step that narrates the incident resolution
- Written in narrative style: *"The ransomware was successfully contained. Systems were restored from clean backups within 4 hours..."*
- This is the emotional payoff — the student sees the result of their cumulative decisions

### Stage 10 — Final Results
- Separate completion page (not a step within the simulation)
- Shows: Total XP earned this session, Accuracy percentage, Time taken, Correct/incorrect decision breakdown, New badges unlocked
- Key decisions reviewed: each decision step listed with what the student chose vs. the correct answer

### Stage 11 — Lessons Learned
- Section below the results, on the same Completion page
- 3–5 bullet takeaways written by the scenario designer
- Each takeaway is tagged to a NIST phase (displayed as a subtle label)
- Ends with a recommended next scenario or return to dashboard

---

## 1.4 The Core Learning Loop (Observe → Decide → Reflect)

```
┌─────────────────────────────────────────────────────────┐
│                    SIMULATION STEP                       │
│                                                          │
│  OBSERVE          │  Student reads the situation.        │
│  ──────────────── │  A realistic incident narrative is   │
│  [Situation Text] │  presented. No hints given.          │
│                   │                                      │
│  DECIDE           │  Student selects one of 2–4 options. │
│  ──────────────── │  Each option represents a real-world │
│  [Option A]       │  response action. No obvious "right  │
│  [Option B]       │  answer" labelling — student must    │
│  [Option C]       │  apply knowledge.                    │
│                   │                                      │
│  REFLECT          │  Feedback modal appears.             │
│  ──────────────── │  Explains WHY the chosen action was  │
│  [Feedback Modal] │  correct or incorrect. Connects      │
│                   │  decision to real-world consequence. │
└─────────────────────────────────────────────────────────┘
         │
         ▼ (loops until is_final_step = true)
```

---

## 1.5 Student Progression Logic

| Condition | Behaviour |
|---|---|
| First visit to a category | Category Overview shown with Learning Objectives |
| Returning to a category | Directly shows Scenario Selection (overview accessible via link) |
| Scenario not yet started | Shows "Start" button, XP reward |
| Scenario in progress | Shows "Resume" button, current step indicator |
| Scenario completed | Shows ✅ badge, earned XP, "Replay" option |
| All scenarios in a category completed | Category card shows 100% completion indicator |

---

---

# AGENT 2 — Scenario Architecture Designer
## Complete 6-Category Scenario Hierarchy (26 Scenarios)

---

## 2.1 Hierarchy Design Rules (Applied to All Categories)

Every category must follow these exact structural rules:

1. **Exactly 3 difficulty tiers**: Beginner, Intermediate, Advanced
2. **Beginner**: Always 2 scenarios (lowest cognitive load, guided narrative)
3. **Intermediate**: Always 2 scenarios (moderate complexity, some branching)
4. **Advanced**: Always 1 scenario (high complexity, full branching, multi-phase)
5. **Total per category**: 5 scenarios
6. **Grand total**: 6 categories × 5 scenarios = **30 scenarios**
7. Scenario names are professional, real-world-sounding — not gamified
8. Difficulty progression within each category must be logical and sequential

---

## 2.2 Category 1: Malware Infection Response

**Icon**: 🦠  
**Color Theme**: Red-700  
**Description**: Investigate and respond to malicious software infections across various attack vectors.  

**Learning Objectives**:
- Identify signs of active malware infection on a system
- Apply containment procedures to prevent malware spread
- Execute eradication steps and verify system integrity
- Document findings and strengthen defenses post-incident

```
Malware Infection Response
├── Beginner
│   ├── S-MAL-01 │ "Suspicious Process Alert"
│   │             Situation: An employee reports slow system performance.
│   │             Task Manager shows an unknown process consuming CPU.
│   │             Student role: Junior Analyst
│   │
│   └── S-MAL-02 │ "Email Attachment Execution"
│                 Situation: An employee opened an email attachment.
│                 Antivirus triggered but was dismissed. Files now
│                 encrypting in a temp folder.
│                 Student role: Junior Analyst
│
├── Intermediate
│   ├── S-MAL-03 │ "Trojan Backdoor Discovery"
│   │             Situation: Firewall logs reveal periodic outbound
│   │             connections to an unknown IP. Investigation begins.
│   │             Student role: Security Analyst
│   │
│   └── S-MAL-04 │ "Spyware on Executive Laptop"
│                 Situation: An executive reports odd browser behavior.
│                 Keystroke anomalies detected in endpoint logs.
│                 Student role: Security Analyst
│
└── Advanced
    └── S-MAL-05 │ "Ransomware Network Outbreak"
                  Situation: Multiple workstations across three
                  departments simultaneously begin encrypting files.
                  A ransom note appears on screens.
                  Student role: Incident Response Lead
```

---

## 2.3 Category 2: Phishing Attack Response

**Icon**: 🎣  
**Color Theme**: Amber-600  
**Description**: Detect, investigate, and respond to social engineering attacks targeting organizational users.

**Learning Objectives**:
- Recognize indicators of phishing and social engineering attempts
- Investigate email headers, domains, and links safely
- Coordinate user response and limit credential exposure
- Implement controls to prevent repeat phishing campaigns

```
Phishing Attack Response
├── Beginner
│   ├── S-PHI-01 │ "Fake Login Page Report"
│   │             Situation: A user submits a helpdesk ticket — they
│   │             clicked a link claiming to be the IT portal and
│   │             entered their credentials.
│   │             Student role: Junior Analyst
│   │
│   └── S-PHI-02 │ "HR Payroll Diversion Scam"
│                 Situation: Finance receives an email appearing to
│                 come from the HR director requesting immediate
│                 payroll bank account changes.
│                 Student role: Junior Analyst
│
├── Intermediate
│   ├── S-PHI-03 │ "Targeted Spear Phishing Attack"
│   │             Situation: A senior engineer receives a highly
│   │             personalized email referencing a real internal
│   │             project, with a malicious attachment.
│   │             Student role: Security Analyst
│   │
│   └── S-PHI-04 │ "Business Email Compromise (BEC)"
│                 Situation: An attacker has compromised the CEO's
│                 email account and is sending wire transfer
│                 instructions to the finance department.
│                 Student role: Security Analyst
│
└── Advanced
    └── S-PHI-05 │ "Multi-Stage Phishing Campaign"
                  Situation: A coordinated campaign targets 40 users
                  simultaneously. First wave is credential harvesting;
                  second wave uses harvested accounts to spread
                  internally.
                  Student role: Incident Response Lead
```

---

## 2.4 Category 3: DDoS Attack Mitigation

**Icon**: 🌊  
**Color Theme**: Blue-600  
**Description**: Identify, analyze, and mitigate Distributed Denial of Service attacks against organizational infrastructure.

**Learning Objectives**:
- Distinguish between legitimate traffic spikes and DDoS attack patterns
- Apply rate limiting, filtering, and traffic-shaping countermeasures
- Coordinate with ISPs and upstream providers during active attacks
- Evaluate attack vectors and plan post-incident hardening

```
DDoS Attack Mitigation
├── Beginner
│   ├── S-DDoS-01 │ "Unexpected Traffic Spike"
│   │              Situation: The company website is loading slowly.
│   │              The hosting dashboard shows traffic 10x above normal
│   │              from concentrated geographic sources.
│   │              Student role: Junior Network Analyst
│   │
│   └── S-DDoS-02 │ "HTTP Flood on Web Application"
│                  Situation: The web application server logs show
│                  thousands of identical GET requests per second
│                  from rotating IP addresses.
│                  Student role: Junior Network Analyst
│
├── Intermediate
│   ├── S-DDoS-03 │ "SYN Flood Attack"
│   │              Situation: Server connection tables are nearly full.
│   │              Network logs show thousands of half-open TCP
│   │              connections. Legitimate users cannot connect.
│   │              Student role: Network Security Analyst
│   │
│   └── S-DDoS-04 │ "UDP Amplification Attack"
│                  Situation: Massive UDP traffic is overwhelming the
│                  firewall. Packet analysis reveals amplified responses
│                  from third-party DNS and NTP servers being abused.
│                  Student role: Network Security Analyst
│
└── Advanced
    └── S-DDoS-05 │ "Distributed Botnet Assault"
                   Situation: A coordinated botnet of 15,000 nodes
                   launches a multi-vector attack combining HTTP floods,
                   SYN floods, and application-layer attacks
                   simultaneously.
                   Student role: Incident Response Lead
```

---

## 2.5 Category 4: Data Breach Response

**Icon**: 🔓  
**Color Theme**: Purple-600  
**Description**: Respond to unauthorized data access and exfiltration incidents following legal and procedural best practices.

**Learning Objectives**:
- Identify the scope and source of a data breach
- Apply containment procedures to stop ongoing data exfiltration
- Fulfill legal notification obligations (GDPR awareness)
- Conduct forensic preservation of evidence

```
Data Breach Response
├── Beginner
│   ├── S-BRE-01 │ "Publicly Exposed File Server"
│   │             Situation: An external security researcher contacts
│   │             the company — a file server containing employee
│   │             records appears to be openly accessible on the web.
│   │             Student role: Junior Analyst
│   │
│   └── S-BRE-02 │ "Compromised User Account"
│                 Situation: Login logs show a valid user account
│                 accessing sensitive HR files at 3 AM from an
│                 overseas IP address. The user confirms they were
│                 not active.
│                 Student role: Junior Analyst
│
├── Intermediate
│   ├── S-BRE-03 │ "Database Records Exfiltration"
│   │             Situation: Database query logs show an unusual
│   │             SELECT * dump of the customer table, 500,000 records,
│   │             executed by a service account. Data was exported.
│   │             Student role: Security Analyst
│   │
│   └── S-BRE-04 │ "Cloud Storage Misconfiguration"
│                 Situation: A misconfigured S3-equivalent bucket
│                 has been publicly readable for an unknown period.
│                 It contains contracts, financial reports, and PII.
│                 Student role: Security Analyst
│
└── Advanced
    └── S-BRE-05 │ "Large-Scale Customer Data Breach"
                  Situation: Threat intelligence confirms 2 million
                  customer records are being sold on a dark web forum.
                  The breach source is unknown. Legal, PR, and
                  technical teams must be coordinated simultaneously.
                  Student role: Incident Response Lead
```

---

## 2.6 Category 5: Insider Threat Detection

**Icon**: 👤  
**Color Theme**: Orange-600  
**Description**: Detect, investigate, and respond to threats originating from within the organization.

**Learning Objectives**:
- Recognize behavioral indicators of insider threat activity
- Apply proportional investigation procedures without violating employee rights
- Distinguish accidental from malicious insider behavior
- Coordinate with HR and legal teams during investigations

```
Insider Threat Detection
├── Beginner
│   ├── S-INS-01 │ "Unauthorized File Access Alert"
│   │             Situation: DLP system flags a junior employee
│   │             accessing payroll files outside their normal
│   │             job scope. No data was copied — access only.
│   │             Student role: Junior Analyst
│   │
│   └── S-INS-02 │ "USB Device Data Copy"
│                 Situation: Endpoint monitoring detects a large
│                 file copy to a USB drive by an employee who
│                 submitted their resignation last week.
│                 Student role: Junior Analyst
│
├── Intermediate
│   ├── S-INS-03 │ "Privilege Misuse by IT Administrator"
│   │             Situation: Audit logs reveal a system administrator
│   │             has been accessing executive email accounts using
│   │             admin privileges over the past three weeks.
│   │             Student role: Security Analyst
│   │
│   └── S-INS-04 │ "Confidential Data Sent to Personal Email"
│                 Situation: Email gateway logs show a sales manager
│                 forwarding client lists and pricing strategies to
│                 a personal Gmail account over two months.
│                 Student role: Security Analyst
│
└── Advanced
    └── S-INS-05 │ "Coordinated Malicious Insider Attack"
                  Situation: Evidence suggests a departing employee
                  colluded with a competitor — they accessed source
                  code repositories, exfiltrated IP, and planted a
                  logic bomb before their exit date.
                  Student role: Incident Response Lead
```

---

## 2.7 Category 6: Network Intrusion Response

**Icon**: 🌐  
**Color Theme**: Teal-600  
**Description**: Detect and respond to unauthorized access and movement within organizational network infrastructure.

**Learning Objectives**:
- Identify indicators of network compromise using log and traffic analysis
- Apply network segmentation and access control to limit attacker movement
- Trace attacker activity across systems and reconstruct the attack timeline
- Implement monitoring improvements to detect future intrusions

```
Network Intrusion Response
├── Beginner
│   ├── S-NET-01 │ "Failed Login Brute Force Alert"
│   │             Situation: The firewall flags 500 failed SSH login
│   │             attempts within 10 minutes targeting a public-facing
│   │             server from a single IP.
│   │             Student role: Junior Network Analyst
│   │
│   └── S-NET-02 │ "Unauthorized Port Scan Detected"
│                 Situation: IDS alerts show a systematic port scan
│                 across the internal network subnet, probing all
│                 hosts on standard service ports.
│                 Student role: Junior Network Analyst
│
├── Intermediate
│   ├── S-NET-03 │ "Remote Access Compromise via VPN"
│   │             Situation: A valid VPN account is connecting from
│   │             two geographic locations simultaneously — one is the
│   │             legitimate user working from home; the other is
│   │             unknown.
│   │             Student role: Network Security Analyst
│   │
│   └── S-NET-04 │ "Lateral Movement Across Servers"
│                 Situation: An attacker who initially compromised a
│                 low-privilege web server is now moving laterally —
│                 credential dumping and accessing internal database
│                 servers.
│                 Student role: Network Security Analyst
│
└── Advanced
    └── S-NET-05 │ "Persistent Advanced Network Intrusion"
                  Situation: Threat intelligence identifies an APT
                  group has maintained persistent access to the
                  network for an estimated 60 days. Multiple backdoors
                  may exist. A full compromise assessment is required.
                  Student role: Incident Response Lead
```

---

## 2.8 Complete Scenario Index

| ID | Category | Difficulty | Scenario Name |
|---|---|---|---|
| S-MAL-01 | Malware | Beginner | Suspicious Process Alert |
| S-MAL-02 | Malware | Beginner | Email Attachment Execution |
| S-MAL-03 | Malware | Intermediate | Trojan Backdoor Discovery |
| S-MAL-04 | Malware | Intermediate | Spyware on Executive Laptop |
| S-MAL-05 | Malware | Advanced | Ransomware Network Outbreak |
| S-PHI-01 | Phishing | Beginner | Fake Login Page Report |
| S-PHI-02 | Phishing | Beginner | HR Payroll Diversion Scam |
| S-PHI-03 | Phishing | Intermediate | Targeted Spear Phishing Attack |
| S-PHI-04 | Phishing | Intermediate | Business Email Compromise (BEC) |
| S-PHI-05 | Phishing | Advanced | Multi-Stage Phishing Campaign |
| S-DDoS-01 | DDoS | Beginner | Unexpected Traffic Spike |
| S-DDoS-02 | DDoS | Beginner | HTTP Flood on Web Application |
| S-DDoS-03 | DDoS | Intermediate | SYN Flood Attack |
| S-DDoS-04 | DDoS | Intermediate | UDP Amplification Attack |
| S-DDoS-05 | DDoS | Advanced | Distributed Botnet Assault |
| S-BRE-01 | Data Breach | Beginner | Publicly Exposed File Server |
| S-BRE-02 | Data Breach | Beginner | Compromised User Account |
| S-BRE-03 | Data Breach | Intermediate | Database Records Exfiltration |
| S-BRE-04 | Data Breach | Intermediate | Cloud Storage Misconfiguration |
| S-BRE-05 | Data Breach | Advanced | Large-Scale Customer Data Breach |
| S-INS-01 | Insider Threat | Beginner | Unauthorized File Access Alert |
| S-INS-02 | Insider Threat | Beginner | USB Device Data Copy |
| S-INS-03 | Insider Threat | Intermediate | Privilege Misuse by IT Administrator |
| S-INS-04 | Insider Threat | Intermediate | Confidential Data Sent to Personal Email |
| S-INS-05 | Insider Threat | Advanced | Coordinated Malicious Insider Attack |
| S-NET-01 | Network Intrusion | Beginner | Failed Login Brute Force Alert |
| S-NET-02 | Network Intrusion | Beginner | Unauthorized Port Scan Detected |
| S-NET-03 | Network Intrusion | Intermediate | Remote Access Compromise via VPN |
| S-NET-04 | Network Intrusion | Intermediate | Lateral Movement Across Servers |
| S-NET-05 | Network Intrusion | Advanced | Persistent Advanced Network Intrusion |

**Total: 30 Scenarios across 6 Categories**

---

---

# AGENT 3 — Scenario Flow Designer
## Standardized Scenario Template & Step Specification

---

## 3.1 The Universal Scenario Template

Every one of the 30 scenarios uses this identical structure. No exceptions. This ensures students develop a consistent learning rhythm and administrators can create new content predictably.

```
╔══════════════════════════════════════════════════════════════════╗
║                    SCENARIO TEMPLATE                             ║
╠══════════════════════════════════════════════════════════════════╣
║  METADATA BLOCK                                                  ║
║  ─────────────────────────────────────────────────────────────   ║
║  Scenario ID        │  e.g., S-MAL-05                           ║
║  Scenario Title     │  e.g., Ransomware Network Outbreak        ║
║  Category           │  Malware Infection Response               ║
║  Difficulty         │  Advanced                                 ║
║  Estimated Duration │  20–25 minutes                            ║
║  XP Reward          │  200 XP                                   ║
║  Student Role       │  Incident Response Lead                   ║
║  NIST Phases Used   │  All 4 phases                             ║
╠══════════════════════════════════════════════════════════════════╣
║  OVERVIEW BLOCK (shown on Scenario Overview page)                ║
║  ─────────────────────────────────────────────────────────────   ║
║  Background Context │  What has already happened                ║
║  Student's Role     │  Who they are in this scenario            ║
║  Primary Challenge  │  The core problem to be solved            ║
╠══════════════════════════════════════════════════════════════════╣
║  LEARNING OBJECTIVES (3–4 bullet points)                         ║
║  ─────────────────────────────────────────────────────────────   ║
║  • Objective 1                                                   ║
║  • Objective 2                                                   ║
║  • Objective 3                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  STEP SEQUENCE                                                   ║
║  ─────────────────────────────────────────────────────────────   ║
║  Step 1 (info)       → NIST: Preparation                        ║
║  Step 2 (decision)   → NIST: Detection                          ║
║  Step 3 (decision)   → NIST: Detection                          ║
║  Step 4 (decision)   → NIST: Containment                        ║
║  Step 5 (decision)   → NIST: Eradication                        ║
║  Step 6 (decision)   → NIST: Recovery                           ║
║  Step 7 (info, final)→ NIST: Post-Incident                      ║
╠══════════════════════════════════════════════════════════════════╣
║  LESSONS LEARNED BLOCK (shown on Completion page)                ║
║  ─────────────────────────────────────────────────────────────   ║
║  3–5 key takeaways from this scenario                            ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 3.2 Step Type Definitions

| Step Type | Purpose | Student Action | Decision Required? |
|---|---|---|---|
| `info` | Deliver context or scene-setting narrative | Click "Continue" | No |
| `decision` | Present a situation requiring a judgment call | Select one of 2–4 options | Yes |
| `quiz` | Test recall of a fact just established | Select one of 3–4 options | Yes |

---

## 3.3 Step Counts by Difficulty

| Difficulty | Info Steps | Decision Steps | Total Steps | XP Reward |
|---|---|---|---|---|
| Beginner | 2 | 3 | 5 | 75 XP |
| Intermediate | 2 | 4 | 6 | 125 XP |
| Advanced | 2 | 5 | 7 | 200 XP |

**Rationale**:
- Beginners need more narrative context (higher info:decision ratio) to feel supported
- Advanced scenarios have maximum decision steps to maximize learning depth
- XP scales meaningfully to reflect genuine effort

---

## 3.4 Decision Option Specification

Every `decision` step must have:
- **Minimum**: 2 options
- **Maximum**: 4 options
- **Exactly 1**: correct option (marked `is_correct = true`)
- **Remaining**: incorrect options with distinct `consequence_type`

| Consequence Type | Meaning | XP Awarded |
|---|---|---|
| `positive` | Correct and best-practice response | 15–30 XP |
| `negative` | Actively harmful decision | 0 XP |
| `neutral` | Not wrong but not optimal | 0 XP |

**Design Rule**: Incorrect options must be plausible. They should represent actions a real, under-trained analyst might genuinely consider. Obvious "joke" options are not permitted — this is educational, not a game show.

---

## 3.5 Feedback Text Specification

Every decision option's `feedback_text` must follow this structure:

```
For CORRECT options:
"[Why this is correct in one sentence]. [Real-world context explaining the 
consequence of this action]. [Connection to industry best practice or NIST guidance]."

Example:
"Isolating the affected workstation from the network is the correct first 
containment step. This prevents the malware from communicating with its 
command-and-control server and stops lateral spread to other machines. 
NIST SP 800-61 recommends network isolation as the primary containment 
action for active malware incidents."

For INCORRECT (negative) options:
"[Why this action would cause harm in one sentence]. [What the likely 
consequence would be]. [What should have been done instead, briefly]."

Example:
"Requesting the user to restart their computer before isolating it could 
trigger a malware persistence mechanism or destroy volatile memory evidence. 
The system should first be isolated from the network before any local 
actions are taken."

For INCORRECT (neutral) options:
"[Why this is not the optimal choice]. [What the limitation of this action is]. 
[What would have been better]."

Example:
"Running a full antivirus scan immediately is not incorrect, but it is not 
the right first step. Without first isolating the machine, an active network 
connection could allow the malware to update or communicate while the scan 
is running. Network isolation should precede any scanning."
```

---

## 3.6 Full Worked Example: S-MAL-01 "Suspicious Process Alert"

**Category**: Malware Infection Response  
**Difficulty**: Beginner  
**Duration**: 10–12 minutes  
**XP Reward**: 75 XP  
**Student Role**: Junior Security Analyst at Nexus Financial Services

---

**OVERVIEW**  
You are a Junior Security Analyst at Nexus Financial Services. At 10:32 AM, a helpdesk ticket is raised by an employee in the accounts department. Their computer has been running unusually slowly for the past hour. Your team lead has assigned the ticket to you for initial triage.

**LEARNING OBJECTIVES**:
- Identify initial indicators of a potential malware infection
- Apply safe triage procedures without disturbing potential evidence
- Escalate appropriately within the incident response process
- Document findings accurately for handover

---

**Step 1** | Type: `info` | NIST: `Preparation`  
*"You open the helpdesk ticket. The employee's name is Sarah Chen, accounts payable. She reports her computer has been slow since 9:45 AM. She cannot remember opening anything unusual. Your company's Incident Response Plan (IRP) instructs analysts to begin with remote observation before touching the affected machine. You open your remote monitoring console."*

→ Action: **[Continue →]**

---

**Step 2** | Type: `decision` | NIST: `Detection & Analysis`  
*"You connect to Sarah's workstation remotely. Task Manager shows CPU usage at 97%. You spot an unfamiliar process: `svchost32.exe` consuming 94% CPU. Note: the legitimate Windows process is `svchost.exe` — the name is slightly different. What is your first action?"*

Options:
- **A) End the svchost32.exe process immediately to restore performance**  
  `is_correct: false` | `consequence: negative` | `xp: 0`  
  Feedback: *"Terminating the process immediately destroys volatile memory evidence, including the process's network connections, loaded modules, and command-line arguments. This makes forensic analysis significantly harder. The process should be investigated first, and any action taken should be coordinated and documented."*

- **B) Search the process name and location in the file system to investigate**  
  `is_correct: true` | `consequence: positive` | `xp: 20`  
  Feedback: *"Correct. Before taking any action, you should investigate the process to confirm whether it is malicious. Checking the file path, parent process, and digital signature are all safe investigative steps that preserve evidence. This aligns with the Detection & Analysis phase of NIST SP 800-61."*

- **C) Ask Sarah to restart the computer to see if the problem resolves**  
  `is_correct: false` | `consequence: negative` | `xp: 0`  
  Feedback: *"Restarting the computer would clear all volatile memory, destroying critical forensic evidence such as running processes, network connections, and in-memory malware variants. Restarting is never a first response to a suspected security incident."*

---

**Step 3** | Type: `decision` | NIST: `Detection & Analysis`  
*"Your investigation reveals svchost32.exe is located at C:\Users\Sarah\AppData\Roaming\ — not in C:\Windows\System32\ where the legitimate process lives. It has no digital signature and was created at 9:43 AM today. Antivirus has not flagged it. What do you do next?"*

Options:
- **A) Submit the file hash to VirusTotal for reputation analysis**  
  `is_correct: true` | `consequence: positive` | `xp: 20`  
  Feedback: *"Excellent. Submitting the file hash (not the file itself) to a threat intelligence platform like VirusTotal is a low-risk, high-value investigative step. It confirms malicious classification without risking further exposure. This is a core Detection & Analysis technique."*

- **B) Email Sarah's manager to inform them of the situation before doing anything else**  
  `is_correct: false` | `consequence: neutral` | `xp: 0`  
  Feedback: *"Notifying management is part of the process but should not happen before you have confirmed the threat and taken initial containment steps. Acting on an unconfirmed incident without investigation can cause unnecessary disruption. Investigate first, then escalate with evidence."*

- **C) Delete the svchost32.exe file from the file system**  
  `is_correct: false` | `consequence: negative` | `xp: 0`  
  Feedback: *"Deleting the file before investigation removes the ability to analyze the malware's behavior, origin, or potential persistence mechanisms. Evidence preservation is critical. The file should be quarantined, not deleted, and only after the threat is confirmed."*

---

**Step 4** | Type: `decision` | NIST: `Containment`  
*"VirusTotal returns a 47/70 detection rate — the file is confirmed malicious. It is identified as a Trojan dropper. The process has been making outbound connections to 185.220.x.x every 5 minutes. What is your immediate containment action?"*

Options:
- **A) Isolate the workstation from the network immediately**  
  `is_correct: true` | `consequence: positive` | `xp: 20`  
  Feedback: *"Network isolation is the correct and urgent containment action. Disconnecting the machine from the network stops the malware's C2 (Command and Control) communication and prevents it from receiving further instructions or exfiltrating additional data. This is the primary containment step in NIST SP 800-61."*

- **B) Run a full antivirus scan on the isolated workstation**  
  `is_correct: false` | `consequence: neutral` | `xp: 0`  
  Feedback: *"A full antivirus scan is appropriate, but only after isolation. If the machine is still connected to the network while scanning, the malware remains capable of communicating with its C2 server. Isolation must come first."*

---

**Step 5** | Type: `info` | NIST: `Post-Incident Activity` | `is_final_step: true`  
*"The workstation has been successfully isolated. You have documented the process name, file hash, creation timestamp, and C2 IP addresses. Your team lead approves escalation to the full incident response team. The machine is scheduled for forensic imaging before reimaging. You have successfully completed the initial triage of a malware incident. Your methodical approach preserved evidence and contained the threat."*

→ Action: **[View Results →]**

---

**LESSONS LEARNED**:
1. **Detection (NIST)** — Subtle naming differences (svchost32.exe vs svchost.exe) are a common malware masquerading technique. Always verify process file paths, not just names.
2. **Evidence Preservation** — Never terminate, delete, or restart before investigating. Volatile memory data is irreplaceable.
3. **Threat Intelligence** — File hash lookups via threat intelligence platforms provide rapid malware confirmation without risk.
4. **Containment First** — Network isolation must precede any local remediation actions to stop C2 communication.
5. **Documentation** — Every action taken and finding noted must be recorded in real time for handover and legal purposes.

---

---

# AGENT 4 — NIST SP 800-61 Integration Designer
## Framework Integration Strategy

---

## 4.1 The NIST SP 800-61 Framework Overview

The four phases of NIST SP 800-61 form the **invisible backbone** of every Guardelio simulation. Students experience the framework through scenario progression rather than being lectured about it.

| NIST Phase | Internal Code | Student-Facing Label |
|---|---|---|
| Preparation | `preparation` | "Preparation" |
| Detection & Analysis | `detection` | "Detection & Analysis" |
| Containment, Eradication & Recovery | `containment` / `eradication` / `recovery` | Split into 3 sub-phases for granularity |
| Post-Incident Activity | `post_incident` | "Post-Incident Review" |

> **Design Decision**: The original NIST framework combines Containment, Eradication, and Recovery into one phase. Guardelio splits them into three distinct step tags for educational granularity — students can see which specific sub-phase they are in. The framework label displayed is still the combined NIST name.

---

## 4.2 NIST Phase Allocation by Step (All Difficulties)

### Beginner Scenarios (5 steps)
| Step | NIST Phase Tag | Step Type | Purpose |
|---|---|---|---|
| 1 | `preparation` | info | Set context, establish student role and tools available |
| 2 | `detection` | decision | Initial triage — identify and confirm the incident |
| 3 | `detection` | decision | Deep investigation — classify the threat |
| 4 | `containment` | decision | Take immediate action to limit damage |
| 5 | `post_incident` | info (final) | Incident resolution, documentation summary |

### Intermediate Scenarios (6 steps)
| Step | NIST Phase Tag | Step Type | Purpose |
|---|---|---|---|
| 1 | `preparation` | info | Context and available resources |
| 2 | `detection` | decision | Initial detection and analysis |
| 3 | `detection` | decision | Deeper threat investigation |
| 4 | `containment` | decision | Containment strategy selection |
| 5 | `eradication` | decision | Removal and remediation |
| 6 | `post_incident` | info (final) | Resolution and lessons |

### Advanced Scenarios (7 steps)
| Step | NIST Phase Tag | Step Type | Purpose |
|---|---|---|---|
| 1 | `preparation` | info | Complex context, multiple stakeholders |
| 2 | `detection` | decision | Multi-signal detection challenge |
| 3 | `detection` | decision | Threat attribution and scope analysis |
| 4 | `containment` | decision | Containment under operational pressure |
| 5 | `eradication` | decision | System-wide eradication with trade-offs |
| 6 | `recovery` | decision | Staged recovery with validation |
| 7 | `post_incident` | info (final) | Post-incident report, policy changes |

---

## 4.3 NIST Phase Bar — UI Integration

The NISTPhaseBar component at the top of every SimulationPage shows the student's current position in the framework at all times.

```
BEGINNER SCENARIO VIEW:
┌────────────────────────────────────────────────────────┐
│  [● Preparation] → [● Detection] → [○ Containment] → [○ Post-Incident]  │
└────────────────────────────────────────────────────────┘
  ● = completed or current    ○ = upcoming

ADVANCED SCENARIO VIEW:
┌──────────────────────────────────────────────────────────────────────────────┐
│ [✓ Prep] → [● Detection] → [○ Containment] → [○ Eradication] → [○ Recovery] → [○ Post] │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Design Rules for NIST Phase Bar**:
- Current phase highlighted with primary color
- Completed phases show a ✓ checkmark
- Upcoming phases are muted/greyed
- Phase name is human-readable (not the internal enum code)
- Bar does not show which step number is current — only the phase

---

## 4.4 NIST Phase Coverage per Category

| Category | Preparation | Detection | Containment | Eradication | Recovery | Post-Incident |
|---|---|---|---|---|---|---|
| Malware | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |
| Phishing | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |
| DDoS | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |
| Data Breach | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |
| Insider Threat | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |
| Network Intrusion | ✅ | ✅ | ✅ | ✅ (Int+Adv) | ✅ (Adv) | ✅ |

**Conclusion**: A student who completes all 30 scenarios will have experienced all 4 NIST phases (all 6 sub-phases) across all 6 incident categories — comprehensive coverage of the framework.

---

## 4.5 NIST Learning Progression by Difficulty

| Beginner | Intermediate | Advanced |
|---|---|---|
| Focus: Detection & Containment | Focus: Detection through Eradication | Focus: Full lifecycle management |
| 2 NIST phases encountered | 4 NIST phases encountered | All 6 sub-phases encountered |
| Role: Observer & first responder | Role: Analyst making autonomous decisions | Role: Incident lead coordinating teams |

---

---

# AGENT 5 — Gamification Designer
## XP Economy, Badge System & Progress Architecture

---

## 5.1 Gamification Philosophy

Guardelio's gamification serves **one purpose**: to make progress visible and provide intrinsic motivation to continue learning. It must never:
- Distract from the educational content
- Create competitive pressure between students
- Feel like a reward loop from a mobile game
- Require daily engagement

The system rewards **knowledge and effort** — not time spent on the platform.

---

## 5.2 XP Economy Design

### XP Sources

| Source | XP Amount | Condition |
|---|---|---|
| Correct decision (Beginner step) | 15–20 XP | Per correct decision option |
| Correct decision (Intermediate step) | 20–25 XP | Per correct decision option |
| Correct decision (Advanced step) | 25–30 XP | Per correct decision option |
| Scenario completion (Beginner) | +25 XP bonus | On session completion |
| Scenario completion (Intermediate) | +50 XP bonus | On session completion |
| Scenario completion (Advanced) | +75 XP bonus | On session completion |
| Perfect score bonus (100% correct) | +30 XP | All decisions correct |

### XP by Full Scenario Completion (Estimated)

| Difficulty | Max XP from Decisions | Completion Bonus | Perfect Bonus | Total Max |
|---|---|---|---|---|
| Beginner | 3 × 20 = 60 XP | +25 XP | +30 XP | **115 XP** |
| Intermediate | 4 × 25 = 100 XP | +50 XP | +30 XP | **180 XP** |
| Advanced | 5 × 30 = 150 XP | +75 XP | +30 XP | **255 XP** |

### Total Platform XP (Perfect Scores, All 30 Scenarios)

| Difficulty | Count | XP Each | Subtotal |
|---|---|---|---|
| Beginner (12 scenarios) | 12 | 115 | 1,380 XP |
| Intermediate (12 scenarios) | 12 | 180 | 2,160 XP |
| Advanced (6 scenarios) | 6 | 255 | 1,530 XP |
| **Grand Total** | **30** | — | **~5,070 XP** |

---

## 5.3 Badge System Design

### Badge Tiers

| Tier | Color | Visual | Meaning |
|---|---|---|---|
| Bronze | #CD7F32 | 🥉 | Entry-level achievement |
| Silver | #C0C0C0 | 🥈 | Developing proficiency |
| Gold | #FFD700 | 🥇 | High achievement |

### Complete Badge Catalog (18 Badges)

#### Progression Badges

| Badge Name | Tier | Criteria Type | Criteria Value | Description |
|---|---|---|---|---|
| First Responder | Bronze | completion_count | 1 | Complete your first scenario |
| Incident Analyst | Bronze | completion_count | 5 | Complete 5 scenarios |
| Senior Analyst | Silver | completion_count | 15 | Complete 15 scenarios |
| Cyber Defender | Gold | completion_count | 30 | Complete all 30 scenarios |

#### XP Milestone Badges

| Badge Name | Tier | Criteria Type | Criteria Value | Description |
|---|---|---|---|---|
| Quick Learner | Bronze | xp_threshold | 250 | Earn 250 XP |
| Skilled Analyst | Silver | xp_threshold | 1000 | Earn 1,000 XP |
| Security Expert | Silver | xp_threshold | 2500 | Earn 2,500 XP |
| NIST Master | Gold | xp_threshold | 5000 | Earn 5,000 XP |

#### Accuracy Badges

| Badge Name | Tier | Criteria Type | Criteria Value | Description |
|---|---|---|---|---|
| Sharp Thinker | Bronze | perfect_score | 1 | Achieve 100% on any scenario |
| Precision Analyst | Silver | perfect_score | 5 | Achieve 100% on 5 scenarios |
| Cyber Sentinel | Gold | perfect_score | 10 | Achieve 100% on 10 scenarios |

#### Category Mastery Badges

| Badge Name | Tier | Criteria Type | Criteria Value | Description |
|---|---|---|---|---|
| Malware Hunter | Bronze | category_complete | malware | Complete all Malware scenarios |
| Phishing Guard | Bronze | category_complete | phishing | Complete all Phishing scenarios |
| Network Defender | Bronze | category_complete | network | Complete all Network Intrusion scenarios |
| Breach Investigator | Silver | category_complete | data_breach | Complete all Data Breach scenarios |
| Insider Investigator | Silver | category_complete | insider | Complete all Insider Threat scenarios |
| DDoS Responder | Silver | category_complete | ddos | Complete all DDoS scenarios |
| Category Champion | Gold | all_categories | 6 | Complete all scenarios in all categories |

**Total: 18 Badges**

---

## 5.4 Progress Tracking Design

### Student Progress Metrics

| Metric | How Calculated | Where Displayed |
|---|---|---|
| Total XP | SUM of all session xp_earned | Navbar (always visible), Profile |
| Overall Completion % | (completed scenarios / 30) × 100 | Dashboard, Progress page |
| Category Completion % | Per-category version of above | Category cards |
| Overall Accuracy % | (total correct decisions / total decisions) × 100 | Progress page |
| Badges Earned | COUNT of UserBadge records | Profile, Progress page, Completion page |
| Scenarios Completed | COUNT of sessions where status=completed | Progress page |

### Progress Page Layout (Design Specification)

```
PROGRESS PAGE
├── Top Row: XP Bar [====75%====] "3,800 / 5,070 XP"
│           Scenarios: "18 / 30 completed"
│           Accuracy: "82% overall"
│
├── Badge Grid (all 18 badges displayed)
│   ├── Earned badges: full color, earned date shown
│   └── Unearned badges: greyed out, criteria shown on hover
│
├── Category Progress
│   └── Per category: progress bar + X/5 scenarios
│
└── Session History Table
    └── Columns: Date | Scenario | XP | Accuracy | Duration
```

---

## 5.5 Gamification Display Rules

| Element | Rule |
|---|---|
| XP Counter in Navbar | Always visible when logged in. Animates +N when XP is earned. |
| Badge notification | Badge award shown on Completion page only — not as a popup mid-simulation |
| Progress percentage | Rounded to nearest whole number |
| XP earned in feedback | Shown in every Feedback Modal — reinforces correct decisions |
| Badge greyed state | Unearned badges visible but greyed — shows what is achievable |
| No streak tracking | Daily login streaks are not tracked — this is not a habit app |

---

---

# AGENT 6 — Validation & Consistency Reviewer
## Architecture Audit, Quality Review & Scalability Assessment

---

## 6.1 Category Hierarchy Consistency Audit

| Check | Malware | Phishing | DDoS | Data Breach | Insider Threat | Network Intrusion |
|---|---|---|---|---|---|---|
| 2 Beginner scenarios | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 Intermediate scenarios | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 1 Advanced scenario | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 Learning objectives | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Consistent student roles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Professional scenario names | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scenario IDs assigned | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Verdict**: ✅ All 6 categories follow an identical structure.

---

## 6.2 Difficulty Progression Audit

| Category | Beginner → Intermediate Progression | Intermediate → Advanced Progression |
|---|---|---|
| Malware | Process alert → Trojan backdoor ✅ | Backdoor → Full ransomware outbreak ✅ |
| Phishing | Fake login → Spear phishing ✅ | Spear phishing → Multi-stage campaign ✅ |
| DDoS | Traffic spike → SYN/UDP floods ✅ | Floods → Coordinated botnet ✅ |
| Data Breach | File exposure → DB exfiltration ✅ | Exfiltration → Large-scale breach ✅ |
| Insider Threat | Access alert → Privilege misuse ✅ | Privilege misuse → Coordinated attack ✅ |
| Network Intrusion | Brute force → VPN compromise ✅ | VPN → APT persistence ✅ |

**Verdict**: ✅ All difficulty progressions are logical and appropriately scaled.

---

## 6.3 Learning Flow Consistency Audit

| Flow Element | Consistent? | Notes |
|---|---|---|
| All scenarios start with an `info` step | ✅ | Preparation phase always first |
| All scenarios end with an `info` (final) step | ✅ | Post-incident summary always last |
| Feedback shown after every decision | ✅ | Enforced by simulation engine |
| NIST phase bar always visible | ✅ | Part of SimulationPage layout, not per-scenario |
| Learning objectives present for every scenario | ✅ | On Scenario Overview page |
| Lessons learned on every completion page | ✅ | 3–5 bullet points per scenario |

**Verdict**: ✅ Learning flow is 100% consistent across all 30 scenarios.

---

## 6.4 NIST Integration Audit

| NIST Phase | Used in Beginner? | Used in Intermediate? | Used in Advanced? |
|---|---|---|---|
| Preparation | ✅ (Step 1, info) | ✅ (Step 1, info) | ✅ (Step 1, info) |
| Detection | ✅ (Steps 2–3) | ✅ (Steps 2–3) | ✅ (Steps 2–3) |
| Containment | ✅ (Step 4) | ✅ (Step 4) | ✅ (Step 4) |
| Eradication | ❌ Beginner only | ✅ (Step 5) | ✅ (Step 5) |
| Recovery | ❌ Beginner only | ❌ Intermediate only | ✅ (Step 6) |
| Post-Incident | ✅ (Final step) | ✅ (Final step) | ✅ (Final step) |

**Note on Beginner**: Beginners skip Eradication and Recovery steps by design — these phases introduce complex trade-off decisions that would overwhelm entry-level students. Beginners focus on Detection and Containment, which are the most universally applicable first-response skills.

**Verdict**: ✅ NIST integration is graduated, logical, and pedagogically sound.

---

## 6.5 Gamification Audit

| Item | Included? | Assessment |
|---|---|---|
| XP Points | ✅ | Appropriate |
| Bronze Badges | ✅ | 7 bronze badges — accessible |
| Silver Badges | ✅ | 7 silver badges — mid-term goals |
| Gold Badges | ✅ | 4 gold badges — long-term goals |
| Progress Percentage | ✅ | Clear and motivating |
| Coins | ❌ Excluded | ✅ Correct |
| Leaderboards | ❌ Excluded | ✅ Correct |
| Multiplayer | ❌ Excluded | ✅ Correct |
| Daily Rewards | ❌ Excluded | ✅ Correct |
| Game Characters | ❌ Excluded | ✅ Correct |
| Complex Animations | ❌ Excluded | ✅ Correct |
| Streaks | ❌ Excluded | ✅ Correct |

**Verdict**: ✅ Gamification is appropriately lightweight and educational.

---

## 6.6 Scalability Recommendations

| Area | Current State | Recommended Addition (Future Phase) |
|---|---|---|
| New categories | 6 categories, rigid ENUM | Add `category` as DB table (already done) — easy to add |
| New difficulties | 3 levels | `difficulty` ENUM can be extended to Expert |
| New step types | `info`, `decision`, `quiz` | `video`, `document-review` types feasible via ENUM extension |
| Scenario import | Manual DB entry via admin | Future: CSV/JSON import tool for bulk scenario loading |
| Badge criteria | 4 criteria types | Extendable ENUM — add `category_complete`, `streak` later |
| Scenario branching | `next_step` FK | Already supports full branching — no schema change needed |
| Multi-language | Not planned | `scenario_text` could be extracted to a translation table |

---

## 6.7 FYP Suitability Assessment

| Criterion | Assessment |
|---|---|
| Scope appropriateness | ✅ 30 scenarios is ambitious but achievable; admin can seed all content |
| Technical complexity | ✅ Branching logic, JWT auth, role-based access — strong FYP showcase |
| Educational value | ✅ NIST framework integration gives academic credibility |
| Demonstration potential | ✅ Visual simulation engine with phase tracking is demo-impressive |
| Code maintainability | ✅ Modular structure, service layer pattern — easy to explain in viva |
| Documentation readiness | ✅ This architecture document IS the technical documentation foundation |

---

## 6.8 Final Pre-Implementation Checklist

Before implementation begins in Phase 4:

- [x] All 6 categories defined with identical hierarchy
- [x] All 30 scenarios named and scoped
- [x] Scenario ID naming convention established (S-CAT-NN)
- [x] Universal scenario template defined
- [x] Step count and XP per difficulty confirmed
- [x] Decision option rules established (1 correct, 2–4 options, no joke options)
- [x] Feedback text format standardized
- [x] NIST phase allocation per step type confirmed
- [x] 18 badges designed with explicit criteria
- [x] XP economy fully balanced
- [x] Progress metrics defined
- [x] Consistency across categories verified
- [x] Difficulty progressions validated
- [x] Gamification scope confirmed (no over-engineering)
- [x] FYP suitability confirmed

---

## Agent Sign-Off — Scenario Architecture Phase Complete

| Agent | Domain | Status |
|---|---|---|
| Agent 1 | Learning Framework (11 stages, core loop) | ✅ Complete |
| Agent 2 | Scenario Hierarchy (6 categories, 30 scenarios) | ✅ Complete |
| Agent 3 | Scenario Flow Template (step spec, worked example) | ✅ Complete |
| Agent 4 | NIST SP 800-61 Integration Strategy | ✅ Complete |
| Agent 5 | Gamification (XP economy, 18 badges, progress design) | ✅ Complete |
| Agent 6 | Consistency Audit & Scalability Review | ✅ Complete |

---

> **Next Phase (Prompt 4)**: Database Design & Models — MySQL schema, Django model implementation, ERD, and complete database migration plan.
> All scenario architecture decisions finalized. Implementation begins next prompt.
