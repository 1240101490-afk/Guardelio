"""
Guardelio — Data Breach & Exfiltration Scenarios (S-DAT-01 to S-DAT-05)
NIST SP 800-61 Aligned Incident Response Simulations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# S-DAT-01: Customer Database via Misconfigured S3 Bucket (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DAT_01_OBJECTIVES = [
    (1, 'Inspect cloud storage bucket access control lists (ACLs) and IAM bucket policies.'),
    (2, 'Execute immediate access lockdown to stop ongoing public exposure.'),
    (3, 'Analyze CloudTrail and S3 access logs to determine if unauthorized exfiltration occurred.'),
]

S_DAT_01_STEPS = [
    {
        'step_number': 1,
        'title': 'The Responsible Disclosure Report',
        'situation_text': (
            'At 08:30 on Wednesday, the security inbox of TrendShop E-Commerce receives a vulnerability disclosure '
            'from an ethical security researcher. The report claims that an Amazon S3 bucket named `trendshop-production-customer-backups` '
            'is openly readable by anyone on the public internet without authentication.\n\n'
            'The researcher provided a screenshot showing unencrypted CSV files containing customer names, email addresses, '
            'physical addresses, hashed passwords, and order histories for over 2 million customers.\n\n'
            'You are the Cloud Security Analyst assigned to investigate and contain the breach.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Bucket Permission & Policy Audit',
        'situation_text': (
            'You inspect the AWS S3 Management Console for `trendshop-production-customer-backups`. You observe:\n\n'
            '- Bucket ACL: `Grantee: Everyone (public access) -> Read: Enabled`\n'
            '- S3 Block Public Access (BPA): Disabled at both the bucket and account level.\n'
            '- Bucket Policy: Includes a statement allowing `"Effect": "Allow", "Principal": "*", "Action": "s3:GetObject"`\n'
            '- Creation date of this policy: 14 days ago by a DevOps automation script during a database migration.\n\n'
            'What is the root cause of this exposure?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A misconfigured S3 bucket policy and public ACL combined with disabled S3 Block Public Access settings.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. The bucket policy explicitly allowed public wildcard (`*`) access and lacked Account-level Block Public Access (BPA) guards, '
                    'leaving the customer backup archives accessible to any unauthenticated web user.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'An attacker cracked the AWS root account password using brute force.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. CloudTrail logs show the policy was set by an internal DevOps script, not via root account password compromise.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Amazon AWS suffered an infrastructure outage that removed all bucket encryption.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Bucket permissions are customer-managed under the Cloud Shared Responsibility Model.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Immediate Emergency Containment',
        'situation_text': (
            'The exposure is confirmed and ongoing right now. Anyone with the bucket URL can download the 2 million customer database backup.\n\n'
            'What is your immediate containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable "Block all public access" at both the bucket and AWS account level immediately, and delete the public wildcard statement from the bucket policy.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Enabling S3 Block Public Access (BPA) and stripping the public wildcard statement instantly terminates all public web downloads, '
                    'containing the ongoing data exposure in seconds.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Delete the S3 bucket and all backup data files immediately.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting the entire bucket destroys production backup data and eliminates critical forensic S3 server access logs '
                    'needed to determine who downloaded the files.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Email the security researcher and ask them to delete their downloaded files before taking action.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Containment must happen immediately on the cloud infrastructure. Asking the researcher does not stop malicious scrapers '
                    'who may also be downloading the files.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Forensic Log Analysis & Exfiltration Scoping',
        'situation_text': (
            'Public access is blocked. You must now determine if malicious threat actors (beyond the reporting researcher) '
            'discovered and downloaded the customer backups during the 14-day window of exposure.\n\n'
            'You query S3 Server Access Logs and AWS CloudTrail via Amazon Athena:\n'
            '- Total `REST.GET.OBJECT` requests for `customer_dump_2026.csv.gz` from external IP addresses.\n'
            '- Result: 1 request from the researcher\'s IP (1.2 MB partial read), and 1 request from an IP associated with a known public data scraping tool (full 450 MB download 3 days ago).\n\n'
            'What does this forensic finding establish?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A confirmed data exfiltration breach occurred, necessitating formal regulatory breach notification and customer notification under GDPR / privacy laws.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. The full download by an unauthorized external scraping IP confirms unauthorized exfiltration occurred, '
                    'elevating the incident from a simple vulnerability exposure to a reportable data breach.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'No breach occurred because only one unauthorized IP downloaded the file.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A single full download of 2 million customer PII records constitutes a complete data exfiltration breach.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The file was compressed, so the contents cannot be read by anyone.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Gzip (`.gz`) is standard compression that anyone can decompress in seconds.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Cloud Governance Hardening',
        'situation_text': (
            'The misconfigured S3 bucket was locked down, the forensic download timeline was mapped, '
            'and the Data Protection Officer was provided with the full IP log report for statutory GDPR/ICO filing.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT TYPE: Unauthenticated Data Exfiltration via Misconfigured Public Cloud Storage.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: CloudTrail and S3 access log infrastructure readiness\n'
            '- Detection & Analysis: Bucket permission auditing, Athena access log query, exfiltration scoping\n'
            '- Containment: Account-level S3 Block Public Access activation, bucket policy remediation\n'
            '- Post-Incident Activity: Regulatory notification handoff, CI/CD policy enforcement\n\n'
            'GOVERNANCE HARDENING ACTIONS:\n'
            '1. Enforced AWS Organization Service Control Policies (SCP) preventing any S3 bucket from being created with public access.\n'
            '2. Integrated AWS Config and Security Hub automated rules to alert and auto-remediate public S3 buckets within 60 seconds.\n'
            '3. Mandated AWS KMS customer-managed key (CMK) encryption for all database backups at rest.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DAT-02: SQL Injection Breach on Healthcare Portal (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DAT_02_OBJECTIVES = [
    (1, 'Analyze web server access logs and database audit logs to confirm SQLi data exfiltration.'),
    (2, 'Implement emergency Web Application Firewall (WAF) virtual patching and code-level remediation.'),
    (3, 'Assess HIPAA / data privacy notification requirements for exfiltrated medical records.'),
]

S_DAT_02_STEPS = [
    {
        'step_number': 1,
        'title': 'Database Error Spike on Patient Portal',
        'situation_text': (
            'At 14:15 on Thursday, application monitoring for MedConnect Health Services triggers high-severity alerts:\n\n'
            '- Spike in HTTP 500 database syntax errors on the `/api/patient/records` endpoint.\n'
            '- Database server CPU spikes to 95%, with high outbound network transfer to an external cloud IP in Eastern Europe.\n'
            '- The portal handles sensitive Electronic Health Records (EHR), diagnostic reports, and medical histories for 50,000 patients.\n\n'
            'You are the Application Security Analyst on incident response duty.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Log Inspection & SQL Injection Confirmation',
        'situation_text': (
            'You pull web application logs and database query logs for the affected endpoint. You find:\n\n'
            'Web Request:\n'
            '`GET /api/patient/records?doctor_id=102+UNION+SELECT+null,patient_id,full_name,ssn,diagnosis_code,prescription_history+FROM+patient_medical_history--`\n\n'
            'Database Query Log:\n'
            'Executed raw query string concatenation: `SELECT id, doc_name FROM doctors WHERE id = 102 UNION SELECT ...`\n\n'
            'What vulnerability enabled this attack and what was its impact?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A Union-Based SQL Injection vulnerability caused by unsanitized dynamic SQL query concatenation, allowing direct extraction of the entire patient database.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Concatenating user input directly into SQL statements without parameterization allows attackers to inject `UNION SELECT` statements, '
                    'bypassing authentication and extracting arbitrary database tables.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A Cross-Site Scripting (XSS) vulnerability executing JavaScript in the doctor’s browser.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. XSS executes in the client browser. The logs show backend database SQL execution and data dumping.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A Cross-Site Request Forgery (CSRF) attack tricking the user into submitting a form.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. CSRF executes actions on behalf of authenticated users; it does not extract arbitrary database tables via SQL syntax injection.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Emergency Virtual Patching via WAF',
        'situation_text': (
            'The backend development team estimates that writing, testing, and deploying a secure code patch will take 3 hours. '
            'However, active automated tools (sqlmap) are continuing to query the endpoint and extract records.\n\n'
            'What is your immediate containment action to block the exploit in seconds without waiting for a code release?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy an emergency Web Application Firewall (WAF) virtual patch rule inspecting query parameters for SQL injection keywords (UNION, SELECT, --) and drop all matching traffic immediately.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. WAF virtual patching immediately blocks malicious SQL syntax at the network edge in seconds, '
                    'containing data exfiltration while giving developers time to build and test permanent code fixes.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Shut down the entire hospital datacenter electrical power.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Powering down hospital infrastructure disrupts critical patient life-support and clinical systems.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ask the database administrator to delete the patient table.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting the patient table destroys medical records and halts patient treatment.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Permanent Code-Level Remediation',
        'situation_text': (
            'The WAF virtual patch is actively blocking malicious requests. You now review the developer’s pull request '
            'to permanently eradicate the SQL injection vulnerability in the application source code.\n\n'
            'Which coding standard permanently prevents SQL injection vulnerabilities?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Use Parameterized Queries / Prepared Statements (or an ORM with parameterized binding), separating SQL query structure from user data.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Prepared statements ensure user input is treated strictly as data parameters, never as executable SQL commands, '
                    'completely neutralizing SQL injection regardless of user input characters.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Write a custom regex filter that replaces single quote characters (\') with double quotes (").',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Blacklist filtering and custom regex replacements are notoriously easy for attackers to bypass with alternative encodings and numeric injection.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Hide the API endpoint URL by renaming it from `/records` to `/secret_records_123`.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Security through obscurity provides zero defense against automated vulnerability scanners.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Data Breach Scope & Regulatory Impact Assessment',
        'situation_text': (
            'The parameterized code patch is deployed and verified. You analyze database audit logs to determine exact impact:\n\n'
            '- Total patient records returned in SQL query responses before WAF containment: 12,400 records.\n'
            '- Data fields exfiltrated: Full Name, Date of Birth, SSN/National ID, Diagnosis Codes, Prescription Histories.\n\n'
            'What legal and regulatory obligations are triggered by this exfiltration of Protected Health Information (PHI)?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Trigger statutory HIPAA / GDPR Breach Notification protocols: notify healthcare regulators within statutory deadlines, document forensic evidence, and notify all 12,400 affected patients.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Breach of Protected Health Information (PHI) exceeding regulatory thresholds mandates formal reporting '
                    'to regulatory authorities (e.g. HHS OCR / ICO) and direct written notification to affected patients.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Keep the incident confidential to protect the hospital’s commercial reputation.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Concealing a breach of health data violates HIPAA/GDPR law, carrying severe criminal penalties and multi-million dollar regulatory fines.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Only notify patients whose names start with the letter A to test the process.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. All individuals whose sensitive medical records were compromised must be notified under data privacy laws.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & DevSecOps Hardening',
        'situation_text': (
            'The SQL injection vulnerability has been eradicated, the application patched with parameterized queries, '
            'and the comprehensive forensic impact report handed over to legal and compliance officers.\n\n'
            'LESSONS LEARNED:\n\n'
            'VULNERABILITY: Unparameterized SQL Injection on patient records endpoint leading to PHI exfiltration.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Database query monitoring and WAF rule engine\n'
            '- Detection & Analysis: Database syntax error analysis, Union SQLi confirmation, Athena scoping\n'
            '- Containment: WAF virtual patching within 5 minutes\n'
            '- Eradication: Source code refactoring using Prepared Statements\n'
            '- Post-Incident Activity: Statutory HIPAA/GDPR regulator and patient notification handoff\n\n'
            'DEVSECOPS ENHANCEMENTS:\n'
            '1. Integrated Static Application Security Testing (SAST) in CI/CD pipeline to block unparameterized SQL queries in code review.\n'
            '2. Enforced database principle of least privilege: application database users restricted from viewing sensitive patient lookup tables directly.\n'
            '3. Configured column-level encryption (AES-256) for SSN and medical diagnosis fields at rest in the database.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DAT-03: Insider Data Theft Before Resignation (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DAT_03_OBJECTIVES = [
    (1, 'Analyze Data Loss Prevention (DLP) alerts, USB transfer logs, and cloud storage synchronization activity.'),
    (2, 'Coordinate with Legal and Human Resources while preserving strict forensic chain of custody.'),
    (3, 'Execute forensic disk imaging and revoke digital and physical access privileges.'),
    (4, 'Produce an admissible forensic investigation report.'),
]

S_DAT_03_STEPS = [
    {
        'step_number': 1,
        'title': 'The Anomaly in Research Lab 4',
        'situation_text': (
            'At 18:45 on a Friday, the DLP monitoring console at Quantum Research Institute flags an alert:\n\n'
            '- 4.8 GB of encrypted 7-Zip archives uploaded to a personal Google Drive account from workstation `WS-RES-09`.\n'
            '- The workstation is assigned to Dr. Marcus Vance, Principal Chemist, who submitted his two-week resignation notice yesterday.\n'
            '- Dr. Vance stated he was leaving for "personal reasons," but intelligence suggests he accepted an executive role with a major foreign competitor.\n\n'
            'You are the Digital Forensics Lead assigned to investigate potential intellectual property theft.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'DLP & Archive Metadata Analysis',
        'situation_text': (
            'You inspect the endpoint DLP telemetry and shadow-copy metadata for `WS-RES-09`. You discover:\n\n'
            '- Archive Name: `Project_Aether_Full_Schematics_2026.7z` (AES-256 encrypted).\n'
            '- Contents before compression: CAD blueprints, chemical synthesis formulas, and proprietary battery lab testing results.\n'
            '- Additional activity: A 128 GB SanDisk USB drive was connected to the workstation at 17:30 today, and 14 GB of data was copied.\n\n'
            'What is your immediate evidentiary assessment?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Substantial, premeditated intellectual property (IP) theft involving trade secrets, utilizing both cloud exfiltration and removable media transfer.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Archiving, encrypting, and transferring proprietary research blueprints to personal cloud and USB drives '
                    'immediately following resignation is textbook malicious insider IP exfiltration.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Standard routine backup of personal family vacation photos.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. File metadata explicitly lists CAD blueprints and chemical formulas from proprietary Project Aether repositories.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A network glitch duplicating temporary cache files.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The files were intentionally packed into a password-protected 7-Zip archive and transmitted across USB and cloud channels.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Legal, HR & Chain of Custody Protocol',
        'situation_text': (
            'Dr. Vance is still in the building working late in his office. You must act without compromising the legal chain of custody '
            'or giving the suspect opportunity to overwrite or destroy digital evidence.\n\n'
            'What is the mandatory first procedural step before approaching the employee?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Brief the General Counsel (Legal) and Head of HR, obtain formal investigation authorization, and coordinate a simultaneous physical badge and digital account suspension.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Insider investigations involving senior staff require legal and HR authorization to ensure compliance with labor laws '
                    'and preserve admissibility of evidence for civil injunctions and criminal proceedings.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Confront Dr. Vance alone in his office and demand he hand over his personal laptop.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Uncoordinated individual confrontation alerts the suspect, risking evidence destruction, physical altercation, or wrongful accusation claims.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Remotely send a popup message to Dr. Vance’s screen saying "You have been caught stealing."',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Warning the suspect allows them to delete cloud backups, wipe local drives, or damage hardware before evidence preservation.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Access Revocation & Evidence Preservation',
        'situation_text': (
            'Legal and HR authorize immediate intervention. HR and Security escort Dr. Vance from the laboratory to a private conference room.\n\n'
            'You arrive at `WS-RES-09` which is currently powered on and logged in.\n\n'
            'What is the forensic best-practice method for capturing evidence from a running live system?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Capture a live RAM memory dump first (e.g., using FTK Imager / WinPmem) to extract encryption keys and open sessions, then disconnect network cables and take a full bitstream physical drive image (E01/RAW) with SHA-256 hashing.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Volatile RAM contains active encryption keys, cloud session tokens, and recent file activity. '
                    'Capturing RAM before physical bitstream disk imaging preserves complete forensic chain of custody.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Pull the power plug immediately to stop the computer.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Pulling the power plug destroys all volatile memory (RAM), wiping out encryption keys and live connection evidence.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Log out of Windows, restart the computer, and run an antivirus scan.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Restarting and running antivirus modifies thousands of file system timestamps, corrupting the forensic timeline.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Removable Media & Cloud Forensics',
        'situation_text': (
            'During the HR interview, Dr. Vance surrenders the 128 GB USB drive. You inspect the drive with a hardware write-blocker:\n\n'
            '- USB contains identical copies of Project Aether CAD models.\n'
            '- File creation timestamps match the 17:30 transfer window.\n'
            '- Memory forensics from the RAM image extracts the 7-Zip password (`A3ther!2026#Vault`) used for the Google Drive archive.\n\n'
            'What legal and technical containment action should General Counsel immediately execute?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'File an emergency court injunction (Anton Piller / Temporary Restraining Order) and issue legal preservation notices to Google to freeze the personal cloud account and prevent disclosure to third parties.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. An emergency legal injunction paired with cloud provider preservation subpoenas legally compels the cloud provider '
                    'to freeze the data and restrains the suspect and competitor from utilizing the stolen trade secrets.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Log into Dr. Vance’s personal Google Drive using the extracted password and delete all files without telling anyone.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Accessing an employee’s personal account without legal process violates the Computer Misuse Act / CFAA and invalidates evidence in court.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Throw the USB drive in the laboratory incinerator.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Destroying physical evidence is illegal spoliation of evidence.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Forensic Reporting & Asset Verification',
        'situation_text': (
            'The court grants the emergency injunction. Google complies with the preservation order and freezes the personal drive.\n\n'
            'You must now compile the formal forensic report for the High Court and police investigators.\n\n'
            'What are the mandatory elements of an admissible digital forensics report?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Documented chain of custody, hardware/software write-blocker verification, cryptographic SHA-256 image hashes, chronological artifact timeline, and objective technical findings without speculative bias.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Admissible forensic reports must strictly adhere to ISO/IEC 27037 standards: verifiable chain of custody, '
                    'cryptographic hash validation, and objective factual presentation of digital artifacts.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Personal opinions about the employee’s moral character and salary negotiations.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Forensic reports must be strictly objective and technical; personal emotional opinions render reports inadmissible in legal proceedings.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A brief verbal summary given over coffee to the HR director.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Complex IP litigation requires formal written, hashed forensic documentation.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Trade Secret Protection',
        'situation_text': (
            'The insider threat investigation concluded with full recovery and legal impoundment of all stolen trade secrets. '
            'The competitor withdrew its job offer to Dr. Vance, and criminal trade secret theft charges were filed.\n\n'
            'LESSONS LEARNED:\n\n'
            'THREAT PROFILE: Pre-resignation trade secret exfiltration using mass compression, personal cloud storage, and removable USB drives.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Endpoint DLP and shadow-copy auditing capabilities\n'
            '- Detection & Analysis: High-volume upload detection, archive payload inspection\n'
            '- Containment: Inter-departmental coordination (Legal/HR), live RAM acquisition, physical device seizure\n'
            '- Eradication: Court injunction, cloud account preservation subpoena\n'
            '- Recovery: Admissible ISO 27037 forensic case documentation\n'
            '- Post-Incident Activity: Data Loss Prevention (DLP) architecture upgrade\n\n'
            'INSTITUTIONAL POLICY UPGRADES:\n'
            '1. Enforced hardware USB storage blocking (read-only / full block) across all scientific workstations.\n'
            '2. Implemented automated elevated DLP monitoring triggered whenever an employee submits resignation notices.\n'
            '3. Deployed Information Rights Management (IRM) watermarking on all proprietary CAD and chemical synthesis blueprints.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DAT-04: Third-Party Vendor Breach Affecting You (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DAT_04_OBJECTIVES = [
    (1, 'Evaluate third-party vendor incident notifications and assess downstream blast radius.'),
    (2, 'Identify specific data elements exposed and cross-reference employee impact scope.'),
    (3, 'Execute vendor containment protocols, identity protection provisions, and regulatory disclosures.'),
]

S_DAT_04_STEPS = [
    {
        'step_number': 1,
        'title': 'The Vendor Breach Notification',
        'situation_text': (
            'At 11:00 AM on Monday, Allied Financial Group receives an urgent formal breach notification from PayMaster Cloud Solutions, '
            'the third-party SaaS vendor managing Allied’s global employee payroll and tax filings.\n\n'
            'The notification states that an unauthorized threat actor accessed PayMaster’s central database 10 days ago '
            'via a compromised administrator credential, exfiltrating 12 months of payroll records.\n\n'
            'You are the Third-Party Risk Management (TPRM) Security Analyst leading the investigation.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Data Mapping & Blast Radius Assessment',
        'situation_text': (
            'You review the Data Processing Agreement (DPA) and data synchronization pipelines between Allied Financial and PayMaster. '
            'You audit the fields transferred via API over the last 12 months:\n\n'
            '- Employee Full Legal Names, Home Addresses, Dates of Birth\n'
            '- National Insurance / Social Security Numbers (SSN)\n'
            '- Bank Account Numbers and Sort Codes\n'
            '- Monthly Salary, Bonus Records, and Tax Deduction Details\n'
            '- Total active Allied Financial employees affected: 1,850 staff members + 320 former employees.\n\n'
            'What is the primary risk posed to the affected employees?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Severe identity theft, fraudulent bank account diversion, unauthorized credit line applications, and highly targeted spear-phishing attacks.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. The combination of SSNs, banking details, dates of birth, and compensation data provides identity thieves '
                    'with complete packages for financial account takeovers and fraudulent credit generation.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Minimal risk because the data was stored on the vendor’s servers, not Allied Financial’s internal servers.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. As the Data Controller, Allied Financial bears legal and operational responsibility for data entrusted to third-party Data Processors.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The only risk is that employees might receive spam marketing flyers in the mail.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Banking numbers and SSNs carry severe financial fraud and identity theft risk.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Vendor Containment & API Token Revocation',
        'situation_text': (
            'While PayMaster works on their internal remediation, you must protect Allied Financial’s remaining active systems '
            'from any ongoing compromise vector originating from the vendor.\n\n'
            'What is your immediate technical containment step regarding Allied\'s integration with PayMaster?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Immediately revoke all active API keys, OAuth tokens, and SFTP credentials connecting Allied Financial to PayMaster, suspending automated data synchronization until security verification is complete.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Severing API integrations and revoking shared authentication credentials stops ongoing automated data feeds '
                    'and isolates Allied Financial from potential lateral compromise from the vendor’s network.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Continue sending daily employee payroll updates to PayMaster as normal so nobody misses payday.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Continuing automated data transmission to an actively compromised vendor continuously leaks new employee records.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the internal Active Directory accounts of all 1,850 employees.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting employee internal accounts shuts down all company business operations and does nothing to mitigate the vendor breach.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Employee Protection & Breach Notification Rollout',
        'situation_text': (
            'API tokens are revoked. Executive leadership and General Counsel approve direct employee notification.\n\n'
            'What comprehensive protection package should Allied Financial provide to all affected staff?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Transparent written breach notification explaining the exposed data fields, 24 months of complimentary credit monitoring and identity theft protection, and direct coordination with employee banking institutions.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Industry standard breach response requires prompt, transparent notification detailing specific exposed fields '
                    'and providing credit monitoring/dark-web surveillance services to mitigate financial harm to individuals.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send an email telling employees not to look at their bank accounts for the next 6 months.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Employees must actively monitor their accounts; telling them to ignore accounts guarantees undetected fraud.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Offer employees a £5 cafeteria voucher as compensation.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Trivializing a severe identity breach damages employee trust and violates regulatory expectations.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Vendor Security Audit & Re-Integration Criteria',
        'situation_text': (
            'PayMaster notifies you that they have eradicated the threat and want to resume the payroll API connection.\n\n'
            'What technical evidence must Allied Financial require from PayMaster before restoring any data transmission?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Require an independent third-party incident forensic report, evidence of MFA enforcement on all administrative access, a clean SOC 2 Type II audit report, and proof of penetration testing remediation.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. TPRM governance mandates independent forensic verification and certified third-party security audits '
                    'before re-establishing trusted data connections with a previously breached vendor.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Accept a verbal phone assurance from the vendor sales representative.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Verbal assurances from sales staff have zero technical or legal validity.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ask the vendor to pay Allied Financial £1,000,000 cash before turning the API back on.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Commercial negotiations do not verify technical security posture or ensure system safety.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & Supply Chain Resilience',
        'situation_text': (
            'The third-party payroll breach response is complete. All 2,170 current and former staff received '
            'identity protection enrollment, statutory notifications were filed with data regulators, and vendor audit controls were updated.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT TYPE: Downstream Data Exposure via Compromised SaaS Payroll Vendor (Supply Chain Breach).\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Third-Party Risk Management (TPRM) data mapping\n'
            '- Detection & Analysis: Vendor notification triage, blast radius calculation (1,850 active + 320 alumni)\n'
            '- Containment: Immediate API/OAuth credential revocation and data sync freeze\n'
            '- Eradication: Employee identity protection rollout, regulator reporting\n'
            '- Recovery: Independent forensic audit verification before re-integration\n'
            '- Post-Incident Activity: Vendor contract security clause review\n\n'
            'SUPPLY CHAIN GOVERNANCE ENHANCEMENTS:\n'
            '1. Added mandatory breach notification SLAs (under 24 hours) in all vendor Data Processing Agreements (DPA).\n'
            '2. Implemented automated continuous third-party cyber risk scoring (e.g. BitSight / SecurityScorecard).\n'
            '3. Enforced data field tokenization, ensuring vendor payroll databases store masked bank details where possible.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DAT-05: GDPR Breach Notification Under 72 Hours (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DAT_05_OBJECTIVES = [
    (1, 'Assess GDPR Article 33 and Article 34 statutory notification triggers based on data sensitivity and risk.'),
    (2, 'Execute the 72-hour regulatory notification timeline with supervisory authorities (ICO / CNIL).'),
    (3, 'Coordinate remote device wipe, credential revocation, and public communications.'),
    (4, 'Institute mandatory full-disk encryption (BitLocker) and Mobile Device Management (MDM) enforcement.'),
]

S_DAT_05_STEPS = [
    {
        'step_number': 1,
        'title': 'The Lost Executive Laptop on the Train',
        'situation_text': (
            'At 07:15 on a Tuesday, the Operations Director at EuroPost Logistics calls the IT Helpdesk. '
            'While commuting on the London to Manchester train, his laptop bag was stolen from the overhead luggage rack.\n\n'
            'The laptop was an older legacy device that had been manually exempted from the mandatory BitLocker encryption policy '
            'due to a driver compatibility issue. The laptop hard drive contains unencrypted local copies of:\n'
            '- 150,000 customer parcel delivery records (names, home addresses, phone numbers, signature scans)\n'
            '- Keycode entry codes for 12,000 residential apartment building access gates across the UK\n\n'
            'You are the Data Protection Officer (DPO) leading the statutory breach response.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'GDPR Article 33 72-Hour Clock Trigger',
        'situation_text': (
            'Under Article 33 of the General Data Protection Regulation (GDPR / UK GDPR), the statutory clock starts '
            'the moment the data controller becomes "aware" of a personal data breach.\n\n'
            'What is the mandatory statutory timeframe to notify the supervisory authority (Information Commissioner\'s Office — ICO)?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Within 72 hours of becoming aware of the breach, where the breach is likely to result in a risk to the rights and freedoms of natural persons.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. GDPR Article 33 strictly mandates notification to the relevant supervisory authority (ICO) '
                    'without undue delay and, where feasible, not later than 72 hours after becoming aware of the breach.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Within 30 calendar days of completing all internal disciplinary hearings.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. 30 days violates the statutory 72-hour Article 33 deadline and triggers severe regulatory fines.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Notification is only required if the thief posts the data on Twitter/X.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The physical loss of unencrypted personal data and building security access codes constitutes a breach immediately upon loss.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Assessing "High Risk" to Data Subjects (Article 34)',
        'situation_text': (
            'You analyze the data categories exposed on the unencrypted drive: residential delivery addresses '
            'combined with private building gate entry codes and resident contact numbers.\n\n'
            'Does this breach trigger GDPR Article 34 mandatory communication directly to affected data subjects?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Yes. Because the unencrypted data includes physical residential gate access codes and home addresses, it poses a "high risk" of physical burglary and harassment, triggering mandatory direct notification without undue delay.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Under GDPR Article 34, when a breach poses a "high risk" to the rights and freedoms (including physical safety/security) '
                    'of individuals, the controller must communicate the breach directly to all affected individuals.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'No. Direct notification is never required as long as the ICO is notified.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. High-risk breaches mandate direct individual notification under Article 34 in addition to regulatory Article 33 notification.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'No. Gate keycodes are not considered personal data under any circumstances.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Gate codes linked directly to identifiable residential names and addresses create severe personal security risks.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Immediate Technical Containment & Wipe Command',
        'situation_text': (
            'The Operations Director’s laptop is enrolled in Microsoft Intune (MDM). '
            'The laptop is currently offline, but may connect to the internet if the thief powers it on.\n\n'
            'What technical containment commands must you execute immediately in the MDM console?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Issue an immediate remote "Wipe Device" command in Intune, revoke all Microsoft 365 / Entra ID active session tokens, and reset the user\'s credentials and certificates.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Issuing an emergency remote wipe ensures that the moment the device connects to Wi-Fi/cellular, all local partitions are wiped, '
                    'while token revocation immediately prevents cloud resource access.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Wait for the laptop battery to drain completely before issuing any commands.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Delaying the remote wipe gives the thief opportunity to extract the unencrypted hard drive and read files offline.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the device from Intune so it no longer appears in the company inventory.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting the device from MDM unenrolls it and permanently removes your ability to trigger the remote wipe command.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Formulating the Statutory ICO Article 33 Report',
        'situation_text': (
            'You are at Hour 24 of the 72-hour window. You draft the formal regulatory notification to the ICO.\n\n'
            'What required information must be included in the formal Article 33 notification document?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Nature of the breach, categories and approximate number of data subjects and records, DPO contact details, likely consequences/risks, and mitigation measures taken/proposed.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. GDPR Article 33(3) explicitly lists these mandatory disclosure criteria. Providing complete, structured information '
                    'demonstrates organizational accountability and compliance.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The home address and salary of the IT Helpdesk technician who forgot to enable BitLocker.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Regulatory filings focus on organizational risk, data categories, and mitigation, not internal employee scapegoating.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A request asking the ICO to send police officers to search the train.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The ICO is a regulatory supervisory authority, not a physical police emergency dispatch service.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Physical Risk Remediation & Keycode Rotation',
        'situation_text': (
            'In parallel with the Article 34 individual notices, EuroPost Logistics must mitigate the physical security risk '
            'posed by the 12,000 exposed building residential gate codes.\n\n'
            'What immediate remediation action must the operations team execute with property managers?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Issue urgent notices to all residential property building managers requesting an immediate reprogram/rotation of physical access keycodes, and transition delivery drivers to dynamic one-time OTP gate access.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Rotating the physical gate keycodes directly neutralizes the security threat to residents, '
                    'preventing unauthorized individuals from using stolen codes for building access.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Leave the gate codes unchanged because the thief probably cannot read English.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Assuming an adversary cannot utilize stolen plain-text security data is catastrophic negligence.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Post the 12,000 gate codes on a public message board so residents know which ones were compromised.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Publishing gate codes publicly exposes all 12,000 buildings to immediate burglary risk.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Compliance Closure',
        'situation_text': (
            'The GDPR Article 33 filing was submitted at Hour 36 (well within the 72-hour window). '
            'All 12,000 residential gate codes were rotated, and the ICO commended EuroPost for its rapid mitigation and transparent response.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT PROFILE: Physical theft of unencrypted endpoint containing 150K customer records and physical access security codes.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: DPO statutory escalation readiness\n'
            '- Detection & Analysis: High-risk Article 33 and Article 34 assessment\n'
            '- Containment: Intune remote wipe trigger, cloud session revocation\n'
            '- Eradication: Article 33 ICO statutory filing within 36 hours\n'
            '- Recovery: Article 34 customer notifications and 12,000 building keycode rotation\n'
            '- Post-Incident Activity: Elimination of encryption policy exemptions\n\n'
            'ENTERPRISE COMPLIANCE REMEDIATION:\n'
            '1. Permanently abolished all local encryption policy exemption waivers system-wide.\n'
            '2. Enforced Conditional Access: Intune device compliance (BitLocker Active + TPM 2.0) mandatory to access company email or files.\n'
            '3. Replaced static local spreadsheet storage of gate codes with an encrypted, ephemeral API that delivers one-time time-expiring codes to drivers.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]

DATA_BREACH_SCENARIOS = {
    'S-DAT-01': (S_DAT_01_OBJECTIVES, S_DAT_01_STEPS),
    'S-DAT-02': (S_DAT_02_OBJECTIVES, S_DAT_02_STEPS),
    'S-DAT-03': (S_DAT_03_OBJECTIVES, S_DAT_03_STEPS),
    'S-DAT-04': (S_DAT_04_OBJECTIVES, S_DAT_04_STEPS),
    'S-DAT-05': (S_DAT_05_OBJECTIVES, S_DAT_05_STEPS),
}
