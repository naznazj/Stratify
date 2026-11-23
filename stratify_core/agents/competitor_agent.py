"""
Agent 2: Competitor Intelligence Analyst
Responsibilities:
- Direct and indirect competitor identification
- Competitor offerings, features & pricing tiers
- Market positioning map
- Documented strengths and documented customer complaints/weaknesses
- Exploitable market white space & competitive gaps
"""
from typing import Dict, Any, List
from stratify_core.agents.base_agent import BaseAgent
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand
from stratify_core.verification_service import FactClassification

class CompetitorIntelligenceAgent(BaseAgent):
    def __init__(self, token_tracker, verification_service):
        super().__init__(
            name="competitor_agent",
            role_title="Competitor Intelligence Analyst",
            token_tracker=token_tracker,
            verification_service=verification_service
        )

    def execute(self, command: StratifyCommand, profile: IndustryProfile, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        ind_key = profile.industry_key
        loc = profile.geographic_market
        is_ph = "philippines" in loc.lower() or "ph" in loc.lower()

        input_tokens = 980
        output_tokens = 920

        competitors: List[Dict[str, Any]] = []

        if ind_key == "healthcare":
            if is_ph:
                competitors = [
                    {
                        "name": "KonsultaMD",
                        "type": "Direct",
                        "website": "https://konsulta.md",
                        "offerings": "Teleconsultations, medicine delivery, at-home lab diagnostics booking",
                        "pricing": "₱60 - ₱500 / consultation; Family plans from ₱999/yr",
                        "positioning": "Mass-market 24/7 telehealth backed by 917Ventures (Globe)",
                        "strengths": "Massive consumer distribution, telco carrier billing, broad physician network",
                        "weaknesses": "Inconsistent doctor punctuality, app UI latency during peak hours, limited clinic EHR integrations",
                        "market_gap": "Lacks seamless deep integration with regional standalone clinics and hospital operating systems"
                    },
                    {
                        "name": "NowServing by SeriousMD",
                        "type": "Direct",
                        "website": "https://nowserving.com",
                        "offerings": "Doctor appointment scheduling, teleconsult, prescription management, SeriousMD EHR",
                        "pricing": "Free for patients; ₱1,500 - ₱3,500/mo doctor SaaS subscription",
                        "positioning": "Doctor-first clinical EHR and patient management portal",
                        "strengths": "Deep loyalty among private medical practitioners, robust offline EHR capabilities",
                        "weaknesses": "Complex onboarding for non-tech-savvy clinics, limited enterprise hospital multi-department modules",
                        "market_gap": "Enterprise-grade inpatient bed allocation and automated PhilHealth claims processing"
                    },
                    {
                        "name": "Kindred Health",
                        "type": "Indirect / Hybrid",
                        "website": "https://mykindred.co",
                        "offerings": "Omnichannel women's health clinics and virtual consultations",
                        "pricing": "₱1,200 - ₱4,500 per specialized service package",
                        "positioning": "Premium, judgment-free specialized women's health destination",
                        "strengths": "Strong brand aesthetic, high consumer NPS, high aesthetic physical clinics",
                        "weaknesses": "Geographically restricted to Metro Manila high-income hubs (BGC, QC)",
                        "market_gap": "Affordable suburban and provincial specialized care networks"
                    },
                    {
                        "name": "MedGrocer",
                        "type": "Indirect / B2B",
                        "website": "https://medgrocer.com",
                        "offerings": "Corporate on-site clinics, corporate wellness, medicine management",
                        "pricing": "Custom enterprise annual corporate retainers (₱250k - ₱3M+)",
                        "positioning": "Enterprise B2B managed corporate healthcare partner",
                        "strengths": "High enterprise BPO client retention, reliable medical staff deployment",
                        "weaknesses": "Slower innovation cycles on patient-facing mobile apps",
                        "market_gap": "On-demand flexible micro-clinic services for SMEs with fewer than 100 employees"
                    }
                ]
            else:
                competitors = [
                    {
                        "name": "Epic Systems",
                        "type": "Direct / Enterprise",
                        "website": "https://www.epic.com",
                        "offerings": "Comprehensive EHR, clinical workflows, patient portal (MyChart)",
                        "pricing": "$500,000 - $100M+ enterprise licensing & deployment",
                        "positioning": "Dominant hospital network and academic medical center standard",
                        "strengths": "Massive clinical database, gold-standard hospital market share, deep interoperability",
                        "weaknesses": "Prohibitive costs, multi-year implementation, legacy clunky UI, despised by small clinics",
                        "market_gap": "Lightweight, AI-first clinical documentation and modern mobile-native outpatient workflows"
                    },
                    {
                        "name": "Teladoc Health",
                        "type": "Direct / Telehealth",
                        "website": "https://www.teladoc.com",
                        "offerings": "Virtual primary care, chronic condition management (Livongo), mental health",
                        "pricing": "Per-Member-Per-Month (PMPM) enterprise insurance contracts + $75/visit cash",
                        "positioning": "Global enterprise virtual care conglomerate",
                        "strengths": "Massive insurer distribution, employer benefits integration",
                        "weaknesses": "Depersonalized care, physician turnover, high corporate losses post-Livongo acquisition",
                        "market_gap": "Continuous specialty care pods (e.g. endocrinology, autoimmune) with high physician continuity"
                    },
                    {
                        "name": "Abridge AI",
                        "type": "Direct / Clinical AI",
                        "website": "https://www.abridge.com",
                        "offerings": "Ambient AI clinical scribe and medical conversation summarizer",
                        "pricing": "$150 - $350 / physician / month",
                        "positioning": "Ambient clinical intelligence integrated with Epic",
                        "strengths": "Top-tier accuracy, major hospital system contracts (UPMC, Emory)",
                        "weaknesses": "Requires integration with existing legacy EHRs, dependent on enterprise partnerships",
                        "market_gap": "Full end-to-end automated clinic billing and revenue cycle management combined with ambient notes"
                    },
                    {
                        "name": "Kareo (Tebra)",
                        "type": "Direct / SMB Practice",
                        "website": "https://www.tebra.com",
                        "offerings": "Clinical EHR, billing, patient engagement for independent practices",
                        "pricing": "$300 - $500 / provider / month",
                        "positioning": "All-in-one operating system for independent medical practices",
                        "strengths": "Affordable entry point for solo/small practices, integrated billing",
                        "weaknesses": "Occasional customer support bottlenecks, slow modern AI adoption",
                        "market_gap": "Autonomous patient intake and insurance prior-authorization agents"
                    }
                ]
        elif ind_key == "real_estate":
            if is_ph:
                competitors = [
                    {
                        "name": "Property24 Philippines",
                        "type": "Direct",
                        "website": "https://www.property24.com.ph",
                        "offerings": "Classified property portal, developer advertising",
                        "pricing": "₱1,500 - ₱8,000 / mo broker listing packages",
                        "positioning": "Mainstream digital property search portal",
                        "strengths": "High organic search visibility, high listing volume",
                        "weaknesses": "Outdated duplicate listings, unverified agents, low lead quality",
                        "market_gap": "Verified-only title deed listings with escrow transaction management"
                    },
                    {
                        "name": "Rentpad",
                        "type": "Direct",
                        "website": "https://rentpad.com.ph",
                        "offerings": "Long-term condo and apartment rental marketplace",
                        "pricing": "Free basic / ₱500 - ₱2,000 featured listing credits",
                        "positioning": "Dedicated rental listing hub for condo landlords and tenants",
                        "strengths": "Simple UI, dedicated to rentals, strong tenant search traffic",
                        "weaknesses": "No automated lease signing, no digital rent collection or background checks",
                        "market_gap": "End-to-end digital tenant onboarding, automated PDC/e-wallet rent collection, and maintenance tracking"
                    },
                    {
                        "name": "Lamudi Philippines",
                        "type": "Direct",
                        "website": "https://www.lamudi.com.ph",
                        "offerings": "Commercial & residential marketplace, developer lead gen",
                        "pricing": "Tiered monthly agency subscriptions (₱5,000 - ₱35,000/mo)",
                        "positioning": "Developer-aligned national property marketplace",
                        "strengths": "Strong corporate ties with top developers (Ayala, Megaworld, SMDC)",
                        "weaknesses": "Heavy developer ads degrade buyer search experience",
                        "market_gap": "Buyer-agent matching with transparent commission sharing and verified yield analytics"
                    }
                ]
            else:
                competitors = [
                    {
                        "name": "Zillow Group",
                        "type": "Direct",
                        "website": "https://www.zillow.com",
                        "offerings": "Premier Agent lead gen, Zestimate valuation, mortgage marketplace, rental leasing",
                        "pricing": "Pay-per-lead / Premier Agent flex commission split (20-35% of agent commission)",
                        "positioning": "The unchallenged consumer portal for US home search",
                        "strengths": "Massive organic consumer mindshare, accurate search algorithms, mobile dominance",
                        "weaknesses": "Agents frustrated with high lead costs, non-exclusive leads, declining lead conversion rates",
                        "market_gap": "AI agent platform that nurtures and qualifies dead buyer leads directly into agent calendars"
                    },
                    {
                        "name": "CoStar Group / Apartments.com",
                        "type": "Direct / Commercial & Multifamily",
                        "website": "https://www.costar.com",
                        "offerings": "Commercial real estate data, LoopNet marketplace, multifamily advertising",
                        "pricing": "$500 - $3,000+ / seat / month (enterprise locked contracts)",
                        "positioning": "The Bloomberg of commercial real estate data",
                        "strengths": "Comprehensive proprietary asset database, monopoly power in commercial analytics",
                        "weaknesses": "Extremely aggressive pricing, hostile contract renewal terms, legacy desktop UI",
                        "market_gap": "Open, collaborative commercial deal room and underwriting platform for mid-market brokers"
                    },
                    {
                        "name": "Buildium / AppFolio",
                        "type": "Direct / Property SaaS",
                        "website": "https://www.appfolio.com",
                        "offerings": "Multifamily and HOA property management, accounting, tenant portal",
                        "pricing": "$1.40 - $3.00 / unit / month (minimum $280 - $400/mo)",
                        "positioning": "Scale-oriented operating system for residential property managers",
                        "strengths": "Robust accounting and tenant payment automation",
                        "weaknesses": "Steep learning curve, expensive for portfolios with under 50 units",
                        "market_gap": "AI property assistant for landlords managing 5-50 doors without complex bookkeeping overhead"
                    }
                ]
        elif ind_key == "ecommerce":
            competitors = [
                {
                    "name": "Shopify",
                    "type": "Direct / Platform",
                    "website": "https://www.shopify.com",
                    "offerings": "E-commerce storefronts, Shopify Payments, Shop App, POS, app ecosystem",
                    "pricing": "$39/mo Basic, $105/mo Shopify, $399/mo Advanced + 2.4-2.9% transaction fees",
                    "positioning": "The world's leading commerce platform powering independent merchants",
                    "strengths": "Unrivaled app store ecosystem, rock-solid checkout (Shop Pay), scalable",
                    "weaknesses": "Fragmented app subscriptions increase monthly tech stack cost ($300-$800/mo for basic apps)",
                    "market_gap": "Bundled AI agent suites replacing 10+ expensive single-purpose Shopify apps"
                },
                {
                    "name": "Klaviyo",
                    "type": "Direct / Retention",
                    "website": "https://www.klaviyo.com",
                    "offerings": "Email & SMS marketing automation, customer data platform (CDP)",
                    "pricing": "Free up to 250 contacts; escalates quickly to $150 - $2,000+/mo",
                    "positioning": "Gold standard marketing automation for direct-to-consumer brands",
                    "strengths": "Granular segmentation, high deliverability, predictive lifetime value analytics",
                    "weaknesses": "Rapidly compounding price tiers, complex setup for non-technical store owners",
                    "market_gap": "Autonomous lifecycle marketer that writes, designs, tests, and deploys campaigns without human input"
                },
                {
                    "name": "Triple Whale",
                    "type": "Direct / Analytics",
                    "website": "https://www.triplewhale.com",
                    "offerings": "First-party attribution, marketing analytics dashboard, creative cockpit",
                    "pricing": "$129 - $999/mo based on tracked store revenue",
                    "positioning": "Single source of truth operating system for modern e-commerce brands",
                    "strengths": "Accurate first-party pixel attribution, creative analysis",
                    "weaknesses": "Expensive for early-stage brands (<$50k monthly revenue)",
                    "market_gap": "Affordable attribution combined with automated ad spend reallocator for emerging D2C founders"
                }
            ]
        elif ind_key == "automotive":
            competitors = [
                {
                    "name": "Samsara",
                    "type": "Direct / Fleet IoT",
                    "website": "https://www.samsara.com",
                    "offerings": "Connected Operations Cloud: fleet GPS tracking, AI dash cams, maintenance telematics",
                    "pricing": "$25 - $40 / vehicle / month + hardware costs (multi-year contract)",
                    "positioning": "Premier enterprise IoT platform for industrial fleet operations",
                    "strengths": "Superior hardware reliability, AI driver safety alerts, Fortune 500 enterprise adoption",
                    "weaknesses": "Long 3-5 year lock-in contracts, high pricing for small fleets (<15 vehicles)",
                    "market_gap": "No-contract, plug-and-play telematics with instant fuel theft and battery health alerts for SMB fleets"
                },
                {
                    "name": "Tekmetric",
                    "type": "Direct / Auto Repair SaaS",
                    "website": "https://www.tekmetric.com",
                    "offerings": "Shop management software, digital vehicle inspection (DVI), workflow tracking",
                    "pricing": "$199 - $499 / shop / month",
                    "positioning": "Cloud-based operating system for independent automotive repair shops",
                    "strengths": "Intuitive digital vehicle inspection sent directly to customer phones with photos",
                    "weaknesses": "Limited native parts inventory supplier integration in regional markets",
                    "market_gap": "Automated parts sourcing engine comparing regional distributor pricing and delivery ETA in real time"
                },
                {
                    "name": "DealerSocket / Cox Automotive",
                    "type": "Direct / Dealership CRM",
                    "website": "https://www.coxautoinc.com",
                    "offerings": "Automotive CRM, dealership inventory management, desking tools",
                    "pricing": "$1,000 - $4,500 / rooftop / month",
                    "positioning": "Comprehensive automotive dealership enterprise software",
                    "strengths": "Deep DMS integration with major auto OEMs",
                    "weaknesses": "Outdated legacy user experience, sluggish customer support, poor mobile app",
                    "market_gap": "AI conversational assistant responding to inbound car buyer inquiries in under 30 seconds"
                }
            ]
        else: # SaaS / Tech
            competitors = [
                {
                    "name": "HubSpot",
                    "type": "Direct / Marketing & CRM",
                    "website": "https://www.hubspot.com",
                    "offerings": "Inbound Marketing Hub, Sales CRM, Service Hub, CMS",
                    "pricing": "$20/seat Starter up to $3,600/mo Enterprise + mandatory onboarding fees",
                    "positioning": "The go-to CRM and inbound platform for scaling companies",
                    "strengths": "Exceptional ecosystem, clean UI, rich content academy and inbound brand",
                    "weaknesses": "Severe price escalation as contact lists grow; expensive enterprise tier gating basic permissions",
                    "market_gap": "Uncapped contact pricing with native AI research agents built directly into the CRM"
                },
                {
                    "name": "Apollo.io",
                    "type": "Direct / Prospecting & Sales",
                    "website": "https://www.apollo.io",
                    "offerings": "B2B lead database (275M+ contacts), email sequencing, AI sales assistant",
                    "pricing": "$49 - $99 / user / month",
                    "positioning": "All-in-one sales intelligence and outbound execution platform",
                    "strengths": "Unbeatable value for B2B contact credits, fast lead enrichment",
                    "weaknesses": "B2B email bounce rate averages 15-20%; shared IP deliverability challenges",
                    "market_gap": "Multi-channel intent validation with verified phone connect-rates and deep company research"
                },
                {
                    "name": "G2 / Capterra",
                    "type": "Indirect / Review Marketplace",
                    "website": "https://www.g2.com",
                    "offerings": "Software reviews, buyer intent data, vendor profile marketing",
                    "pricing": "$12,000 - $60,000+ / year for vendor buyer-intent packages",
                    "positioning": "The world's largest tech marketplace and software peer review site",
                    "strengths": "High Google search dominance for '[software] reviews'",
                    "weaknesses": "High cost for startups, allegations of review gating and pay-to-play badge placements",
                    "market_gap": "Transparent, un-monetized open benchmarking powered by objective API benchmarks and LLM code evaluations"
                }
            ]

        self.record_usage("Competitor Intelligence & Pricing Teardown", input_tokens, output_tokens)

        return {
            "competitors_count": len(competitors),
            "competitors": competitors,
            "white_space_opportunities": [
                "Unbundling overpriced all-in-one enterprise suites into affordable, modular workflows",
                "Delivering native AI autonomous execution instead of just static software forms",
                "Eliminating punitive contact and seat-based pricing models in favor of value-aligned usage"
            ]
        }
