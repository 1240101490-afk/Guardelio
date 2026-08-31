"""
Guardelio — DDoS & Network Disruption Scenarios (S-DDS-01 to S-DDS-05)
NIST SP 800-61 Aligned Incident Response Simulations
"""

# ═══════════════════════════════════════════════════════════════════════════════
# S-DDS-01: Volumetric DDoS on E-Commerce Platform (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DDS_01_OBJECTIVES = [
    (1, 'Analyze bandwidth metrics and NetFlow telemetry to differentiate legitimate traffic from volumetric UDP floods.'),
    (2, 'Activate upstream DDoS cloud scrubbing protections and BGP routing under operational pressure.'),
    (3, 'Monitor origin server health and latency metrics post-mitigation.'),
]

S_DDS_01_STEPS = [
    {
        'step_number': 1,
        'title': 'Black Friday Traffic Spike',
        'situation_text': (
            'It is 00:15 on Black Friday. You are on duty as a NOC Analyst at ShopFront Retail Technologies. '
            'Suddenly, monitoring alerts light up the operations dashboard:\n\n'
            '- Inbound bandwidth spikes from 2.5 Gbps to 52.0 Gbps within 90 seconds.\n'
            '- Edge router CPU utilization reaches 98%, and packet drop rates surge to 45%.\n'
            '- Customer checkout transactions are failing worldwide.\n\n'
            'The E-Commerce Director demands to know if this is an overwhelming rush of genuine holiday shoppers or a cyber attack.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Traffic Flow & Protocol Analysis',
        'situation_text': (
            'You pull NetFlow and sFlow metrics from the edge border routers. You inspect the traffic profile:\n\n'
            '- Protocol: 94% UDP traffic directed at destination ports 80, 443, and random high ports (UDP/5353, UDP/11211).\n'
            '- Packet Length: Uniform 1,400-byte payloads with randomized data.\n'
            '- Source IPs: Over 800,000 distinct IP addresses exhibiting spoofed Class A/B header characteristics.\n'
            '- Legitimate HTTPS (TCP/443) traffic is being starved of bandwidth.\n\n'
            'What type of incident are you dealing with?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A volumetric UDP flood DDoS attack attempting to saturate the ISP upstream transit link bandwidth.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Legitimate web traffic uses TCP (HTTP/HTTPS). A massive 50+ Gbps flood of uniform UDP packets '
                    'with spoofed source IPs is a textbook volumetric DDoS attack aimed at link exhaustion.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A surge of legitimate Black Friday shoppers using modern HTTP/3 protocols.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. While HTTP/3 uses QUIC (UDP), legitimate shopping traffic consists of variable packet sizes, '
                    'valid TLS handshakes, and application-level session flows—not randomized high-volume UDP floods on non-standard ports.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'An internal database replication loop causing broadcast storms.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The traffic is arriving from external WAN transit links via hundreds of thousands of external IPs, '
                    'not from internal LAN database segments.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Emergency Containment Strategy',
        'situation_text': (
            'The attack is filling 95% of your total 50 Gbps transit pipe from your Tier-1 ISP. '
            'Local firewall rules cannot drop the packets because the physical connection to the datacenter is completely saturated before traffic reaches your firewalls.\n\n'
            'What is the most effective containment action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Activate cloud DDoS scrubbing via BGP Anycast redirection (e.g. Cloudflare / Akamai / AWS Shield) to absorb and filter the 50 Gbps flood in the cloud before reaching origin.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. When an attack exceeds physical pipe capacity, on-premises firewalls are useless. '
                    'BGP Anycast cloud scrubbing diverts incoming traffic across a multi-terabit global network, '
                    'filtering out the malicious UDP flood and passing only clean TCP traffic to your origin.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Configure `iptables` drop rules on all web application servers locally.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Dropping packets on the servers does not help when the upstream network interface and ISP circuit are completely choked with saturated bandwidth.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Restart all core routers and switches to clear their packet memory buffers.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Restarting network hardware causes total self-inflicted downtime and does not stop the incoming flood once routers come back online.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Upstream ISP Coordination & Origin Lockdown',
        'situation_text': (
            'BGP routes have been announced to the cloud DDoS mitigation provider. Traffic is now routing through the scrubbing center.\n\n'
            'However, monitoring shows ~2 Gbps of direct attack traffic is still hitting your origin IP address directly, bypassing the cloud proxy.\n\n'
            'How should you eradicate this direct origin leakage?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Restrict edge firewall ingress rules to ONLY accept connections from the cloud scrubbing provider’s published IP ranges, dropping all direct public traffic.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. Locking down edge firewalls to exclusively whitelist scrubbing center IP ranges prevents adversaries from attacking '
                    'the origin IP directly, forcing 100% of traffic through the protective cloud shield.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Request the ISP to blackhole (Null0 route) your entire `/24` subnet.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Blackholing (Null0 routing) the subnet stops the attack but also permanently kills all legitimate customer traffic, '
                    'completing the attacker’s denial-of-service objective.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Change the DNS records back to the origin server IP.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Reverting DNS records to origin removes the cloud mitigation layer and directly re-exposes the servers to the full 50 Gbps flood.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & Capacity Hardening',
        'situation_text': (
            'The volumetric DDoS attack has been fully mitigated. The scrubbing center filtered 52 Gbps of malicious UDP traffic, '
            'while legitimate shoppers experienced normal site performance and sub-second checkout speeds.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: 52 Gbps Volumetric UDP Flood targeting infrastructure bandwidth exhaustion.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Monitoring threshold configuration and emergency vendor playbook availability\n'
            '- Detection & Analysis: NetFlow protocol breakdown and spoofed IP entropy confirmation\n'
            '- Containment: BGP Anycast cloud scrubbing activation and origin IP ACL whitelisting\n'
            '- Post-Incident Activity: Review of DDoS defense architecture and auto-mitigation thresholds\n\n'
            'STRATEGIC HARDENING ACTIONS:\n'
            '1. Switched cloud DDoS protection from "on-demand" to "always-on" proxy mode for all public ecommerce endpoints.\n'
            '2. Rotated origin IP addresses and hidden origin infrastructure behind private interconnects (AWS DirectConnect).\n'
            '3. Configured rate-limiting rules at the cloud edge to automatically challenge abnormal traffic surges.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DDS-02: DNS Amplification Attack on ISP (Intermediate, 6 steps, 4 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DDS_02_OBJECTIVES = [
    (1, 'Identify DNS ANY request amplification characteristics and reflection vectors.'),
    (2, 'Apply Response Rate Limiting (RRL) and upstream BGP Flowspec filtering rules.'),
    (3, 'Coordinate with upstream transit providers to filter reflected traffic before reaching customer links.'),
]

S_DDS_02_STEPS = [
    {
        'step_number': 1,
        'title': 'Nameserver Schedulers Under Siege',
        'situation_text': (
            'At 16:45, FastNet Internet Services NOC reports severe packet drops affecting authoritative DNS clusters. '
            'Multiple enterprise customer domains are failing to resolve, causing widespread email and web outages across 400 client organizations.\n\n'
            'Edge interfaces on nameservers `ns1.fastnet.net` and `ns2.fastnet.net` are receiving over 80 million packets per second.\n\n'
            'You are the Senior Network Security Engineer on duty.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Packet Capture & Reflection Analysis',
        'situation_text': (
            'You run `tcpdump -nn -c 1000 -i eth0 udp port 53` on the primary authoritative server. You observe:\n\n'
            '- Thousands of source IP addresses on UDP port 53 returning massive DNS responses.\n'
            '- The query payload is `IN ANY isc.org` or `IN ANY ripe.net` containing DNSSEC RRSIG records.\n'
            '- Inbound request size: ~64 bytes. Inbound response size: ~3,800 bytes.\n'
            '- Destination IP: FastNet’s authoritative DNS virtual IP (`198.51.100.53`).\n\n'
            'What specific attack mechanism is occurring?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A DNS Amplification / Reflection attack where open recursive resolvers worldwide are abused using spoofed requests to flood the target with 50x-amplified responses.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. The attacker sends 64-byte `ANY` queries with spoofed source IP (victim\'s IP) to misconfigured open resolvers, '
                    'which return 3,800-byte amplified responses. This generates enormous volumetric bandwidth multiplication.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A DNS cache poisoning attack attempting to overwrite zone records.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Cache poisoning targets recursive caching resolvers with forged transaction IDs, not authoritative servers flooded with high-volume amplified traffic.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A slow-read HTTP DoS attack consuming Apache connection pools.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Telemetry clearly shows UDP port 53 DNS reflection packets, not Layer 7 HTTP connection pool exhaustion.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Local Server Rate Limiting & Defense',
        'situation_text': (
            'While network links are congested, you must protect the BIND/Named DNS server daemon from crashing.\n\n'
            'What authoritative DNS configuration helps mitigate reflected and repetitive queries directly on the nameservers?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable Response Rate Limiting (RRL) in BIND and disable recursion globally on all authoritative nameservers.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Response Rate Limiting (RRL) throttles identical responses to high-volume query patterns, '
                    'and disabling open recursion ensures your own servers cannot be weaponized as reflectors.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Disable UDP port 53 entirely on the nameservers and only allow TCP port 53.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Standard DNS resolution across the internet relies primarily on UDP. Disabling UDP port 53 breaks domain resolution for millions of legitimate clients.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Delete all DNSSEC records from all customer zones.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Deleting DNSSEC breaks cryptographic validation for secure domains and does not stop the external flood already heading towards the server IP.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Upstream Mitigation via BGP Flowspec',
        'situation_text': (
            'Even with RRL, the inbound bandwidth saturation (70 Gbps) is choking the physical uplinks between your routers and Tier-1 transit carriers.\n\n'
            'You need to filter the attack traffic inside the carrier backbone before it enters FastNet’s physical lines.\n\n'
            'What carrier-grade protocol is designed for this rapid multi-provider traffic filtering?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy BGP Flowspec (RFC 5575 / RFC 8955) rules to upstream transit providers to match UDP port 53 traffic with packet lengths > 2,000 bytes and rate-limit/drop at the carrier edge.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. BGP Flow Specification (Flowspec) allows network operators to dynamically distribute granular Layer 3/4 firewall rules '
                    '(protocol, port, packet length) to upstream transit providers, neutralizing reflection floods in the carrier core.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Send individual abuse emails to all 50,000 open DNS resolvers asking them to patch their servers.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Manual abuse reports take days or weeks and cannot resolve an active live network emergency.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Change the BGP autonomous system number (ASN) of FastNet.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Changing an ISP\'s ASN is impossible during an incident and would disconnect the entire ISP from global routing tables.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Validation of Authoritative Resolution',
        'situation_text': (
            'The upstream BGP Flowspec filter is active. Reflected packets over 2,000 bytes are being dropped in transit.\n\n'
            'You now verify that standard customer DNS resolution has returned to normal latency (<20ms).\n\n'
            'How do you validate the health and correctness of customer domain lookups globally?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Run distributed DNS queries across global looking-glasses and monitoring probes (e.g., RIPE Atlas) verifying standard A/AAAA/MX response latency and 100% resolution success.',
                'is_correct': True,
                'xp': 25,
                'feedback': (
                    'Correct. Using geographically distributed probes confirms that legitimate low-byte queries resolve worldwide without being collateral damage of the Flowspec filters.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Query `localhost` on the nameserver console once.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Localhost queries do not test external network transit links, carrier Flowspec filters, or global latency.'
                ),
                'consequence': 'neutral',
                'display_order': 2,
            },
            {
                'text': 'Turn off monitoring alerts to see if any customers call the helpdesk.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Relying on customer complaints instead of proactive telemetry violates SLA obligations.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Post-Incident Review & Anti-Amplification Strategy',
        'situation_text': (
            'The DNS reflection attack has been mitigated. Over 70 Gbps of amplified traffic was filtered, '
            'and authoritative name resolution for all 400 customer domains is fully restored.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK MECHANISM: DNS ANY Reflection/Amplification (50x multiplier) targeting authoritative infrastructure.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Telemetry sensor deployment and packet capture automation\n'
            '- Detection & Analysis: Reflection factor calculation, query payload identification\n'
            '- Containment: Response Rate Limiting (RRL) activation, recursion lockdown\n'
            '- Eradication: Upstream BGP Flowspec distribution across Tier-1 transit partners\n'
            '- Recovery: Global looking-glass validation\n'
            '- Post-Incident Activity: Upstream automated Flowspec peering agreements\n\n'
            'INFRASTRUCTURE ENHANCEMENTS:\n'
            '1. Automated BGP Flowspec trigger upon detecting UDP/53 traffic > 20 Gbps.\n'
            '2. Deployed Anycast DNS architecture across 6 global geographic POPs to disperse traffic load.\n'
            '3. Verified BCP 38 / Source Address Validation across all FastNet downstream customer links.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DDS-03: Application-Layer Attack on Banking Portal (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DDS_03_OBJECTIVES = [
    (1, 'Diagnose Layer 7 Slowloris and Slow POST attacks evading standard volumetric DDoS thresholds.'),
    (2, 'Configure Web Application Firewall (WAF) challenge-response mechanisms and connection timeout controls.'),
    (3, 'Isolate application thread pools and preserve database connection integrity under attack.'),
    (4, 'Establish forensic timelines and resilient reverse-proxy architectures.'),
]

S_DDS_03_STEPS = [
    {
        'step_number': 1,
        'title': 'The Silent Banking Outage',
        'situation_text': (
            'At 10:00 AM on a Monday, the mobile banking app and web portal of NovaBanque Digital Services become completely unresponsive. '
            'Online banking customers cannot log in, check balances, or transfer money.\n\n'
            'Curiously, the NOC network bandwidth graph shows only 15% link utilization (under 400 Mbps). '
            'The volumetric DDoS mitigation system did NOT trigger because overall traffic volume is well below alert thresholds.\n\n'
            'You are the Incident Commander leading the crisis response.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Web Server Thread Pool Diagnosis',
        'situation_text': (
            'You inspect the reverse proxies (NGINX) and application servers (Tomcat/Java). '
            'You check system metrics and process tables:\n\n'
            '- Web server worker connections: 10,000 / 10,000 (100% capacity reached).\n'
            '- Server state: Thousands of connections are held open in `W` (Sending Reply) or `R` (Reading Request) state.\n'
            '- Client requests are sending partial HTTP headers (e.g. `X-a: b\\r\\n`) every 15 seconds, keeping the TCP connection alive indefinitely.\n\n'
            'What specific Layer 7 attack vector is causing this outage?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A Slowloris / Slow HTTP Headers attack designed to exhaust web server thread/connection pools with minimal bandwidth consumption.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Slowloris sends incomplete HTTP headers at periodic intervals, forcing the web server to keep worker threads open '
                    'waiting for the request to complete. This exhausts the server’s connection limit without generating high bandwidth volume.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A volumetric ICMP Ping Flood overwhelming network switches.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Link bandwidth is only at 15% and ICMP traffic is negligible; the bottleneck is web server worker threads.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A database deadlock caused by a software release bug.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Telemetry proves the reverse proxy connection pool is exhausted by slow partial HTTP client headers before requests even reach the database.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Reverse Proxy Timeout Tuning',
        'situation_text': (
            'The Slowloris attack is identified. You need to configure the reverse proxy layer to rapidly terminate '
            'connections that fail to send complete HTTP headers within a reasonable timeframe.\n\n'
            'Which reverse proxy configuration changes immediately neutralize Slowloris attacks?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Lower `client_header_timeout` and `client_body_timeout` to 5 seconds, and enforce `client_header_buffer_size` and minimum data transmission rate limits (`send_lowat` / `limit_req`).',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Reducing client header and body timeouts from default 60s down to 5s forces the proxy to close connections '
                    'that trickle headers, instantly freeing up worker connections for legitimate mobile app users.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Increase `client_header_timeout` to 300 seconds so slow mobile connections have more time.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Increasing the timeout allows the attacker to hold connections open even longer, worsening the denial of service.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Disable HTTPS and switch the entire banking portal to HTTP port 80.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling encryption exposes customer banking credentials and does nothing to solve thread pool exhaustion.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Mitigating Distributed Botnet Slow POSTs',
        'situation_text': (
            'After tuning header timeouts, the attacker switches tactics to Slow POST (RUDY — R-U-Dead-Yet):\n'
            '- Attackers send legitimate `Content-Length: 1000000` headers on login forms.\n'
            '- They transmit message body bytes at 1 byte every 10 seconds.\n'
            '- Over 4,000 distinct IP addresses across multiple cloud hosting providers are participating.\n\n'
            'What WAF defense mechanism effectively stops distributed Layer 7 slow POST bots?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enforce minimum client body data transfer rate (e.g., `client_body_timeout 10s`, `reset_timedout_connections on`) and deploy WAF JavaScript challenges / Managed Bot Protection on login endpoints.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Enforcing minimum body transmission throughput requirements drops connections transmitting below acceptable thresholds, '
                    'and WAF JavaScript challenges filter out scripted bots that cannot execute JS.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Block all POST requests across the banking website.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Blocking POST requests prevents all customers from logging in, submitting forms, or transferring money.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Add 1,000 new Tomcat backend application servers to outlast the attack.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Adding backend servers is expensive and ineffective against unthrottled slow HTTP connections; '
                    'the reverse proxy connection pools will still be exhausted.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Database Connection Pool Protection',
        'situation_text': (
            'The reverse proxy filtering is working. You must now ensure the backend database connection pools (HikariCP / PostgreSQL) '
            'were not corrupted or left with orphaned transactions during the period of worker exhaustion.\n\n'
            'What eradication and integrity verification action should you perform on the database tier?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Audit active database backend processes, terminate orphaned `idle in transaction` queries, and verify connection pool health and transaction isolation integrity.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Slow client disconnects can leave backend application threads holding database connections. '
                    'Auditing and cleaning idle-in-transaction locks prevents backend database deadlocks.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Drop the primary database cluster and restore from last night’s backup.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. There was no database corruption or data breach; dropping the live database destroys all current morning transactions.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Disable all database password authentication to speed up query execution.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling authentication creates an immediate severe security vulnerability.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Safe Service Recovery & Traffic Ramp-Up',
        'situation_text': (
            'Reverse proxy timeouts are tuned, WAF bot mitigations are active, and backend database pools are healthy.\n\n'
            'How do you safely restore customer traffic while monitoring for secondary attack waves?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Gradually reopen traffic through the load balancers while monitoring active connection counts, HTTP 5xx error rates, response latency, and customer login success metrics in real-time.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Controlled traffic restoration combined with real-time monitoring of connection metrics '
                    'validates that mitigation controls hold under legitimate customer traffic load.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Instantly turn off all logging and monitoring to maximize CPU speed.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling monitoring blinds the team to secondary attack waves and system failures.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Keep the service offline for 72 hours until the attacker gets bored.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Prolonging downtime violates banking regulatory availability requirements.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Resilience Architecture',
        'situation_text': (
            'NovaBanque digital banking services have been fully restored. Zero customer accounts were compromised, '
            'and all slow HTTP connections were successfully dropped with no database deadlock.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: Layer 7 Slowloris & Slow POST (RUDY) Application-Layer DoS evading volumetric thresholds.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Low-bandwidth outage triage\n'
            '- Detection & Analysis: Web server connection pool state analysis, Slowloris fingerprinting\n'
            '- Containment: Aggressive reverse-proxy header/body timeout reduction, WAF JS challenge\n'
            '- Eradication: Backend database connection pool cleanup, idle transaction termination\n'
            '- Recovery: Staged load-balancer traffic restoration\n'
            '- Post-Incident Activity: Architectural hardening for asymmetric L7 attacks\n\n'
            'PERMANENT ARCHITECTURAL UPGRADES:\n'
            '1. Standardized aggressive timeouts across all cloud reverse proxies (client_header_timeout: 5s).\n'
            '2. Implemented AI-driven behavioral bot mitigation in WAF edge layer.\n'
            '3. Configured synthetic health-check monitors that simulate complete end-to-end user transactions every 30 seconds.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DDS-04: SYN Flood on Government Portal (Beginner, 5 steps, 3 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DDS_04_OBJECTIVES = [
    (1, 'Understand TCP three-way handshake mechanics and SYN queue state exhaustion.'),
    (2, 'Enable Linux kernel SYN cookies and firewall TCP state protections.'),
    (3, 'Validate legitimate citizen connection recovery post-mitigation.'),
]

S_DDS_04_STEPS = [
    {
        'step_number': 1,
        'title': 'Tax Filing Deadline Crisis',
        'situation_text': (
            'It is 36 hours before the national annual tax filing deadline. '
            'Citizens trying to access the National Revenue Agency self-assessment portal report "Connection Timed Out" errors.\n\n'
            'The Agency Director warns that if the system is down for even 2 hours, hundreds of thousands of citizens will miss '
            'the statutory deadline, triggering national press attention and parliamentary inquiry.\n\n'
            'You are the Junior Network Analyst tasked with triaging the portal servers.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'TCP Connection State Analysis',
        'situation_text': (
            'You run `netstat -n -p tcp` and `ss -s` on the front-end load balancers. You observe:\n\n'
            '- Total active TCP connections: 65,535 (maximum kernel backlog reached).\n'
            '- Connection status: Over 98% of connections are in `SYN_RECV` state.\n'
            '- Inbound traffic consists of continuous TCP packets with the SYN flag set, but no subsequent ACK packets are ever received.\n'
            '- Source IP addresses are completely randomized across global IP ranges.\n\n'
            'What specific network protocol attack is being executed?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'A TCP SYN Flood attack exploiting the half-open TCP handshake to exhaust the server’s SYN queue backlog.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. A SYN flood sends continuous SYN packets with spoofed source IPs. The server allocates memory '
                    'in its SYN backlog queue and waits for an ACK that never comes, starving legitimate connections.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'A DNS tunneling attack exfiltrating tax records.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The traffic is pure TCP SYN traffic on web ports, not DNS queries over port 53.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'A Man-in-the-Middle (MitM) ARP spoofing attack on the local switch.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Telemetry demonstrates TCP state table exhaustion from external WAN traffic, not local ARP layer manipulation.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Kernel SYN Cookie & Backlog Hardening',
        'situation_text': (
            'The SYN flood is filling the server backlog queue (`tcp_max_syn_backlog`). '
            'You must configure the Linux kernel to handle half-open connections without allocating memory until the handshake is complete.\n\n'
            'Which kernel feature prevents SYN backlog exhaustion without dropping legitimate connections?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable TCP SYN Cookies (`sysctl -w net.ipv4.tcp_syncookies=1`) and increase `net.ipv4.tcp_max_syn_backlog` and `net.core.somaxconn`.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. SYN cookies encode connection parameters into the SYN-ACK sequence number, avoiding memory allocation '
                    'until the client returns a valid ACK. This completely neutralizes SYN flood queue exhaustion.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Disable all incoming TCP connections on port 443.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disabling port 443 turns off HTTPS access entirely, making the portal unavailable to all citizens.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Set `net.ipv4.tcp_syncookies=0` to speed up CPU packet processing.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Setting syncookies to 0 disables SYN cookie protection, leaving the system completely vulnerable to backlog exhaustion.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Firewall TCP State Protection & SYN Proxy',
        'situation_text': (
            'SYN cookies are enabled on the servers. To further reduce load on server CPUs, you configure the perimeter firewall.\n\n'
            'What firewall feature terminates the initial TCP handshake at the firewall before passing established connections to backend servers?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Enable SYN Proxy / TCP Intercept on the perimeter firewall to validate the complete 3-way handshake before forwarding legitimate sessions to backend servers.',
                'is_correct': True,
                'xp': 20,
                'feedback': (
                    'Correct. A firewall SYN Proxy intercepts client SYNs, responds with a SYN-ACK, and only forwards the connection to the backend server '
                    'once a valid ACK is received from the client, shielding backend web servers completely.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Allow all incoming packets without state tracking (stateless mode).',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Stateless mode allows spoofed SYN floods to reach backend servers unfiltered.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Block all IP addresses from foreign countries.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Partially flawed — spoofed SYN floods easily spoof domestic IP addresses, and many legitimate citizens file taxes while travelling abroad.'
                ),
                'consequence': 'neutral',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Post-Incident Review & System Normalization',
        'situation_text': (
            'The SYN flood attack was successfully mitigated. SYN cookies and firewall SYN proxy protections allowed '
            'legitimate citizens to connect and file taxes seamlessly with zero server downtime.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK MECHANISM: TCP SYN Flood state table exhaustion during peak national deadline window.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Emergency response during peak tax filing period\n'
            '- Detection & Analysis: `SYN_RECV` state table analysis and SYN flood identification\n'
            '- Containment: Kernel TCP syncookies enablement, backlog buffer expansion\n'
            '- Eradication: Perimeter firewall SYN Proxy enforcement\n'
            '- Post-Incident Activity: Baseline sysctl template deployment\n\n'
            'CONFIGURATIONS STANDARDIZED:\n'
            '1. Permanent deployment of `net.ipv4.tcp_syncookies = 1` across all golden server images.\n'
            '2. Enabled hardware-accelerated TCP SYN Proxy on border firewalls.\n'
            '3. Configured automated alert notifications when `SYN_RECV` count exceeds 5,000.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# S-DDS-05: Multi-Vector DDoS with Extortion (Advanced, 7 steps, 5 decisions)
# ═══════════════════════════════════════════════════════════════════════════════

S_DDS_05_OBJECTIVES = [
    (1, 'Coordinate multi-layered defense against concurrent Layer 3/4 reflection and Layer 7 botnet attacks.'),
    (2, 'Manage extortion response policy following law enforcement and CISA anti-ransom guidelines.'),
    (3, 'Apply granular traffic filtering without dropping legitimate user traffic during live operational events.'),
    (4, 'Perform root cause forensic attribution and upstream mitigation.'),
]

S_DDS_05_STEPS = [
    {
        'step_number': 1,
        'title': 'Tournament Outage & The Extortion Email',
        'situation_text': (
            'At 19:30 on Saturday, the Grand Finals of the Apex Global Gaming Championship are broadcasting live to 1.2 million viewers. '
            'Suddenly, game servers disconnect and the livestream collapses under an unprecedented 320 Gbps assault.\n\n'
            'Simultaneously, an email arrives in the CISO and NOC inboxes from "ShadowLocker Syndicate":\n'
            '"We are flooding your infrastructure with 300+ Gbps. Pay 5 Bitcoin ($300,000) within 30 minutes to BTC address 1BoatSLR... '
            'or your championship will be offline all weekend."\n\n'
            'You are the Security Operations Lead in the command room.'
        ),
        'nist_phase': 'preparation',
        'step_type': 'info',
        'is_final_step': False,
        'options': [],
    },
    {
        'step_number': 2,
        'title': 'Deconstructing the Multi-Vector Profile',
        'situation_text': (
            'You analyze the attack traffic across upstream telemetry sensors. You identify three distinct vectors running simultaneously:\n\n'
            '1. NTP Amplification (UDP port 123) monlist reflection (~180 Gbps)\n'
            '2. SSDP Reflection (UDP port 1900) abusing IoT devices (~90 Gbps)\n'
            '3. Layer 7 HTTPS TLS Handshake / Flood targeting the matchmaking API (~50 Gbps / 400,000 req/sec)\n\n'
            'Why do sophisticated adversaries employ multi-vector DDoS attacks?'
        ),
        'nist_phase': 'detection',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'To overwhelm multiple architectural layers simultaneously (saturating upstream bandwidth with L3/4 reflection while exhausting server CPUs with L7 SSL renegotiation).',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Multi-vector attacks combine volumetric reflection (filling network pipes) with compute-intensive application attacks '
                    '(exhausting CPU/TLS capacity), rendering single-point defense mechanisms ineffective.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Because NTP and SSDP protocols are required to transmit ransomware encryption keys.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. NTP and SSDP are public UDP protocols abused for bandwidth reflection, not ransomware key distribution.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'The attacker accidentally ran three separate testing tools at the same time.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The coordinated multi-vector flood combined with a timed extortion note is an intentional, organized cybercrime operation.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 3,
        'title': 'Extortion Policy & Executive Guidance',
        'situation_text': (
            'The Executive Producer asks if the company should quickly pay the 5 Bitcoin ransom to save the tournament broadcast.\n\n'
            'What is the mandatory policy guidance regarding DDoS extortion payments according to CISA, FBI, and corporate governance?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Do NOT pay the ransom. Payment does not guarantee attack cessation, funds criminal enterprises, marks the organization for repeated extortion, and may violate legal sanctions.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. CISA and law enforcement strongly advise against paying DDoS extortion demands. '
                    'Attackers frequently demand more money after payment, and paying provides zero technical protection against future floods.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Pay 2.5 Bitcoin as a deposit to see if they reduce the attack volume by half.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Negotiating or paying extortionists legitimizes criminal extortion and exposes the company to repeated demands.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Offer to give the attackers free in-game skins and VIP tournament tickets in exchange for peace.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Unprofessional and completely ineffective against organized criminal extortion syndicates.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 4,
        'title': 'Layer 3/4 Upstream Volumetric Scrubbing',
        'situation_text': (
            'The executive team approves total technical defense with zero ransom payment.\n\n'
            'You must immediately contain the 270 Gbps of UDP/123 (NTP) and UDP/1900 (SSDP) reflection traffic choking the ingress transit pipes.\n\n'
            'What is the immediate upstream mitigation action?'
        ),
        'nist_phase': 'containment',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Engage cloud DDoS scrubbing providers to absorb traffic via Anycast, and issue upstream transit ACL drop rules for incoming UDP fragments, UDP/123, and UDP/1900.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Enterprise game servers do not receive inbound public NTP monlist or SSDP responses. '
                    'Dropping UDP/123 and UDP/1900 at the cloud scrubbing tier immediately eliminates 270 Gbps of reflection traffic.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Ask game players to disconnect from their home routers and use cellular data.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. The attack is targeting the central game server infrastructure, not individual players\' homes.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Unplug all network cables from the datacenter switches.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Disconnecting the infrastructure creates permanent self-inflicted outage.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 5,
        'title': 'Mitigating Layer 7 HTTPS TLS Handshake Floods',
        'situation_text': (
            'The 270 Gbps volumetric reflection flood is dropped by the scrubbing tier. '
            'However, the game matchmaking API is still struggling under 400,000 HTTPS requests/sec from a botnet.\n\n'
            'What Layer 7 mitigation strategy stops the HTTPS botnet flood without disconnecting legitimate game clients?'
        ),
        'nist_phase': 'eradication',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Deploy WAF TLS session resumption caching, enforce client certificate / HMAC token validation on game API endpoints, and apply behavioral rate limiting per player account ID.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Requiring cryptographic client HMAC tokens embedded in the game binary authenticates genuine game clients '
                    'and drops unauthorized botnet HTTPS floods at the edge.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Disable TLS encryption and accept all API traffic in plaintext.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Removing TLS exposes player authentication credentials and session tokens to interception.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'IP ban every player who connects more than once every 5 minutes.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Legitimate game matchmaking requires multiple rapid API calls; arbitrary IP bans create false positives and lock out legitimate players.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 6,
        'title': 'Game Cluster Health Validation & Match Resumption',
        'situation_text': (
            'Both the Layer 3/4 volumetric reflection and Layer 7 HTTPS flood are neutralized. '
            'Origin latency has dropped to a healthy 18ms.\n\n'
            'What operational checks must you execute before resuming the championship finals broadcast?'
        ),
        'nist_phase': 'recovery',
        'step_type': 'decision',
        'is_final_step': False,
        'options': [
            {
                'text': 'Conduct automated synthetic matchmaking transactions, verify game server tick rate (128 tick), check stream encoder stability, and confirm zero packet loss across tournament pods.',
                'is_correct': True,
                'xp': 30,
                'feedback': (
                    'Correct. Verifying game server tick rates, stream encoders, and packet loss metrics ensures a flawless '
                    'experience for esports competitors and spectators before going back on-air.'
                ),
                'consequence': 'positive',
                'display_order': 1,
            },
            {
                'text': 'Immediately start the match without testing to save broadcast time.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Resuming without verifying server tick rates and packet loss risks player mid-match disconnects.'
                ),
                'consequence': 'negative',
                'display_order': 2,
            },
            {
                'text': 'Change all player in-game names to random numbers.',
                'is_correct': False,
                'xp': 0,
                'feedback': (
                    'Incorrect. Has zero technical relevance to network latency and game server stability.'
                ),
                'consequence': 'negative',
                'display_order': 3,
            },
        ],
    },
    {
        'step_number': 7,
        'title': 'Post-Incident Review & Law Enforcement Handover',
        'situation_text': (
            'The Grand Finals resumed and completed successfully with over 1.4 million live viewers. '
            'Zero ransom was paid, all 320 Gbps of attack traffic was mitigated, and the extortion attempt failed completely.\n\n'
            'LESSONS LEARNED:\n\n'
            'ATTACK PROFILE: 320 Gbps Multi-Vector DDoS (NTP + SSDP + HTTPS L7 Flood) accompanied by financial extortion.\n\n'
            'NIST PHASES COMPLETED:\n'
            '- Preparation: Rapid incident command establishment during live international broadcast\n'
            '- Detection & Analysis: Multi-vector deconstruction (NTP, SSDP, TLS floods)\n'
            '- Containment: Anti-extortion policy execution, Anycast cloud scrubbing engagement\n'
            '- Eradication: Protocol drop rules (UDP 123/1900), game client HMAC token validation\n'
            '- Recovery: Server tick-rate and latency validation, successful tournament resumption\n'
            '- Post-Incident Activity: Law enforcement (FBI Cyber Division) evidence package submission\n\n'
            'STRATEGIC DEFENSE ACTIONS:\n'
            '1. Preserved email headers, Bitcoin addresses, and NetFlow PCAP forensic packages for FBI cybercrime referral.\n'
            '2. Hardened game client API authentication using hardware-bound device attestations.\n'
            '3. Contracted always-on 1 Tbps multi-cloud DDoS scrubbing SLAs for all major esports events.'
        ),
        'nist_phase': 'post_incident',
        'step_type': 'info',
        'is_final_step': True,
        'options': [],
    },
]

DDOS_SCENARIOS = {
    'S-DDS-01': (S_DDS_01_OBJECTIVES, S_DDS_01_STEPS),
    'S-DDS-02': (S_DDS_02_OBJECTIVES, S_DDS_02_STEPS),
    'S-DDS-03': (S_DDS_03_OBJECTIVES, S_DDS_03_STEPS),
    'S-DDS-04': (S_DDS_04_OBJECTIVES, S_DDS_04_STEPS),
    'S-DDS-05': (S_DDS_05_OBJECTIVES, S_DDS_05_STEPS),
}
