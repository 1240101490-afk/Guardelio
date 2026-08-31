"""
Guardelio — Insider Threat Detection Scenarios (S-INS-01 to S-INS-05)
NIST SP 800-61 Aligned Incident Response Simulations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# S-INS-01: Disgruntled Employee Sabotaging Systems (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_INS_01_OBJECTIVES = [
    (1, 'Recognize indicators of post-termination sabotage in system logs and authentication traces.'),
    (2, 'Execute immediate inter-departmental privilege termination workflows.'),
    (3, 'Verify backup immutability and file system integrity after destructive sabotage commands.'),
]

S_INS_01_STEPS = [
    {
        'step_number': 1,
        'title': 'The Midnight Deletion Alert',
        'situation_text': (
            'At 23:45 on a Wednesday, the automated SIEM console at Omega Logistics generates a critical alert:\n\n'
            '- High-rate file deletion commands (`rm -rf /var/log/*`, `rm -rf /opt/dispatch/data/*`) executed on the central dispatch staging server.\n'
            '- Over 8,000 active delivery routes and customer manifests have been erased in the last 15 minutes.\n'
            '- The session was established via SSH using the credentials of user `g.harrison`.\n\n'
            'You are the SOC Analyst on the night shift.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'User Context & Identity Correlation',
        'situation_text': (
            'You check Active Directory and HR identity records for `g.harrison` (Greg Harrison, Junior Linux Admin). You discover:\n\n'
            '- Greg Harrison was formally terminated for gross misconduct at 16:30 today.\n'
            '- HR submitted a deprovisioning ticket at 16:45, but the helpdesk queue had a 24-hour backlog, leaving his accounts active.\n'
            '- Physical security logs show his building keycard was swiped at the side entrance at 23:30 tonight.\n\n'
            'What type of security incident are you facing?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A malicious insider sabotage attack by a terminated employee exploiting delayed IT deprovisioning and unrevoked physical building access.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. A recently fired employee using active credentials and physical access to systematically destroy operational files '
                    'is a classic malicious insider sabotage incident. Failure to synchronize HR offboarding with immediate IT access revocation is the root operational flaw.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'An automated Linux kernel package update running routine cleanup cron jobs.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Cron updates do not execute interactive `rm -rf` commands across customer data folders under an individual employee’s login.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A DDoS attack from an external botnet in China.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The attack was executed locally inside the building using legitimate internal SSH credentials.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Immediate Account & Physical Containment',
        'situation_text': (
            'Greg Harrison is still actively logged into the server and may be currently inside the server room or offices.\n\n'
            'What is your immediate two-pronged containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Terminate all active SSH sessions for `g.harrison`, immediately disable his Active Directory and SSH keys, and alert on-site physical security guards to locate and escort him off the premises.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Immediate digital account suspension combined with active session termination (`pkill -u g.harrison`) and physical security intervention '
                    'stops both logical data destruction and unauthorized on-premise physical tampering.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send an email to Greg asking him to stop deleting files.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Emailing an active saboteur will only accelerate their destructive actions.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Wait until normal office opening hours at 09:00 AM to raise a ticket with the helpdesk.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Delaying response for hours allows the saboteur to wipe all corporate servers and backup stores.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Data Recovery & Backup Immutability Verification',
        'situation_text': (
            'Physical security detains Harrison in the 2nd-floor breakroom and police are called. '
            'His digital sessions have been terminated. You must now recover the 8,000 deleted delivery manifests before morning operations at 06:00.\n\n'
            'What is the correct recovery procedure?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Restore the dispatch database and manifests from an immutable, write-once-read-many (WORM) offline backup snapshot taken at 22:00, and verify SHA-256 data integrity.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Restoring from an immutable/WORM backup snapshot taken prior to the sabotage window guarantees full data recovery '
                    'that the rogue insider could not tamper with or delete.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Call all 8,000 customers on the phone and ask them to re-order their shipments manually.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Unrealistic and destructive to business operations when healthy backups are available.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Offer Harrison his job back if he undeletes the files.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Rewarding extortion and criminal sabotage is completely unacceptable.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Offboarding Automation',
        'situation_text': (
            'Dispatch manifests were completely restored by 03:30 AM with zero customer delay. '
            'Harrison was arrested and charged under the Computer Misuse Act.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT PROFILE: Malicious Insider Sabotage resulting from asynchronous HR-to-IT offboarding delay.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: SIEM file deletion threshold alerting\n'
            '- Detection & Analysis: User context correlation, physical badge entry matching\n'
            '- Containment: Immediate active session termination, AD/SSH revocation, physical security intervention\n'
            '- Eradication: Immutable snapshot data restoration\n'
            '- Post-Incident Activity: Offboarding integration redesign\n\n'
            'GOVERNANCE REMEDIATION:\n'
            '1. Integrated HR Information System (HRIS) directly with Active Directory/Okta to automate instant account deactivation upon termination.\n'
            '2. Linked HR termination events to physical building access control to revoke building badges simultaneously.\n'
            '3. Restricted Linux root/sudo privilege delegation and enforced strict command logging on all staging/production hosts.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-INS-02: Privileged Account Abuse by System Admin (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_INS_02_OBJECTIVES = [
    (1, 'Detect anomalous privileged account behavior using User and Entity Behavior Analytics (UEBA).'),
    (2, 'Conduct discreet, non-invasive investigation without tipping off the privileged subject.'),
    (3, 'Apply the principle of least privilege (PoLP) and Just-In-Time (JIT) administrative access controls.'),
]

S_INS_02_STEPS = [
    {
        'step_number': 1,
        'title': 'The UEBA Anomaly Alert',
        'situation_text': (
            'At 03:30 on a Sunday morning, the User and Entity Behavior Analytics (UEBA) platform at SecureBank UK '
            'triggers a critical risk score (98/100) on senior infrastructure engineer `j.smith` (John Smith).\n\n'
            'Over the past 3 weeks, John has used his Global Domain Administrator credentials to execute unauthorized '
            '`Search-Mailbox` and `New-MailboxExportRequest` commands across Microsoft Exchange, exporting complete mailbox PST files '
            'for the Chief Executive Officer, Chief Risk Officer, and Head of M&A.\n\n'
            'You are the Insider Threat Analyst assigned to investigate.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Change Management & Authorization Audit',
        'situation_text': (
            'Before reaching any conclusion, you must determine whether these mailbox exports were part of an authorized legal hold '
            'or scheduled IT maintenance window.\n\n'
            'You check the ServiceNow ITSM Change Database and Legal Hold registry. You observe:\n\n'
            '- Zero change requests or maintenance tickets exist for C-suite mailbox exports.\n'
            '- Zero legal holds or compliance eDiscovery requests are assigned to John Smith.\n'
            '- The exported `.pst` archives were copied to an encrypted local VHD volume on John Smith\'s administrative jump box.\n\n'
            'What does this discrepancy confirm?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Unauthorized privileged account abuse and unauthorized access to executive confidential communications, constituting a high-severity insider threat.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Accessing and exporting executive communications without an authorized change ticket, legal hold, or business justification '
                    'is a direct violation of bank policy and the Computer Misuse Act.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Standard automated Exchange maintenance that runs on all mailboxes every weekend.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Automated maintenance does not export `.pst` files of specific C-suite executives to a hidden local VHD volume.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A false positive triggered by an antivirus signature update.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Exchange PowerShell audit logs definitively record specific manual command executions by user `j.smith`.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Silent Monitoring vs. Immediate Revocation Strategy',
        'situation_text': (
            'John Smith has Domain Admin rights and could delete audit logs, wipe domain controllers, or destroy evidence if he realizes he is under investigation.\n\n'
            'How should the security team proceed with containment without tipping off the administrator prematurely?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable out-of-band immutable SIEM log mirroring (ensuring local log tampering is impossible), preserve forensic jump box disk snapshots silently, and coordinate a synchronized suspension with HR and Legal.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Privileged insiders possess the power to alter logs. Mirroring logs to an immutable repository '
                    'and snapshotting artifacts silently prevents the subject from destroying evidence prior to formal interview.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send a Slack message to the IT team channel asking "Why is John reading the CEO\'s email?"',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Publicly broadcasting the investigation alerts the suspect, who can wipe their jump box and delete logs in seconds.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Change John Smith\'s password and leave a note on his desk.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Tipping off a domain administrator without first securing evidence snapshots risks catastrophic retaliatory sabotage.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Executing Coordinated Privilege Revocation',
        'situation_text': (
            'Forensic jump box snapshots and immutable log archives are secured. On Monday morning at 09:00, '
            'HR and Legal summon John Smith to an executive conference room for an interview.\n\n'
            'What synchronized technical containment actions must occur the moment John enters the meeting room?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Revoke all Domain Admin and privileged role memberships, terminate all active RDP/SSH/VPN sessions, disable his smartcard/Active Directory accounts, and revoke his physical building access.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Synchronizing full digital privilege revocation with the physical HR interview eliminates the insider’s ability '
                    'to execute revenge commands or access sensitive systems.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Demote his account from Domain Admin to Server Admin and let him continue working.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Allowing an employee under active investigation for unauthorized executive surveillance to retain administrative rights is extreme negligence.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Only change his email password so he cannot send messages.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Domain Admin credentials grant full access to all network infrastructure regardless of email access.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Architectural Remediation: Privileged Access Management (PAM)',
        'situation_text': (
            'The investigation revealed that John Smith was attempting to gather insider trading intelligence on an upcoming bank merger. '
            'He was dismissed and referred to the Financial Conduct Authority (FCA).\n\n'
            'What architectural control prevents single administrators from accessing executive mailboxes unilaterally in the future?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy Privileged Access Management (PAM) with Just-In-Time (JIT) access, dual-custody authorization (four-eyes principle), and complete session recording for all administrative operations.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. PAM with dual-custody ensures no single administrator can gain access to sensitive mailboxes or databases '
                    'without real-time secondary manager approval and full session recording.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ask all sysadmins to sign a paper promise that they will only look at their own emails.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Paper policies without technical enforcement controls fail against malicious insiders.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Eliminate all IT administrator positions and outsource all management to unvetted contractors.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Unvetted third parties increase insider threat risks exponentially.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & Privileged Governance',
        'situation_text': (
            'The privileged insider threat investigation concluded with zero data exfiltration to external third parties. '
            'The FCA and ICO were notified, and the bank’s privileged access architecture was overhauled.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT TYPE: Privileged Account Abuse & Executive Surveillance by Internal Domain Administrator.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: UEBA anomaly detection deployment\n'
            '- Detection & Analysis: Baseline deviation correlation, ITSM/eDiscovery authorization audit\n'
            '- Containment: Silent immutable log preservation, synchronized HR interview revocation\n'
            '- Eradication: Privilege stripping, local jump box forensic isolation\n'
            '- Post-Incident Activity: PAM and Four-Eyes policy enforcement\n\n'
            'ARCHITECTURAL ENHANCEMENTS:\n'
            '1. Implemented CyberArk PAM: standing Domain Admin accounts eliminated in favor of ephemeral, JIT credential checkouts.\n'
            '2. Enforced Dual-Custody Approval on Exchange Application Impersonation and eDiscovery role assignment.\n'
            '3. Configured automated real-time alerts to the CISO whenever executive mailboxes are accessed by any administrative account.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-INS-03: Contractor Selling Access to Dark Web (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_INS_03_OBJECTIVES = [
    (1, 'Correlate external dark web threat intelligence leads with internal authentication logs.'),
    (2, 'Identify rogue third-party contractor accounts operating outside authorized project scopes.'),
    (3, 'Coordinate with national cybercrime law enforcement (NC3 / FBI) for criminal evidence preservation.'),
    (4, 'Isolate contractor network segments and enforce Zero Trust Network Access (ZTNA).'),
]

S_INS_03_STEPS = [
    {
        'step_number': 1,
        'title': 'The Dark Web Intelligence Lead',
        'situation_text': (
            'At 15:00 on Tuesday, an external threat intelligence partner alerts the SOC at Nexus Defence Technologies. '
            'A verified dark web broker on a Russian cybercrime forum posted a listing:\n\n'
            '"[FOR SALE] Active High-Privilege Corporate VPN + RDP Access into UK Defence Contractor (Nexus Defence). '
            'Includes Active Subnets, Internal CAD Repositories, and Admin Credentials. Price: $15,000 in Monero (XMR)."\n\n'
            'The listing includes a proof screenshot showing an internal desktop with hostname `DEV-JUMP-04.nexusdefence.local`.\n\n'
            'You are the Lead Threat Hunter leading the emergency investigation.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Internal Asset & Account Correlation',
        'situation_text': (
            'You query Active Directory and network inventory for `DEV-JUMP-04`. You find:\n\n'
            '- Assigned User: `c_vanguard_dev` (Third-party software engineering contractor from Vanguard Software Ltd).\n'
            '- Contract Scope: Authorized strictly to maintain unclassified logistics billing software in VLAN 40.\n'
            '- Active Connections: The account has been actively connecting via VPN from external residential IPs in London and Munich.\n\n'
            'What is your immediate correlation assessment?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A rogue contractor (or a contractor whose credentials were sold/compromised) is brokering unauthorized initial access into the defense network.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. The matching internal hostname in the dark web screenshot paired with anomalous multi-location VPN logins '
                    'confirms active access monetization of defense contractor credentials.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A fake dark web scam that has nothing to do with Nexus Defence.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The screenshot contains genuine internal hostnames and network topology diagrams that could only originate from inside the network.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'An automated marketing campaign by Vanguard Software.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Selling access for Monero on cybercrime forums is serious criminal activity, not corporate marketing.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Lateral Movement & Reconnaissance Scoping',
        'situation_text': (
            'You audit internal firewall traffic and NetFlow telemetry for `DEV-JUMP-04` over the past 14 days. You uncover:\n\n'
            '- Port scanning executed across VLAN 10 (Classified Missile Guidance Systems) and VLAN 20 (Propulsion R&D).\n'
            '- SMB shares accessed: `\\\\CLASSIFIED-FS01\\Aero_Guidance_2026`\n'
            '- Tools detected in user AppData: `nmap.exe`, `mimikatz.exe`, and `bloodhound.exe`.\n\n'
            'What does this toolset and activity indicate?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Active internal reconnaissance, lateral movement, and credential dumping far outside the contractor\'s billing software scope, preparing an extensive access package for buyers.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Deploying Mimikatz, BloodHound, and Nmap across classified defense VLANs confirms deliberate malicious insider espionage and reconnaissance.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Standard routine billing software maintenance procedures.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Mimikatz and BloodHound are penetration testing and credential harvesting tools that have zero place in logistics billing.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The contractor was playing an online multiplayer video game.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Network telemetry and tool names reflect offensive cyber reconnaissance, not video gaming.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Emergency Network Isolation & Session Termination',
        'situation_text': (
            'The threat is critical. The contractor account is currently logged into `DEV-JUMP-04` via VPN.\n\n'
            'What is your immediate containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Sever the active VPN tunnel immediately, revoke all Vanguard contractor accounts in Active Directory, isolate `DEV-JUMP-04` on the network via EDR, and preserve volatile memory (RAM) on the host.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Instantly cutting the VPN session and isolating the host stops ongoing reconnaissance or exfiltration, '
                    'while RAM capture preserves active Mimikatz processes and C2 channels for criminal prosecution.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Allow the contractor to keep working until the end of his monthly billing cycle.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Allowing active espionage on defense systems risks catastrophic compromise of classified national security data.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Reboot all domain controllers in the entire company.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Rebooting DCs does not revoke the contractor\'s VPN tunnel or isolate the compromised jump box.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Law Enforcement & National Security Escalation',
        'situation_text': (
            'Because Nexus Defence Technologies holds Ministry of Defence (MoD) contracts, this breach involves national security.\n\n'
            'What formal regulatory and law enforcement escalation path is mandatory?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Notify the National Cyber Security Centre (NCSC), MoD Defence Cyber Protection, and the National Crime Agency (NCA) Cyber Crime Unit, submitting the hashed forensic evidence package.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Breaches involving defense infrastructure mandate statutory escalation to defense security authorities (NCSC / MoD) '
                    'and national cybercrime units for international criminal prosecution.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Keep the incident secret and fire Vanguard Software quietly.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Concealing defense sector breaches violates defense procurement contracts and national security legislation.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Create a dark web account and purchase the access listing for $15,000 to see who is selling it.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Security analysts must never engage in unauthorized financial transactions with dark web cybercrime brokers.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Full Network Compromise Assessment & Eradication',
        'situation_text': (
            'NCA and MoD investigators take over the physical suspect investigation. You must ensure no backdoors, '
            'scheduled tasks, or secondary web shells were planted across classified network segments.\n\n'
            'What technical eradication and verification actions must be conducted?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Execute enterprise-wide threat hunting for IoCs extracted from DEV-JUMP-04, reimage all jump boxes, rotate the Kerberos KRBTGT password twice, and enforce Zero Trust Network Access (ZTNA) with strict micro-segmentation.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Complete eradication requires hunting for secondary footholds, rotating KRBTGT to invalidate forged Golden Tickets, '
                    'rebuilding jump hosts, and implementing ZTNA micro-segmentation to restrict third-party access strictly to required IPs.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Only delete the files inside `C:\\Windows\\Temp\\` on the contractor\'s jump host.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Surface cleanup ignores potential persistence mechanisms planted across classified servers.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Turn off all internal firewalls so all traffic flows faster.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Turning off internal firewalls destroys network segmentation completely.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Supply Chain Defense',
        'situation_text': (
            'The rogue contractor was arrested by the NCA in London. Forensic evidence proved he attempted to sell '
            'defense access to foreign buyers. The dark web listing was closed and zero classified schematics were transferred.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT PROFILE: Third-Party Contractor Access Monetization & Malicious Reconnaissance.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Dark web threat intelligence monitoring integration\n'
            '- Detection & Analysis: Hostname correlation, lateral movement tool identification (BloodHound/Mimikatz)\n'
            '- Containment: VPN termination, jump host EDR isolation, live RAM forensics\n'
            '- Eradication: National security escalation (NCSC/NCA), enterprise KRBTGT rotation\n'
            '- Recovery: Enterprise IoC hunting, ZTNA micro-segmentation enforcement\n'
            '- Post-Incident Activity: Supply chain security architecture overhaul\n\n'
            'STRATEGIC DEFENSE ENHANCEMENTS:\n'
            '1. Abolished broad VPN access for contractors; replaced with agentless ZTNA restricting access to single port/application scopes.\n'
            '2. Enforced hardware FIDO2 keys and company-managed Compliant Laptops for all third-party developers.\n'
            '3. Configured automated EDR network isolation upon detection of offensive tools (BloodHound, Nmap, Mimikatz).'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-INS-04: Accidental Data Leak by Negligent Employee (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_INS_04_OBJECTIVES = [
    (1, 'Distinguish between accidental data spills and malicious insider intent.'),
    (2, 'Execute mail gateway message recall and purge operations across email servers.'),
    (3, 'Deploy Data Loss Prevention (DLP) auto-blocking rules for sensitive keyword patterns.'),
]

S_INS_04_STEPS = [
    {
        'step_number': 1,
        'title': 'The Distressed Paralegal',
        'situation_text': (
            'At 16:30 on a Friday, an extremely distressed paralegal at Citywide Legal Services calls the IT Security Desk. '
            'She was attempting to email an unredacted litigation settlement spreadsheet titled `Q3_Client_Payouts_Confidential.xlsx` '
            'to a partner in her department.\n\n'
            'Due to Outlook email address auto-complete, she accidentally selected the broad distribution list '
            '`All_Partners_And_External_Affiliates@citywidelegal.com` which includes 320 internal staff and 45 external commercial partner addresses.\n\n'
            'The spreadsheet contains names, bank details, National Insurance numbers, and settlement payouts for 450 clients.\n\n'
            'You are the Information Security Advisor on duty.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Intent Assessment & Spill Scoping',
        'situation_text': (
            'You review the message headers and email gateway logs in Microsoft 365 Exchange Online. You confirm:\n\n'
            '- The message was dispatched 4 minutes ago.\n'
            '- Recipient count: 320 internal mailboxes, 45 external external recipient domains.\n'
            '- The paralegal immediately self-reported the error and is cooperating fully.\n\n'
            'What type of security incident is this?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'An unintentional/negligent data spill (accidental insider leak) requiring rapid administrative message recall and external containment.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Unintentional misdirection of sensitive data due to auto-complete errors is a very common accidental insider leak. '
                    'Distinguishing lack of malicious intent from deliberate theft guides proportional incident containment.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A malicious APT cyber espionage attack from a foreign government.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The incident was a human auto-complete addressing error, not an APT malware intrusion.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A ransomware encryption attack on the Exchange server.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. No files or servers have been encrypted; this is an email data misdirection incident.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Administrative Mailbox Recall & Compliance Purge',
        'situation_text': (
            'The standard Outlook client "Recall Message" feature is unreliable and only works if recipients have not opened the email.\n\n'
            'What administrative method must you execute to purge the sensitive email from all 320 internal mailboxes immediately?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Execute a Microsoft Purview / Exchange PowerShell compliance search and hard-delete purge (`New-ComplianceSearchAction -Purge -PurgeType HardDelete`) targeting the Message-ID across all internal mailboxes.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Administrative HardDelete via Compliance Search instantly strips the message from all internal inboxes, '
                    'Deleted Items, and mobile devices regardless of whether users have read it.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Email all 320 staff members asking them to please click "Delete" and not look at the attachment.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Asking users not to look at an email creates the "Streisand Effect," prompting curious employees to open it immediately.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the entire Exchange server virtual machine.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Destroying the mail infrastructure destroys all business communications and is completely disproportionate.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'External Recipient Containment & Non-Disclosure',
        'situation_text': (
            'The email has been successfully hard-purged from all 320 internal employee mailboxes. '
            'However, 45 messages were delivered to external commercial partner mail servers outside your administrative control.\n\n'
            'How should General Counsel and the Security team handle the 45 external recipients?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Issue formal legal recall and data destruction notices to all 45 external recipient organizations requesting written confirmation of deletion, and log evidence for the Data Protection Officer.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. For external misdirected emails, formal legal destruction notices paired with written compliance confirmations '
                    'mitigates regulatory risk and establishes statutory due diligence under privacy regulations.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Hack into the external partner email servers to delete the emails secretly.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Hacking external systems is illegal criminal conduct under the Computer Misuse Act.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ignore the external recipients and pretend it never happened.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Ignoring external data leaks violates GDPR/privacy reporting mandates.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Technical DLP Guardrails',
        'situation_text': (
            'All internal copies were purged within 12 minutes of the initial send, all 45 external partners provided '
            'written certificates of deletion, and the ICO evaluated the incident as low risk due to immediate containment.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT PROFILE: Accidental Data Leakage via Auto-Complete Distribution List Misdirection.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Fast employee self-reporting culture\n'
            '- Detection & Analysis: Intent evaluation, Exchange message tracking\n'
            '- Containment: PowerShell Compliance Search HardDelete execution\n'
            '- Eradication: External legal destruction notices and deletion certificates\n'
            '- Post-Incident Activity: Mail flow rule and DLP policy implementation\n\n'
            'PREVENTATIVE CONTROLS IMPLEMENTED:\n'
            '1. Configured Microsoft Purview DLP policy to block external transmission of spreadsheets containing financial PII / SSNs.\n'
            '2. Restricted broad distribution lists (e.g. `All_Partners`) to require moderator approval before messages are released.\n'
            '3. Configured Outlook MailTips to display a prominent warning banner when sending emails to external distribution groups.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-INS-05: Nation-State Recruitment of Employee (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_INS_05_OBJECTIVES = [
    (1, 'Recognize behavioral and technical indicators of foreign intelligence recruitment.'),
    (2, 'Conduct sensitive insider investigation while coordinating with national security agencies.'),
    (3, 'Silently isolate classified data repositories while monitoring adversary collection requirements.'),
    (4, 'Implement compartmentalized access controls and insider threat detection policies.'),
]

S_INS_05_STEPS = [
    {
        'step_number': 1,
        'title': 'The Anomaly in Hypersonic Propulsion',
        'situation_text': (
            'At GlobalAerospace Corp, the Counterintelligence & Insider Threat Unit receives a prioritized lead. '
            'Dr. Elena Rostova, Lead Propulsion Scientist on classified hypersonic defense projects, attended an international '
            'aviation symposium in Singapore 6 weeks ago.\n\n'
            'Since returning, internal UEBA monitoring flags significant behavioral changes:\n'
            '- 450+ classified design files queried outside her authorized sub-project scope.\n'
            '- Multiple late-night logins at 02:00 AM downloading complete CAD schematics for thermal heat-shield materials.\n'
            '- Financial intelligence reports indicate sudden, unexplained offshore cryptocurrency deposits to her wallet.\n\n'
            'You are the Counterintelligence Liaison leading the internal response.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Technical Behavioral Baseline Analysis',
        'situation_text': (
            'You analyze Dr. Rostova’s workstation access logs, network activity, and file staging areas. You observe:\n\n'
            '- Files are being copied into an obscure local directory: `C:\\ProgramData\\Diagnostics\\Temp\\`\n'
            '- Files are being converted into password-protected encrypted archives using VeraCrypt.\n'
            '- Outbound encrypted DNS queries (DoH) directed to a known command infrastructure associated with APT29 / Foreign Intelligence.\n\n'
            'What does this combination of behavioral and technical indicators confirm?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'An active, nation-state sponsored espionage operation involving an recruited insider collecting and staging classified defense intellectual property.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. The staging of unauthorized classified schematics, local VeraCrypt encryption, DoH beaconing to state-sponsored C2, '
                    'and offshore deposits represent a textbook human intelligence (HUMINT) espionage recruitment operation.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'An employee doing standard literature review for an upcoming academic paper.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Literature review does not involve VeraCrypt encrypted staging of restricted defense files and DoH beaconing to APT infrastructure.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A routine IT backup failure.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Forensic artifacts show deliberate human file gathering, encryption, and covert C2 communication.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'National Security Agency Coordination',
        'situation_text': (
            'Because this incident involves state-sponsored espionage targeting classified hypersonic defense technology, '
            'standard internal corporate termination procedures could compromise ongoing national counterintelligence operations.\n\n'
            'What is the mandatory protocol for handling foreign intelligence insider operations?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Immediately brief national intelligence and security services (e.g. MI5 / FBI Counterintelligence) and establish a joint operational control plan before taking any visible internal action.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. In nation-state espionage cases, premature internal action can burn active counterintelligence surveillance, '
                    'allow foreign handlers to escape, or trigger emergency data exfiltration. Joint coordination with national agencies is mandatory.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Immediately fire the employee over email and threaten to call the local newspaper.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Firing the employee prematurely alerts the foreign intelligence handler and destroys the espionage investigation.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the employee’s entire hard drive remotely without saving any evidence.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting the hard drive destroys critical espionage evidence needed for federal prosecution and treason charges.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Deploying Canary Deception & Honeytokens',
        'situation_text': (
            'In coordination with federal counterintelligence agents, you need to track what data the adversary handlers '
            'are requesting without allowing genuine classified defense schematics to leave the network.\n\n'
            'What technical deception technique should you deploy?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy watermarked decoy files (Honeytokens / Canary Documents) containing realistic but flawed engineering data with embedded tracking beacons, while silently restricting access to genuine production repositories.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Deception technology (canary honeytokens) provides definitive forensic tracking when the files are opened by adversary handlers, '
                    'while protecting genuine defense IP from exfiltration.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Replace all company engineering files with blank Word documents.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Blank documents immediately tip off the insider and halt legitimate defense operations.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Disable the company internet connection for all 50,000 employees.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Shutting down global company internet is completely disproportionate and alerts the espionage network.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Synchronized Apprehension & Physical Evidence Seizure',
        'situation_text': (
            'The canary documents are accessed by Dr. Rostova and transferred to an encrypted USB drive. '
            'Federal agents and company security execute a synchronized intervention at the facility exit barrier.\n\n'
            'What technical forensics must be conducted on her corporate and seized personal devices immediately?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Conduct certified ISO 27037 forensic imaging of all seized devices with cryptographic hash verification, extract RAM encryption keys, and document complete artifact chain of custody for federal court prosecution.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Strict forensic imaging under ISO 27037 with verifiable chain of custody is essential '
                    'for the evidence to withstand rigorous scrutiny in federal national security espionage trials.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Browse through the seized laptop files using Windows File Explorer to see what is on it.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Live browsing without write-blockers modifies access timestamps and compromises legal evidence integrity.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Give the laptop to an intern to reformat.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Reformatting destroys national security evidence.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Network Compartmentalization & Threat Hunting',
        'situation_text': (
            'The subject is in federal custody. You must ensure no other company employees were compromised '
            'or recruited as part of this intelligence cell.\n\n'
            'What enterprise threat hunting and identity audits should you execute?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Execute enterprise-wide threat hunting for C2 communication indicators, cross-reference employee foreign travel registries with anomalous classified access patterns, and enforce strict Compartmented Information (SCI) access boundaries.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Cross-correlating foreign travel logs with UEBA file access anomalies identifies other potential recruitment targets, '
                    'and micro-segmentation restricts classified compartments strictly to validated clearance holders.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Assume all other 50,000 employees are 100% innocent and do no further auditing.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Foreign intelligence services frequently target multiple personnel within the same high-value program.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Shut down all hypersonic defense research permanently.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Defense contracts must continue under strengthened, validated security controls.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & National Security Closure',
        'situation_text': (
            'The counterintelligence operation was completed with 100% success. Zero genuine classified defense schematics '
            'were exfiltrated to the adversary, the insider was indicted under the Espionage Act, and the intelligence cell was neutralized.\n\n'
            'LESSONS LEARNED:\n\n'
            'INCIDENT PROFILE: Nation-State Recruitment & Coordinated Insider Espionage targeting classified defense intellectual property.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: UEBA behavioral analytics and travel anomaly correlation\n'
            '- Detection & Analysis: Staged encrypted file analysis, DoH C2 beaconing detection\n'
            '- Containment: Inter-agency counterintelligence coordination, canary token deception deployment\n'
            '- Eradication: Synchronized arrest, certified ISO 27037 forensic acquisition\n'
            '- Recovery: Enterprise threat hunting, Sensitive Compartmented Information (SCI) lockdown\n'
            '- Post-Incident Activity: Security clearance governance upgrade\n\n'
            'NATIONAL SECURITY ENHANCEMENTS:\n'
            '1. Enforced mandatory reporting and continuous monitoring of foreign official interactions and foreign financial accounts for all clearance holders.\n'
            '2. Implemented Zero Trust Continuous Authentication with cryptographic hardware tokens on all classified R&D jump hosts.\n'
            '3. Deployed automated DLP canary traps across all classified engineering directories.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]

INSIDER_THREAT_SCENARIOS = {
    'S-INS-01': (S_INS_01_OBJECTIVES, S_INS_01_STEPS),
    'S-INS-02': (S_INS_02_OBJECTIVES, S_INS_02_STEPS),
    'S-INS-03': (S_INS_03_OBJECTIVES, S_INS_03_STEPS),
    'S-INS-04': (S_INS_04_OBJECTIVES, S_INS_04_STEPS),
    'S-INS-05': (S_INS_05_OBJECTIVES, S_INS_05_STEPS),
}
