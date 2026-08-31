"""
Guardelio — Phishing & Social Engineering Scenarios (S-PHI-01 to S-PHI-05)
NIST SP 800-61 Aligned Incident Response Simulations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# S-PHI-01: CEO Fraud Email at City Council (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_PHI_01_OBJECTIVES = [
    (1, 'Analyze email headers, domain names, and reply-to addresses to detect spoofing and BEC attempts.'),
    (2, 'Execute rapid communication containment to prevent financial loss from fraudulent payment requests.'),
    (3, 'Formulate end-user reporting guidelines and email filtering rules to prevent recurring CEO fraud.'),
]

S_PHI_01_STEPS = [
    {
        'step_number': 1,
        'title': 'Urgent Payment Request',
        'situation_text': (
            'At 09:15 AM, an accounts payable clerk at City Metropolitan Council contacts the IT Helpdesk. '
            'She received an email marked "URGENT & CONFIDENTIAL" purportedly from the Council Chief Executive, '
            'demanding an immediate £45,000 wire transfer to an emergency municipal infrastructure supplier.\n\n'
            'The email emphasizes that the Chief Executive is in all-day cabinet meetings and cannot take calls. '
            'The clerk is nervous because the payment deadline is 11:00 AM, but the supplier bank details '
            'differ from the approved vendor database.\n\n'
            'You are the first-response IT Support Analyst. Your goal is to triage the message and take appropriate action.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Email Header & Domain Analysis',
        'situation_text': (
            'You inspect the raw email headers forwarded by the clerk. You observe:\n\n'
            '- Display Name: "Arthur Pendelton <Chief Executive>"\n'
            '- From Address: "arthur.pendelton@citycounci1.gov.uk"\n'
            '- Reply-To: "executive-office-priority@mail-secure-portal.com"\n'
            '- Authentication-Results: spf=softfail, dkim=none, dmarc=fail\n\n'
            'What is the most critical indicator of compromise in these headers?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'The sender domain uses typosquatting ("citycounci1.gov.uk" with a numeral 1) and the Reply-To routes to an external domain.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Typosquatting (substituting "l" with "1") combined with an external Reply-To '
                    'address and failed SPF/DMARC checks conclusively proves this is a spoofed CEO fraud attack. '
                    'This aligns with NIST SP 800-61 Detection & Analysis practices.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The email was sent before 09:30 AM, which is earlier than typical council working hours.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Email timestamp alone is circumstantial and not a technical indicator of spoofing. '
                    'The cryptographic authentication failures and domain typosquatting are the definitive evidence.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The display name includes angle brackets around the title, which is not permitted in SMTP.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Display name formatting is not restricted in this manner by SMTP standards. '
                    'The actionable threat indicators are the typosquatted domain and mismatched Reply-To header.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Immediate Payment Halt & Verification',
        'situation_text': (
            'The spoofing attempt is confirmed. However, the clerk mentions that she already drafted the wire transfer '
            'in the council’s banking portal and only needs the Finance Director’s second authorization.\n\n'
            'What is your immediate action to prevent financial loss?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Instruct the clerk immediately in writing and in person to cancel the draft wire, and notify the Finance Director to reject any pending transfer.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Immediate operational intervention is essential to stop the financial transaction. '
                    'Direct communication with both the clerk and the second-approver eliminates the risk of accidental execution.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Reply to the external Reply-To address threatening the attacker with police action.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Engaging with the attacker alerts them to detection, confirms the validity of the clerk’s email, '
                    'and does nothing to halt the internal wire approval process.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Wait for the Chief Executive to exit his meeting at 17:00 to verify if he sent the request.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Delaying action violates incident response containment timelines and risks unauthorized payment '
                    'approval before the 11:00 AM deadline.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Tenant-Wide Scope Assessment & Blocking',
        'situation_text': (
            'The fraudulent wire draft has been canceled. No funds were transferred.\n\n'
            'Now you must ensure no other council employees received the same or similar fraudulent emails from this threat actor.\n\n'
            'What is your next technical containment step?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Block the sender domain "citycounci1.gov.uk" on the email gateway and run a tenant-wide message trace to purge matching emails from all user mailboxes.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Blocking the malicious domain and executing an Exchange/M365 compliance purge '
                    '(HardDelete) neutralizes the campaign across the entire organization, preventing other staff from falling victim.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Forward the fraudulent email to all council staff asking them if they also received it.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Forwarding active phishing emails increases organizational risk and can cause panic or accidental interaction. '
                    'Always use automated administrative search and purge tools.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Reset the password of the legitimate Chief Executive immediately.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The Chief Executive’s actual account was not compromised; the attacker used an external spoofed domain. '
                    'Resetting his password causes unnecessary disruption without addressing the inbound email threat.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Policy Hardening',
        'situation_text': (
            'The CEO fraud attempt was successfully intercepted with zero financial loss. '
            'A total of 4 additional finance staff members had received the spoofed email; all copies were purged automatically.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK SUMMARY: Business Email Compromise (BEC) via typosquatted external domain attempting emergency wire diversion.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Triage of urgent payment alert and evidence collection\n'
            '- Detection & Analysis: Header inspection, DMARC/SPF failure analysis, domain typosquatting identification\n'
            '- Containment: Immediate wire cancellation and tenant-wide message purge\n'
            '- Post-Incident Activity: Review of financial dual-control controls\n\n'
            'PREVENTATIVE ACTIONS IMPLEMENTED:\n'
            '1. Enforced strict DMARC "p=reject" policy on all inbound mail filters.\n'
            '2. Configured external sender warning banners for emails displaying executive names.\n'
            '3. Mandated out-of-band phone verification for all wire transfers exceeding £5,000.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-PHI-02: Spear-Phishing Campaign Targeting HR (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_PHI_02_OBJECTIVES = [
    (1, 'Triage suspicious PDF attachments containing embedded malicious hyperlinks and credential-harvesting macros.'),
    (2, 'Identify compromised user credentials and enforce immediate session token invalidation and MFA resets.'),
    (3, 'Audit and eradicate unauthorized OAuth app permissions, mail forwarding rules, and persistent access grants.'),
]

S_PHI_02_STEPS = [
    {
        'step_number': 1,
        'title': 'Suspicious Resume Attachment',
        'situation_text': (
            'At 14:20, an HR recruiter at Atlas Insurance Group opens a ticket with the SOC. '
            'She received an unsolicited job application email with an attachment titled "Executive_CV_Morgan.pdf".\n\n'
            'Upon opening the PDF, a prompt claimed the document was protected by Microsoft Purview and instructed '
            'her to click a button to "Verify Corporate Credentials via Microsoft 365". She clicked the button and entered '
            'her username, password, and SMS MFA code on a page that looked identical to the company login portal.\n\n'
            'She realized something was wrong when the browser redirected to an error page. You are the SOC Tier 2 Analyst assigned.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Attachment Sandbox & Threat Analysis',
        'situation_text': (
            'You analyze the PDF in an isolated sandbox environment. The PDF contains an embedded URI action pointing to:\n\n'
            'https://login.microsoftonline.atlasinsurance-auth.workers.dev/login\n\n'
            'Sandbox network telemetry shows an adversary-in-the-middle (AiTM) proxy intercepting authentication tokens '
            'and relaying them to a command server in real time.\n\n'
            'What does this AiTM proxy capability imply regarding the user’s MFA?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'The AiTM proxy captured the valid session cookie alongside credentials, allowing the attacker to bypass standard SMS/TOTP MFA completely.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. AiTM phishing proxies (e.g., Evilginx) proxy real login requests between the victim and legitimate IdP, '
                    'stealing session cookies (ESTSAUTH) and bypassing non-FIDO2 MFA. Fast session revocation is critical.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'MFA protected the account, so the attacker only received the plaintext password without access.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. AiTM proxies capture the session cookie generated AFTER the user completes the MFA challenge. '
                    'The account is actively compromised despite SMS MFA.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The PDF exploited a zero-day vulnerability in Adobe Reader to execute remote shellcode.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Sandbox telemetry confirms this was an AiTM credential harvesting phishing link, '
                    'not a client-side memory corruption zero-day exploit.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Identity Provider Audit & Scope Confirmation',
        'situation_text': (
            'You inspect Microsoft Entra ID (Azure AD) sign-in logs for the recruiter’s account (c.davis@atlasinsurance.com). '
            'You find:\n\n'
            '- 14:23: Successful interactive login from London (legitimate user IP)\n'
            '- 14:24: Successful session access using stolen cookie from an IP located in Frankfurt, Germany (ASN 16276 / VPN host)\n'
            '- 14:26: Access to SharePoint HR directory and Exchange Online Mailbox\n\n'
            'What is the immediate priority containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Revoke all active refresh tokens (Revoke-AzureADUserAllRefreshToken), reset the user password, and temporarily disable the account.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Revoking active session and refresh tokens immediately invalidates the stolen AiTM session cookie, '
                    'terminating the attacker’s active web sessions across all cloud apps.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send an email to c.davis asking her to log out of all devices when she has a moment.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. With an active unauthorized session downloading sensitive HR files, immediate administrative session revocation is mandatory.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Block the IP address in Frankfurt on the corporate perimeter firewall.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The attacker is accessing cloud services (M365) directly, which does not pass through your on-premises firewall. '
                    'Token revocation in the Identity Provider is the correct containment action.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Investigating Persistence Mechanisms',
        'situation_text': (
            'Tokens have been revoked and the account password has been reset. You now audit the mailbox and cloud tenant '
            'for any persistence mechanisms created during the attacker’s 12-minute window of access.\n\n'
            'Exchange audit logs reveal:\n'
            '- Mailbox Rule Added: "Move all messages containing keywords [invoice, password, wire, confidential] to RSS Feeds folder and forward to drop@shadowexfil.net"\n'
            '- OAuth App Registered: "M365 Data Sync Tool" with permissions `Mail.ReadWrite` and `Files.ReadWrite.All`\n\n'
            'What eradication action is required?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Delete the malicious inbox rule, remove the unauthorized OAuth app registration, and revoke all enterprise application consent grants.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Attackers frequently deploy hidden inbox forwarding rules and malicious OAuth applications '
                    'to maintain persistent API-level access even after password changes. Both must be thoroughly eradicated.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Delete the entire mailbox of the HR recruiter and create a fresh mailbox from scratch.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting the entire mailbox destroys business records and forensic evidence. '
                    'Targeted removal of the forwarding rule and OAuth consent is the standard, proportional eradication procedure.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Leave the OAuth application in place to monitor what data the attacker tries to request.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Leaving malicious OAuth apps active in a production healthcare/insurance environment risks continued '
                    'data exfiltration and violates regulatory compliance obligations.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Tenant Hardening & Phishing-Resistant MFA',
        'situation_text': (
            'All persistence artifacts have been eradicated. You must now implement controls to prevent future '
            'AiTM spear-phishing attacks from bypassing MFA across the organization.\n\n'
            'Which technical control effectively neutralizes Adversary-in-the-Middle (AiTM) proxy phishing?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enforce FIDO2 / WebAuthn hardware security keys or certificate-based authentication (CBA), which cryptographically bind the authentication session to the legitimate domain origin.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. FIDO2 / WebAuthn is phishing-resistant because the browser cryptographically verifies the website domain origin, '
                    'refusing to send authentication assertions to proxy domains like "atlasinsurance-auth.workers.dev".'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Increase the complexity requirement of user passwords to 24 characters with special symbols.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Password complexity has zero effect on AiTM phishing, as the user willingly enters the password into the proxy.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Switch from SMS verification to email-based OTP verification codes.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Email OTPs are just as vulnerable to AiTM interception and relay as SMS OTPs. Only FIDO2/WebAuthn provides origin binding.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Incident Closure & Executive Debrief',
        'situation_text': (
            'The spear-phishing incident is resolved. The compromised session was terminated within 15 minutes of detection, '
            'all malicious inbox rules and OAuth persistence vectors were removed, and no mass data exfiltration occurred.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK VECTOR: Weaponized PDF with AiTM credential and session token harvesting proxy.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Triage of recruiter alert and sandbox detonation of weaponized PDF\n'
            '- Detection & Analysis: AiTM proxy identification, Azure AD session token correlation\n'
            '- Containment: Universal token revocation and account isolation\n'
            '- Eradication: Malicious inbox rule removal and OAuth application deregistration\n'
            '- Post-Incident Activity: Implementation of FIDO2 phishing-resistant authentication\n\n'
            'STRATEGIC RECOMMENDATIONS:\n'
            '1. Mandated FIDO2 security keys for all high-risk roles (HR, Finance, IT Administrators).\n'
            '2. Blocked external user consent for third-party multi-tenant applications.\n'
            '3. Configured Defender for Cloud Apps anomaly detection alerts for Impossible Travel and anomalous OAuth apps.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-PHI-03: Vishing Attack on Service Desk (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_PHI_03_OBJECTIVES = [
    (1, 'Identify social engineering and voice phishing (vishing) manipulation tactics targeting help desk personnel.'),
    (2, 'Execute out-of-band identity verification before performing privileged account modifications.'),
    (3, 'Coordinate incident containment for unauthorized VPN credential resets.'),
]

S_PHI_03_STEPS = [
    {
        'step_number': 1,
        'title': 'The Urgent Field Call',
        'situation_text': (
            'At 02:30 AM, a junior service desk analyst at Northern Rail Operations receives an urgent phone call. '
            'The caller claims to be "David Miller, Senior Signalling Engineer on emergency trackside duty near Leeds."\n\n'
            'The caller states that severe weather caused signalling power failure and he needs immediate VPN access from '
            'a local emergency laptop to restore railway signals. He claims his phone battery is dead, his MFA device was left '
            'in his vehicle, and he demands the analyst immediately reset his password and register a temporary phone number for MFA.\n\n'
            'You are the Service Desk Lead supervising night operations.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Recognizing Social Engineering Indicators',
        'situation_text': (
            'The junior analyst asks for your guidance before proceeding. You listen to the caller’s background audio '
            'and examine his request details.\n\n'
            'What combination of psychological manipulation tactics is the caller using?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Artificial urgency, appeal to critical safety authority, fear of operational consequences, and bypassing standard identity verification.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Attackers exploit high-stress scenarios (signalling emergency, dead battery) to pressure service desk staff '
                    'into violating identity verification protocols out of fear or urgency.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Technical jargon overload and SQL injection terminology.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The caller is using emotional and situational social engineering tactics (vishing), not technical jargon overload.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Bribery and financial incentives offered to the helpdesk agent.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The caller is using urgency and safety authority, not financial bribery.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Out-of-Band Verification Protocol',
        'situation_text': (
            'The caller insists: "Trains are stopping at red signals right now! If you don\'t reset my password in 60 seconds, '
            'I will report you to the Operations Director for endangering passenger safety!"\n\n'
            'What is the mandatory verification procedure according to NIST and IT security best practice?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Refuse to modify credentials on the incoming call; perform an out-of-band callback to David Miller’s pre-registered HR mobile and contact the Leeds Rail Control Room.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Out-of-band verification via official, pre-registered communication channels is the only reliable defense '
                    'against voice phishing (vishing). Never accept incoming caller credentials under pressure.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ask the caller for his employee badge number and mother’s maiden name, then complete the reset.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Static knowledge-based authentication data (badge numbers, personal details) is easily harvested by attackers '
                    'through open-source intelligence (OSINT) or data breaches.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Perform the password reset immediately to avoid train delays, but flag the ticket for review in the morning.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Yielding to pressure gives an unauthorized attacker privileged access into critical railway control infrastructure.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Incident Confirmation & Account Locking',
        'situation_text': (
            'You place the caller on hold and call the Leeds Rail Control Room. The duty manager confirms:\n'
            '- There are NO power or signalling failures in Leeds.\n'
            '- David Miller is currently on approved annual leave in Spain and is not on duty.\n\n'
            'The attacker hangs up when you return to the line.\n\n'
            'What containment action should you take immediately regarding David Miller’s real account?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Place a temporary security lock on David Miller’s account, review recent authentication logs for prior compromise attempts, and alert the SOC.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Locking the targeted account and auditing recent authentication history ensures the attacker does not attempt '
                    'alternative entry vectors or self-service password resets.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ignore the incident since the reset was not completed and no breach occurred.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A targeted vishing attack indicates an active reconnaissance and access attempt by a threat actor. '
                    'Logging, containment, and SOC escalation are required.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Email all 10,000 employees notifying them of the call.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Mass uncoordinated email blasts cause alarm and create noise. Escalate to the SOC and follow established security communication channels.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Service Desk Hardening',
        'situation_text': (
            'The vishing attack was successfully thwarted by adhering to strict out-of-band verification procedures. '
            'David Miller’s account was secured and the SOC added the calling number to carrier fraud registries.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK SUMMARY: Voice phishing (vishing) impersonating a senior engineer claiming operational emergencies.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Supervisory oversight of night-shift service desk requests\n'
            '- Detection & Analysis: Social engineering psychological manipulation indicators identified\n'
            '- Containment: Out-of-band verification executed, fraudulent request denied, target account secured\n'
            '- Post-Incident Activity: Verification standard operating procedure review\n\n'
            'PROCEDURAL ENHANCEMENTS:\n'
            '1. Eliminated all verbal and SMS password resets for privileged and OT engineering accounts.\n'
            '2. Implemented mandatory manager video-call verification or in-person hardware token distribution.\n'
            '3. Added vishing simulation modules to regular service desk security awareness training.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-PHI-04: Business Email Compromise at Law Firm (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_PHI_04_OBJECTIVES = [
    (1, 'Reconstruct attacker timeline from email audit logs, mail forwarding rules, and IP geolocations.'),
    (2, 'Coordinate immediate financial kill-chain intervention with banks and legal authorities.'),
    (3, 'Identify and eliminate attacker persistence mechanisms across M365 and hybrid Exchange environments.'),
    (4, 'Implement cryptographic invoice verification controls and strict dual-authorization wire policies.'),
]

S_PHI_04_STEPS = [
    {
        'step_number': 1,
        'title': 'The Intercepted Wire Transfer',
        'situation_text': (
            'At 08:30 on Tuesday, the Managing Partner at Crowe & Partners Law Firm bursts into the IT department. '
            'A corporate real estate client just called asking why their £2.4M commercial property purchase deposit '
            'has not cleared. The client states they wired the money yesterday afternoon following updated payment instructions '
            'received directly from the lead partner’s email address.\n\n'
            'The partner confirms he never sent updated bank details. The legitimate firm bank account is with Barclays in London; '
            'the client was directed to a commercial account in Dubai.\n\n'
            'You are the Digital Forensics Lead called to handle the crisis.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Emergency Financial Intervention & Law Enforcement',
        'situation_text': (
            'The fraudulent wire transfer was initiated 16 hours ago via the international banking network (SWIFT). '
            'Every minute is critical before the funds are dispersed into crypto or cash mules.\n\n'
            'What is the highest-priority initial containment step?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Instruct the client’s sending bank to issue an immediate SWIFT MT199 Recall / Urgent Fraud Stop, and notify the National Cyber Crime Unit (NCCU) and Action Fraud.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. In BEC wire fraud, engaging the originating bank’s fraud desk for a SWIFT Recall '
                    'within the 24–48 hour window is the only viable path to freezing and recovering funds before offshore laundering.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Post a warning message on the law firm’s public website advising all clients of a security incident.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Public statements do nothing to freeze the live financial wire and can cause legal liability before facts are established.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Send an angry email to the Dubai bank account holder demanding immediate refund of the money.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Fraudulent accounts are operated by organized money-mule rings; emailing the mule account is ineffective and alerts criminals to accelerate withdrawals.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Mailbox Forensics & Tampering Identification',
        'situation_text': (
            'While the bank fraud team works the recall, you examine the lead partner’s mailbox (r.crowe@crowepartners.com). '
            'The partner has no sent messages relating to bank changes in his Sent Items folder.\n\n'
            'You execute a PowerShell audit using `Get-InboxRule` and `Search-UnifiedAuditLog`. You discover:\n'
            '- Hidden Inbox Rule: `Name: "..."` -> Matches subjects with "deposit", "wire", "invoice", "bank" -> Moves to Deleted Items -> Marks Read\n'
            '- Attacker replied to the client using a spoofed conversation thread from within the partner’s actual mailbox!\n\n'
            'How did the attacker prevent the partner from noticing the fraudulent client emails?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'The hidden inbox rule automatically intercepted and hid client replies in Deleted Items while the attacker replied directly via Exchange Web Services (EWS).',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. This is the hallmark of sophisticated Business Email Compromise (BEC). Attackers silently divert '
                    'and delete legitimate client replies so the true account owner remains completely unaware of the ongoing manipulation.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The attacker uninstalled Outlook from the partner’s laptop remotely.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The partner was actively using Outlook without disruption; the concealment was achieved through stealth inbox filtering rules.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The client was imagining the emails because no Sent Items existed.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Sent items were automatically purged by the attacker’s inbox rule; audit logs confirm the messages were dispatched from the tenant.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Root Cause Analysis & Initial Vector Discovery',
        'situation_text': (
            'You trace the unified audit logs back 30 days to locate the initial compromise timestamp. You discover:\n\n'
            '- 22 days ago: Successful authentication to `r.crowe` via legacy Basic Authentication (IMAP) from an IP in Lagos, Nigeria.\n'
            '- The password used matched a credential leak from a third-party legal research portal from 2024.\n'
            '- Legacy protocol IMAP bypassed modern Conditional Access and MFA policies because Basic Auth was not disabled tenant-wide.\n\n'
            'What is the root architectural vulnerability that enabled this breach?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Legacy basic authentication protocols (IMAP/POP3/SMTP) enabled credential stuffing and password spraying without MFA enforcement.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Legacy authentication protocols do not support modern Multi-Factor Authentication. '
                    'Adversaries exploit unblocked legacy protocols (e.g. IMAP) to authenticate with compromised credentials and bypass conditional access.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The firm had not installed physical token readers on the partner’s home desktop.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The attack was executed remotely over cloud IMAP protocols, independent of local physical tokens.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The client’s computer was infected with ransomware which modified the bank details on the wire transfer form.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Forensic logs confirm the lead partner’s M365 account was authenticated via IMAP and sent the fraudulent PDF from within the law firm’s tenant.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Eradication & Tenant-Wide Remediation',
        'situation_text': (
            'You must now systematically eradicate all attacker footholds across the firm’s entire cloud estate.\n\n'
            'What comprehensive eradication actions must be executed?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Purge all malicious mailbox rules and forwarding delegates, revoke all active user sessions, reset passwords, disable legacy authentication tenant-wide, and audit all other partner mailboxes.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Complete eradication requires removing hidden mailbox rules, resetting credentials, revoking active session tokens, '
                    'disabling legacy protocols globally, and checking for lateral spread across all high-value accounts.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ask all employees to manually check their own Deleted Items folders for suspicious emails.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Manual end-user checks cannot detect hidden Exchange rules, OAuth grants, or legacy protocol compromise.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Format the hard drive of the lead partner’s laptop and reinstall Windows.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The compromise exists in the cloud tenant (Exchange Online), not on the local laptop hardware.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Secure Recovery & Cryptographic Invoice Controls',
        'situation_text': (
            'The banking recall successfully froze £2.1M of the £2.4M transfer in the destination bank before withdrawal; '
            'recovery of the remaining £300K is being pursued by law enforcement.\n\n'
            'What technical and organizational control will permanently prevent wire redirection in future client engagements?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Mandate out-of-band dual-authorization phone verification for bank changes, and deliver all invoice payment details via a cryptographically signed client portal rather than raw email PDFs.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Combining strict verbal out-of-band verification policies with secure client portal delivery removes email '
                    'as a single point of failure for high-value financial transactions.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Instruct clients to only pay in cash or paper cheques delivered by courier.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Paper cheques and physical cash are operationally infeasible for multi-million pound corporate real estate settlements.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Add a disclaimer line to the bottom of all email signatures stating "We will never change our bank details."',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Email signature disclaimers are routinely altered or ignored by attackers and clients alike; '
                    'they offer zero cryptographic or technical protection.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Forensic Case Closure',
        'situation_text': (
            'The BEC incident investigation is complete. £2.1M was successfully recovered and legal proceedings '
            'are ongoing for the remainder. The firm’s tenant is fully secured and validated.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK CHAIN: 3rd party credential leak -> Legacy IMAP protocol compromise -> Hidden inbox rule creation -> Invoice tampering -> Wire diversion.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Fast incident triage and multi-stakeholder mobilization\n'
            '- Containment: SWIFT wire recall, token revocation, account isolation\n'
            '- Detection & Analysis: Forensic audit of Exchange UnifiedAuditLog, identification of stealth inbox rules\n'
            '- Eradication: Rule purging, legacy authentication disabled globally\n'
            '- Recovery: Secure client communication re-established, client portal implemented\n'
            '- Post-Incident Activity: SRA regulatory notification and compliance hardening\n\n'
            'REGULATORY & TECHNICAL OUTCOMES:\n'
            '1. Soliciters Regulation Authority (SRA) and ICO notified within statutory timelines.\n'
            '2. Disabled Basic Authentication across all M365 services.\n'
            '3. Enforced Conditional Access requiring compliant, Intune-managed devices for cloud access.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-PHI-05: Pretexting Attack on Data Centre Staff (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_PHI_05_OBJECTIVES = [
    (1, 'Detect in-person social engineering, pretexting, and badge bypass attempts at critical infrastructure.'),
    (2, 'Verify third-party contractor credentials through verified vendor dispatch registries.'),
    (3, 'Execute physical and logical containment protocols when unauthorized facility access is attempted.'),
]

S_PHI_05_STEPS = [
    {
        'step_number': 1,
        'title': 'The Urgent Maintenance Contractor',
        'situation_text': (
            'At 11:15 AM on a Friday, an individual wearing a high-visibility vest, hard hat, and a lanyard labeled '
            '"Cisco Optical Infrastructure Maintenance" arrives at the security reception of DataVault Hosting.\n\n'
            'He presents a printed document titled "Emergency Core Switch Firmware Upgrade — Change Ticket #CHG-9941" '
            'and claims that failure to grant him unescorted access to Server Room C within 15 minutes will cause '
            'widespread fibre-optic backbone outages for the entire financial district.\n\n'
            'You are the Physical Security Coordinator on duty.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Document & Identity Verification',
        'situation_text': (
            'You inspect the visitor’s badge and work order document. You check your internal Change Management System (ITSM) '
            'for ticket `#CHG-9941` and observe:\n\n'
            '- Ticket `#CHG-9941` is an old, closed ticket from 8 months ago relating to HVAC maintenance, not core switches.\n'
            '- The contractor’s badge has no magnetic RFID chip and contains a low-resolution printed company logo.\n'
            '- The visitor is becoming visibly agitated, speaking loudly to intimidate the junior receptionist.\n\n'
            'What is your immediate assessment?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'This is a physical social engineering pretexting attack designed to gain unauthorized physical access to critical network hardware.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. The fabricated change ticket, fake badge, and aggressive intimidation tactics are classic indicators '
                    'of an in-person physical penetration testing or malicious red-team pretexting attack.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The ITSM database is having a sync delay, so the contractor should be allowed in with an escort.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A fabricated ticket number and fake badge are definitive indicators of social engineering. '
                    'Granting physical access based on assumptions breaches security policy.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The contractor is legitimate because he has high-visibility safety clothing and tools.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. High-visibility clothing and fake lanyards are easily purchased online and frequently used by social engineers as props.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Physical Containment & Access Denial',
        'situation_text': (
            'The pretexting attempt is confirmed. The visitor demands that you swipe your master badge to let him through '
            'the mantrap into the secure server corridor.\n\n'
            'What is your immediate containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Refuse facility entry, keep the visitor in the public reception area, discreetly alert on-site physical security officers, and request valid government photo ID.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Containing the visitor in the public air-gapped reception area while summoning on-site security '
                    'prevents physical breach of secure perimeters and allows proper documentation of the intruder.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Swipe him into the hallway but tell him not to touch anything while you call his manager.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Never grant physical access across security perimeters to unverified third parties. '
                    'Once inside, a skilled adversary can plant hardware implants (e.g., LAN Turtles, Keyloggers) in seconds.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Draw a weapon and confront the visitor aggressively in the lobby.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Escalate to trained physical security personnel and follow standard de-escalation containment protocols.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Vendor Dispatch Verification & Incident Escalation',
        'situation_text': (
            'Security officers arrive in reception. When asked for government identification, the individual attempts to leave. '
            'Security detains the individual at the exit barrier until police arrive.\n\n'
            'You call Cisco Systems’ official security dispatch number using the verified vendor contact list.\n\n'
            'What critical information must you confirm with the vendor?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Confirm whether Cisco dispatched any on-site engineers to DataVault Hosting today, and cross-reference the individual’s claimed name.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Vendor dispatch verification provides definitive corporate confirmation that no authorized maintenance was scheduled.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ask Cisco for their master administrative switch passwords over the phone.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Administrative credentials should never be requested or discussed during physical security dispatch triage.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ask Cisco to pay for the reception security guard’s overtime.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Irrelevant to incident response and threat attribution.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Physical Perimeter Forensic Audit',
        'situation_text': (
            'Police arrive and take the individual into custody. In his backpack, police discover a rogue Raspberry Pi hardware implant, '
            'Ethernet taps, and unauthorized lock-picking tools.\n\n'
            'You must now verify that no earlier physical compromise occurred.\n\n'
            'What eradication and audit steps should you immediately conduct?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Conduct a comprehensive CCTV review of all building entry points over the past 48 hours, inspect physical server racks for rogue hardware taps, and audit electronic badge access logs.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Physical forensics requires physical inspection of server cages, verifying tamper-evident seals on rack doors, '
                    'and auditing badge access records against video footage to guarantee no prior intrusion occurred.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Reboot all server operating systems remotely.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Server reboots do not detect physical network taps or verify perimeter security integrity.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Discard all visitor logs from the past week to clean the database.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Discarding visitor logs destroys vital forensic evidence needed for criminal prosecution.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & Physical Security Hardening',
        'situation_text': (
            'The physical intrusion attempt was successfully intercepted with zero penetration into secure server zones. '
            'All server racks, patch panels, and CCTV footage were audited with no anomalies found.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK TYPE: Physical pretexting and impersonation targeting high-security data centre infrastructure.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Reception staff training and change management verification\n'
            '- Detection & Analysis: Fake credential detection, ITSM verification, vendor dispatch validation\n'
            '- Containment: Public area containment, law enforcement intervention\n'
            '- Eradication: Physical rack audit and CCTV log reconciliation\n'
            '- Post-Incident Activity: Physical security policy enhancement\n\n'
            'POLICY UPGRADES IMPLEMENTED:\n'
            '1. Enforced mandatory biometric (fingerprint/iris) verification in addition to RFID badges for server room mantrap access.\n'
            '2. Mandated 24-hour advance vendor notice with photo ID pre-registration for all external contractors.\n'
            '3. Installed tamper-evident serialized seals on all external server rack doors.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]

PHISHING_SCENARIOS = {
    'S-PHI-01': (S_PHI_01_OBJECTIVES, S_PHI_01_STEPS),
    'S-PHI-02': (S_PHI_02_OBJECTIVES, S_PHI_02_STEPS),
    'S-PHI-03': (S_PHI_03_OBJECTIVES, S_PHI_03_STEPS),
    'S-PHI-04': (S_PHI_04_OBJECTIVES, S_PHI_04_STEPS),
    'S-PHI-05': (S_PHI_05_OBJECTIVES, S_PHI_05_STEPS),
}
