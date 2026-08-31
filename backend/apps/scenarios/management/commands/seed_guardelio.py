"""
Guardelio — Unified Seed Management Command
python manage.py seed_guardelio

Populates the database with:
  - 6 cybersecurity categories
  - 30 fully-playable cybersecurity scenarios (5 per category across 6 categories):
      * Malware Infection Response (S-MAL-01 to S-MAL-05)
      * Phishing & Social Engineering (S-PHI-01 to S-PHI-05)
      * DDoS & Network Disruption (S-DDS-01 to S-DDS-05)
      * Data Breach & Exfiltration (S-DAT-01 to S-DAT-05)
      * Insider Threat Detection (S-INS-01 to S-INS-05)
      * Network Intrusion & APT (S-APT-01 to S-APT-05)
  - 18 badges with criteria across all categories
  - 1 test student account (student@guardelio.com / Student@123)
  - 1 test admin account   (admin@guardelio.com  / Admin@123)

Safe to re-run: uses get_or_create and field updates throughout — never duplicates records.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User, StudentProfile
from apps.scenarios.models import Category, Scenario, LearningObjective, ScenarioStep, DecisionOption
from apps.progress.models import Badge

from apps.scenarios.seeds.malware_seeds import MALWARE_SCENARIOS
from apps.scenarios.seeds.phishing_seeds import PHISHING_SCENARIOS
from apps.scenarios.seeds.ddos_seeds import DDOS_SCENARIOS
from apps.scenarios.seeds.data_breach_seeds import DATA_BREACH_SCENARIOS
from apps.scenarios.seeds.insider_threat_seeds import INSIDER_THREAT_SCENARIOS
from apps.scenarios.seeds.network_apt_seeds import NETWORK_APT_SCENARIOS


# ─── Raw Category Data ────────────────────────────────────────────────────────

CATEGORIES = [
    {
        'name': 'Malware Infection Response',
        'slug': 'malware-infection-response',
        'short_summary': 'Detect, contain, and eradicate malware from compromised systems.',
        'description': (
            'Malware incidents are among the most common cybersecurity threats faced by organisations today. '
            'In this category, you will practise the NIST Incident Response framework as applied to ransomware, '
            'trojans, worms, and spyware outbreaks. Each scenario puts you in the role of an analyst responding '
            'to a live infection.'
        ),
        'icon_name': 'virus',
        'color_theme': 'red',
        'display_order': 1,
    },
    {
        'name': 'Phishing & Social Engineering',
        'slug': 'phishing-social-engineering',
        'short_summary': 'Identify, investigate, and mitigate phishing attacks and social engineering attempts.',
        'description': (
            'Phishing remains the top initial access vector in security breaches worldwide. '
            'Practise identifying malicious emails, investigating credential theft, '
            'responding to spear-phishing campaigns, and educating end-users — all within realistic simulations.'
        ),
        'icon_name': 'fish',
        'color_theme': 'amber',
        'display_order': 2,
    },
    {
        'name': 'DDoS & Network Disruption',
        'slug': 'ddos-network-disruption',
        'short_summary': 'Respond to volumetric attacks, scrub traffic, and restore service availability.',
        'description': (
            'Distributed Denial of Service attacks threaten service availability and can be combined '
            'with other attack vectors. In this category you will respond to volumetric, protocol, '
            'and application-layer attacks — making triage, traffic scrubbing, and ISP escalation decisions.'
        ),
        'icon_name': 'wifi-off',
        'color_theme': 'blue',
        'display_order': 3,
    },
    {
        'name': 'Data Breach & Exfiltration',
        'slug': 'data-breach-exfiltration',
        'short_summary': 'Investigate data theft, contain the breach, and manage stakeholder communication.',
        'description': (
            'Data breaches can expose sensitive customer records, intellectual property, and regulated data. '
            'These scenarios develop your skills in breach investigation, forensic log analysis, '
            'regulatory notification timelines (GDPR, HIPAA), and post-breach remediation.'
        ),
        'icon_name': 'database',
        'color_theme': 'purple',
        'display_order': 4,
    },
    {
        'name': 'Insider Threat Detection',
        'slug': 'insider-threat-detection',
        'short_summary': 'Detect malicious insiders, investigate anomalous access, and protect privileged data.',
        'description': (
            'Insider threats — whether malicious, negligent, or compromised — are among the hardest '
            'incidents to detect. These simulations train you to analyse audit logs, investigate suspicious '
            'behaviour, and navigate the legal and HR implications of insider threat investigations.'
        ),
        'icon_name': 'user-x',
        'color_theme': 'orange',
        'display_order': 5,
    },
    {
        'name': 'Network Intrusion & APT',
        'slug': 'network-intrusion-apt',
        'short_summary': 'Hunt advanced persistent threats, analyse lateral movement, and evict intruders.',
        'description': (
            'Advanced Persistent Threat actors are sophisticated, patient, and goal-oriented. '
            'These scenarios simulate APT campaigns where you must hunt for indicators of compromise, '
            'trace lateral movement, analyse command-and-control traffic, and execute eviction procedures.'
        ),
        'icon_name': 'shield-alert',
        'color_theme': 'emerald',
        'display_order': 6,
    },
]

SCENARIO_STUBS = [
    # (category_slug, scenario_id, title, difficulty, role, overview, est_min, xp_bonus, xp_perfect)
    # Malware (5)
    ('malware-infection-response', 'S-MAL-01', 'Ransomware Outbreak at Nexus Financial', 'beginner',
     'Junior Security Analyst at Nexus Financial Services',
     'A Monday morning alert: finance workstations encrypted by ransomware. Apply NIST IR to contain and recover.', 20, 30, 40),
    ('malware-infection-response', 'S-MAL-02', 'Trojan Horse in the Supply Chain', 'intermediate',
     'Threat Intelligence Analyst at GlobalTech Manufacturing',
     'A vendor software update delivered a trojan communicating with an external C2 server. Investigate and contain.', 25, 35, 45),
    ('malware-infection-response', 'S-MAL-03', 'Worm Spreading Through Hospital Network', 'advanced',
     'Senior Incident Responder at City General Hospital',
     'A self-propagating worm entered through an unpatched medical device, threatening clinical systems.', 30, 40, 50),
    ('malware-infection-response', 'S-MAL-04', 'Cryptominer on University Servers', 'beginner',
     'IT Security Intern at Westfield University',
     'Unusually high CPU usage reveals a cryptomining script deployed through a compromised admin account.', 15, 25, 35),
    ('malware-infection-response', 'S-MAL-05', 'Spyware in the Executive Suite', 'intermediate',
     'CISO Office Analyst at Meridian Consulting Group',
     'A targeted spyware infection on the CEO workstation may have exfiltrated board communications.', 25, 35, 45),

    # Phishing (5)
    ('phishing-social-engineering', 'S-PHI-01', 'CEO Fraud Email at City Council', 'beginner',
     'IT Support Analyst at City Metropolitan Council',
     'An accounts payable employee almost approved a fraudulent wire transfer from a spoofed CEO email.', 15, 25, 35),
    ('phishing-social-engineering', 'S-PHI-02', 'Spear-Phishing Campaign Targeting HR', 'intermediate',
     'Security Operations Analyst at Atlas Insurance Group',
     'A coordinated spear-phishing campaign uses weaponised PDFs to harvest HR staff credentials.', 25, 35, 45),
    ('phishing-social-engineering', 'S-PHI-03', 'Vishing Attack on Service Desk', 'beginner',
     'Service Desk Lead at Northern Rail Operations',
     'A caller posing as an IT technician convinced an agent to reset a senior engineer VPN account.', 15, 25, 35),
    ('phishing-social-engineering', 'S-PHI-04', 'Business Email Compromise at Law Firm', 'advanced',
     'Digital Forensics Analyst at Crowe & Partners Law Firm',
     'A silently compromised email account enabled attackers to intercept a £2.4M real estate wire transfer.', 35, 45, 55),
    ('phishing-social-engineering', 'S-PHI-05', 'Pretexting Attack on Data Centre Staff', 'intermediate',
     'Physical Security Coordinator at DataVault Hosting',
     'An attacker posing as a vendor engineer used a fabricated work order to gain physical data centre access.', 20, 30, 40),

    # DDoS (5)
    ('ddos-network-disruption', 'S-DDS-01', 'Volumetric DDoS on E-Commerce Platform', 'beginner',
     'NOC Analyst at ShopFront Retail Technologies',
     'Black Friday traffic spikes to 50Gbps. Distinguish DDoS traffic from legitimate load and respond.', 15, 25, 35),
    ('ddos-network-disruption', 'S-DDS-02', 'DNS Amplification Attack on ISP', 'intermediate',
     'Network Security Engineer at FastNet Internet Services',
     'Open DNS resolvers abused to amplify attack traffic against an enterprise customer.', 25, 35, 45),
    ('ddos-network-disruption', 'S-DDS-03', 'Application-Layer Attack on Banking Portal', 'advanced',
     'Incident Commander at NovaBanque Digital Services',
     'Low-and-slow HTTP requests exhaust connection pools without triggering volumetric thresholds.', 30, 40, 50),
    ('ddos-network-disruption', 'S-DDS-04', 'SYN Flood on Government Portal', 'beginner',
     'Junior Network Analyst at National Revenue Agency',
     'A SYN flood during tax filing deadline prevents citizens from submitting returns.', 15, 25, 35),
    ('ddos-network-disruption', 'S-DDS-05', 'Multi-Vector DDoS with Extortion', 'advanced',
     'Security Operations Lead at Apex Gaming Network',
     'Combined volumetric and application-layer DDoS with simultaneous Bitcoin extortion demand.', 35, 45, 55),

    # Data Breach (5)
    ('data-breach-exfiltration', 'S-DAT-01', 'Customer Database via Misconfigured S3 Bucket', 'beginner',
     'Cloud Security Analyst at TrendShop E-Commerce',
     'A researcher reports a publicly accessible S3 bucket containing 2 million customer records.', 20, 30, 40),
    ('data-breach-exfiltration', 'S-DAT-02', 'SQL Injection Breach on Healthcare Portal', 'intermediate',
     'Application Security Analyst at MedConnect Health Services',
     'SQL injection in the patient portal extracted medical records for 50,000 patients.', 25, 35, 45),
    ('data-breach-exfiltration', 'S-DAT-03', 'Insider Data Theft Before Resignation', 'advanced',
     'Digital Forensics Lead at Quantum Research Institute',
     'DLP alerts show mass data transfer to personal cloud storage by a researcher on gardening leave.', 30, 40, 50),
    ('data-breach-exfiltration', 'S-DAT-04', 'Third-Party Vendor Breach Affecting You', 'intermediate',
     'TPRM Analyst at Allied Financial Group',
     'Your payroll vendor suffered a breach; 12 months of employee data may be compromised.', 25, 35, 45),
    ('data-breach-exfiltration', 'S-DAT-05', 'GDPR Breach Notification Under 72 Hours', 'advanced',
     'Data Protection Officer at EuroPost Logistics',
     'A stolen laptop with unencrypted customer data requires GDPR Article 33 ICO notification within 72 hours.', 30, 40, 50),

    # Insider Threat (5)
    ('insider-threat-detection', 'S-INS-01', 'Disgruntled Employee Sabotaging Systems', 'beginner',
     'SOC Analyst at Omega Logistics',
     'A terminated employee with unrevoked badge access deleted files on the night of termination.', 15, 25, 35),
    ('insider-threat-detection', 'S-INS-02', 'Privileged Account Abuse by System Admin', 'intermediate',
     'Insider Threat Analyst at SecureBank UK',
     'A sysadmin querying customer account databases outside business hours has been flagged by anomaly detection.', 25, 35, 45),
    ('insider-threat-detection', 'S-INS-03', 'Contractor Selling Access to Dark Web', 'advanced',
     'Threat Hunter at Nexus Defence Technologies',
     'Threat intelligence shows VPN credentials for a defence contractor on sale on a dark web forum.', 30, 40, 50),
    ('insider-threat-detection', 'S-INS-04', 'Accidental Data Leak by Negligent Employee', 'beginner',
     'Information Security Advisor at Citywide Legal Services',
     'An employee emailed client billing records to the wrong distribution list including external recipients.', 15, 25, 35),
    ('insider-threat-detection', 'S-INS-05', 'Nation-State Recruitment of Employee', 'advanced',
     'Counterintelligence Liaison at GlobalAerospace Corp',
     'An employee who attended a foreign embassy event has since significantly changed data access patterns.', 35, 45, 55),

    # APT (5)
    ('network-intrusion-apt', 'S-APT-01', 'Lateral Movement Detected in Corporate Network', 'beginner',
     'Junior Threat Hunter at DataBridge Consulting',
     'An EDR alert fired on a workstation performing unusual network scans across 3 compromised machines.', 20, 30, 40),
    ('network-intrusion-apt', 'S-APT-02', 'C2 Beaconing to Suspicious Domain', 'intermediate',
     'SOC Tier 2 Analyst at Meridian Telecom',
     'DNS logs show regular beaconing to a DGA-like domain; a workstation is communicating with an attacker C2 server.', 25, 35, 45),
    ('network-intrusion-apt', 'S-APT-03', 'Nation-State APT Campaign Against Energy Sector', 'advanced',
     'Senior Threat Intelligence Analyst at NationalGrid Cyber Defence',
     'CISA advisory warns of APT activity in energy infrastructure; your SIEM flags matching indicators.', 40, 50, 60),
    ('network-intrusion-apt', 'S-APT-04', 'Credential Stuffing on VPN Gateway', 'beginner',
     'Identity Security Analyst at Apex Pharmaceuticals',
     'Thousands of failed VPN login attempts; several accounts accessed using credentials from a prior breach.', 15, 25, 35),
    ('network-intrusion-apt', 'S-APT-05', 'Living-off-the-Land Attack Using WMI and PowerShell', 'advanced',
     'EDR Specialist at FortiShield Managed Security',
     'Attacker uses WMI, PowerShell, and certutil to avoid detection — no malware binaries on disk.', 35, 45, 55),
]

BADGES = [
    # (name, description, badge_type, icon, criteria_type, criteria_value, cat_slug)
    # Bronze
    ('First Responder',        'Completed your first incident response simulation.',              'bronze', 'zap',          'completion_count', 1,    None),
    ('Malware Hunter',         'Successfully completed a malware incident response scenario.',    'bronze', 'virus',        'completion_count', 2,    None),
    ('Phishing Spotter',       'Identified and responded to your first phishing incident.',       'bronze', 'fish',         'completion_count', 3,    None),
    ('XP Earner',              'Earned your first 100 XP through scenario completions.',          'bronze', 'star',         'xp_threshold',     100,  None),
    ('Decision Maker',         'Made your first correct critical decision under pressure.',        'bronze', 'check-circle', 'completion_count', 1,    None),
    ('Incident Aware',         'Completed 5 scenario simulations across any category.',           'bronze', 'shield',       'completion_count', 5,    None),
    # Silver
    ('Network Defender',       'Completed all DDoS & Network Disruption scenarios.',             'silver', 'wifi',         'category_complete', 1,   'ddos-network-disruption'),
    ('Social Engineer Buster', 'Completed all Phishing & Social Engineering scenarios.',         'silver', 'users',        'category_complete', 1,   'phishing-social-engineering'),
    ('Data Guardian',          'Completed all Data Breach & Exfiltration scenarios.',            'silver', 'database',     'category_complete', 1,   'data-breach-exfiltration'),
    ('Insider Threat Hunter',  'Completed all Insider Threat Detection scenarios.',              'silver', 'user-x',       'category_complete', 1,   'insider-threat-detection'),
    ('XP Veteran',             'Earned a total of 500 XP across all scenarios.',                 'silver', 'award',        'xp_threshold',     500,  None),
    ('Accuracy Expert',        'Achieved a perfect score in 3 scenarios.',                       'silver', 'target',       'perfect_score',    3,    None),
    # Gold
    ('Malware Specialist',     'Completed all Malware Infection Response scenarios.',            'gold',   'virus',        'category_complete', 1,   'malware-infection-response'),
    ('APT Hunter',             'Completed all Network Intrusion & APT scenarios.',               'gold',   'shield-alert', 'category_complete', 1,   'network-intrusion-apt'),
    ('Perfect Analyst',        'Achieved a perfect score in 10 scenarios.',                      'gold',   'medal',        'perfect_score',    10,   None),
    ('Seasoned Responder',     'Completed 20 incident response simulations.',                    'gold',   'shield-check', 'completion_count', 20,   None),
    ('XP Master',              'Earned a total of 2000 XP — a true cybersecurity expert.',       'gold',   'crown',        'xp_threshold',     2000, None),
    ('Guardelio Champion',     'Completed all scenarios across all cybersecurity categories.',   'gold',   'trophy',       'all_categories',   1,    None),
]

# Combined dictionary of all 30 playable scenarios across 6 categories
ALL_PLAYABLE_SCENARIOS = {}
ALL_PLAYABLE_SCENARIOS.update(MALWARE_SCENARIOS)
ALL_PLAYABLE_SCENARIOS.update(PHISHING_SCENARIOS)
ALL_PLAYABLE_SCENARIOS.update(DDOS_SCENARIOS)
ALL_PLAYABLE_SCENARIOS.update(DATA_BREACH_SCENARIOS)
ALL_PLAYABLE_SCENARIOS.update(INSIDER_THREAT_SCENARIOS)
ALL_PLAYABLE_SCENARIOS.update(NETWORK_APT_SCENARIOS)


class Command(BaseCommand):
    help = 'Populates the Guardelio database with all 6 categories, 30 scenarios, badges, and test accounts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing seed data before re-seeding (destructive).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Warning: Clearing existing seed data...'))
            User.objects.filter(email__in=['student@guardelio.com', 'admin@guardelio.com']).delete()
            Badge.objects.all().delete()
            Scenario.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing seed data.'))

        self.stdout.write('\nGuardelio Unified Seed Starting...\n')

        categories_map = self._seed_categories()
        self._seed_scenarios(categories_map)
        self._seed_badges(categories_map)
        self._seed_test_accounts()

        self.stdout.write(self.style.SUCCESS('\n========================================='))
        self.stdout.write(self.style.SUCCESS('  Guardelio seed completed successfully!'))
        self.stdout.write(self.style.SUCCESS('=========================================\n'))
        self.stdout.write(f'Total Categories Seeded: {len(CATEGORIES)}')
        self.stdout.write(f'Total Scenarios Seeded:  {len(ALL_PLAYABLE_SCENARIOS)} / 30')
        self.stdout.write(f'Total Badges Seeded:     {len(BADGES)}')
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('  Student: student@guardelio.com  /  Student@123')
        self.stdout.write('  Admin:   admin@guardelio.com    /  Admin@123\n')

    def _seed_categories(self):
        self.stdout.write('Seeding categories...')
        categories_map = {}
        for data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if not created:
                for k, v in data.items():
                    setattr(cat, k, v)
                cat.save()
            categories_map[data['slug']] = cat
            label = '[NEW]' if created else '[OK] '
            self.stdout.write(f'  {label} {cat.name}')
        self.stdout.write(f'  -> {len(CATEGORIES)} categories ready.')
        return categories_map

    def _seed_scenarios(self, categories_map):
        self.stdout.write('\nSeeding scenario stubs and metadata...')
        created_count = 0
        for cat_slug, sid, title, difficulty, role, overview, est_min, xp_bonus, xp_perfect in SCENARIO_STUBS:
            category = categories_map.get(cat_slug)
            if not category:
                self.stdout.write(self.style.ERROR(f'  Category slug not found: {cat_slug}'))
                continue
            scenario, created = Scenario.objects.get_or_create(
                scenario_id=sid,
                defaults={
                    'category':                    category,
                    'title':                       title,
                    'difficulty':                  difficulty,
                    'student_role':                role,
                    'overview':                    overview,
                    'estimated_duration_minutes':  est_min,
                    'xp_completion_bonus':         xp_bonus,
                    'xp_perfect_score_bonus':      xp_perfect,
                    'is_active':                   True,
                },
            )
            if not created:
                scenario.category = category
                scenario.title = title
                scenario.difficulty = difficulty
                scenario.student_role = role
                scenario.overview = overview
                scenario.estimated_duration_minutes = est_min
                scenario.xp_completion_bonus = xp_bonus
                scenario.xp_perfect_score_bonus = xp_perfect
                scenario.is_active = True
                scenario.save()
            else:
                created_count += 1
        self.stdout.write(f'  -> {created_count} new scenarios, {len(SCENARIO_STUBS) - created_count} already existed.')
        self._seed_full_scenarios()

    def _seed_full_scenarios(self):
        self.stdout.write('\nSeeding fully-playable scenario steps and decision options...')
        seeded_scenarios = 0
        total_steps = 0
        total_options = 0

        for sid, (objectives_data, steps_data) in ALL_PLAYABLE_SCENARIOS.items():
            try:
                scenario = Scenario.objects.get(scenario_id=sid)
            except Scenario.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  {sid} not found — skipping.'))
                continue

            # Seed learning objectives
            for order, text in objectives_data:
                obj, created = LearningObjective.objects.get_or_create(
                    scenario=scenario, order=order,
                    defaults={'objective_text': text},
                )
                if not created and obj.objective_text != text:
                    obj.objective_text = text
                    obj.save()

            # Seed steps & options
            for step_dict in steps_data:
                step_fields = {
                    'title':          step_dict['title'],
                    'situation_text': step_dict['situation_text'],
                    'nist_phase':     step_dict['nist_phase'],
                    'step_type':      step_dict['step_type'],
                    'is_final_step':  step_dict['is_final_step'],
                    'is_active':      True,
                }
                step, created = ScenarioStep.objects.get_or_create(
                    scenario=scenario,
                    step_number=step_dict['step_number'],
                    defaults=step_fields,
                )
                if not created:
                    for k, v in step_fields.items():
                        setattr(step, k, v)
                    step.save()
                total_steps += 1

                for opt_data in step_dict.get('options', []):
                    opt_fields = {
                        'is_correct':       opt_data['is_correct'],
                        'xp_awarded':       opt_data['xp'],
                        'feedback_text':    opt_data['feedback'],
                        'consequence_type': opt_data['consequence'],
                        'display_order':    opt_data['display_order'],
                        'next_step':        None,
                    }
                    opt, opt_created = DecisionOption.objects.get_or_create(
                        step=step,
                        option_text=opt_data['text'],
                        defaults=opt_fields,
                    )
                    if not opt_created:
                        for k, v in opt_fields.items():
                            setattr(opt, k, v)
                        opt.save()
                    total_options += 1

            seeded_scenarios += 1
            self.stdout.write(f'  [OK] {sid}: {scenario.title} ({len(steps_data)} steps)')

        self.stdout.write(f'  -> All {seeded_scenarios} scenarios populated ({total_steps} steps, {total_options} options).')

    def _seed_badges(self, categories_map):
        self.stdout.write('\nSeeding badges...')
        created_count = 0
        for name, description, badge_type, icon, criteria_type, criteria_value, cat_slug in BADGES:
            category = categories_map.get(cat_slug) if cat_slug else None
            badge, created = Badge.objects.get_or_create(
                name=name,
                defaults={
                    'description':       description,
                    'badge_type':        badge_type,
                    'icon_name':         icon,
                    'criteria_type':     criteria_type,
                    'criteria_value':    criteria_value,
                    'criteria_category': category,
                    'is_active':         True,
                },
            )
            if not created:
                badge.description = description
                badge.badge_type = badge_type
                badge.icon_name = icon
                badge.criteria_type = criteria_type
                badge.criteria_value = criteria_value
                badge.criteria_category = category
                badge.is_active = True
                badge.save()
            else:
                created_count += 1
        self.stdout.write(f'  -> {created_count} new badges, {len(BADGES) - created_count} already existed.')

    def _seed_test_accounts(self):
        self.stdout.write('\nSeeding test accounts...')
        student, created = User.objects.get_or_create(
            email='student@guardelio.com',
            defaults={
                'username':   'student',
                'first_name': 'Demo',
                'last_name':  'Student',
                'role':       User.Role.STUDENT,
                'is_active':  True,
            },
        )
        if created:
            student.set_password('Student@123')
            student.save()
            StudentProfile.objects.get_or_create(user=student)
            self.stdout.write(self.style.SUCCESS('  [NEW] Student: student@guardelio.com'))
        else:
            self.stdout.write('  [OK]  Student: student@guardelio.com')

        admin, created = User.objects.get_or_create(
            email='admin@guardelio.com',
            defaults={
                'username':   'admin',
                'first_name': 'Admin',
                'last_name':  'User',
                'role':       User.Role.ADMIN,
                'is_active':  True,
                'is_staff':   True,
            },
        )
        if created:
            admin.set_password('Admin@123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  [NEW] Admin: admin@guardelio.com'))
        else:
            self.stdout.write('  [OK]  Admin: admin@guardelio.com')
