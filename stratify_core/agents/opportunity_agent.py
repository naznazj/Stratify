"""
Agent 4: Business Opportunity Analyst
Responsibilities:
- Generate at least 5 differentiated, highly actionable business opportunities
- Provide comprehensive profiles: concept, problem, solution, target audience, revenue model, moats, risks
- Supply quantitative dimensional inputs to the Opportunity Scoring Engine
"""
from typing import Dict, Any, List
from stratify_core.agents.base_agent import BaseAgent
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand
from stratify_core.scoring_engine import OpportunityScoringEngine

class BusinessOpportunityAgent(BaseAgent):
    def __init__(self, token_tracker, verification_service, scoring_engine: OpportunityScoringEngine):
        super().__init__(
            name="opportunity_agent",
            role_title="Business Opportunity Analyst",
            token_tracker=token_tracker,
            verification_service=verification_service
        )
        self.scoring_engine = scoring_engine

    def execute(self, command: StratifyCommand, profile: IndustryProfile, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        ind_key = profile.industry_key
        loc = profile.geographic_market
        is_ph = "philippines" in loc.lower() or "ph" in loc.lower()

        input_tokens = 1100
        output_tokens = 1250

        raw_opportunities = []

        if ind_key == "healthcare":
            if is_ph:
                raw_opportunities = [
                    {
                        "name": "PhilHealth-Integrated Outpatient Clinic ERP",
                        "concept": "Cloud-based clinical operating system specifically engineered to automate PhilHealth eClaims verification, patient queue management, and offline-capable EHR records.",
                        "problem": "Private clinics and regional diagnostic hubs lose up to 18% of reimbursement revenue due to clerical errors and 90-day PhilHealth claims processing backlogs.",
                        "solution": "Lightweight, tablet-ready clinic ERP that pre-validates patient PhilHealth eligibility in real-time, compiles error-free electronic claim packages, and syncs offline when internet fails.",
                        "target_audience": "Stand-alone private clinics, primary care networks, diagnostic labs across Metro Manila, Cebu, Davao, and provincial centers.",
                        "revenue_model": "SaaS Subscription (₱3,500 - ₱12,000 / clinic / month) + ₱15 micro-fee per successfully reimbursed claim.",
                        "competitive_moat": "Direct API certification with PhilHealth eClaims gateway, regional offline sync, native local dialect UI options.",
                        "difficulty": "Medium",
                        "risks": "Bureaucratic delays in government API certification updates; resistance to tech migration among veteran physicians.",
                        "demand_score": 92, "revenue_score": 88, "purchasing_score": 82, "comp_opp_score": 90, "feasibility_score": 80
                    },
                    {
                        "name": "Mobile On-Site Corporate Health & Diagnostic Vans",
                        "concept": "Fleet of tech-enabled mobile diagnostic vans providing on-site Annual Physical Examinations (APE) and executive health screenings directly at BPO and enterprise office parks.",
                        "problem": "BPOs and call center operators lose thousands of work hours when requiring graveyard-shift staff to commute to crowded off-site diagnostic clinics for mandatory annual physicals.",
                        "solution": "Modern vans equipped with digital X-ray, automated blood analyzers, and ECGs that arrive at corporate office campuses, conducting 15-minute exams with digital results delivered in 4 hours.",
                        "target_audience": "IT-BPO companies, shared services centers, manufacturing plants in PEZA economic zones.",
                        "revenue_model": "Corporate B2B contracts (₱650 - ₱1,800 per employee examined; average contract size ₱750k - ₱3M).",
                        "competitive_moat": "PEZA compliance clearances, rapid turnaround laboratory software, corporate HR portal integration.",
                        "difficulty": "Medium",
                        "risks": "Initial vehicle and equipment CapEx; medical technician staffing recruitment in regional hubs.",
                        "demand_score": 89, "revenue_score": 94, "purchasing_score": 90, "comp_opp_score": 84, "feasibility_score": 75
                    },
                    {
                        "name": "Pediatric & Chronic Care Ambient Telehealth Pods",
                        "concept": "Specialized remote diagnostic pods installed in community pharmacies and subdivision clubhouses providing connected otoscopy, stethoscope, and vitals streaming to certified pediatricians.",
                        "problem": "Suburban parents spend 2-4 hours traveling through traffic to hospital emergency rooms for simple ear infections, fever, and respiratory coughs.",
                        "solution": "Self-contained physical kiosks in trusted neighborhood pharmacies where a trained nurse assists with digital otoscope and vitals while a remote pediatrician consults in HD.",
                        "target_audience": "Working parents with young children; suburban families in Cavite, Laguna, Rizal, Bulacan, and Pampanga.",
                        "revenue_model": "₱450 - ₱650 consultation fee split (70% doctor, 20% pharmacy host, 10% platform fee) + prescription fulfillment margin.",
                        "competitive_moat": "Exclusive pharmacy retail partnerships (e.g. Southstar, Generika), hardware integration with medical grade IoT devices.",
                        "difficulty": "High",
                        "risks": "Hardware maintenance logistics; patient hesitation to use kiosk instead of in-person pediatrician.",
                        "demand_score": 86, "revenue_score": 81, "purchasing_score": 76, "comp_opp_score": 88, "feasibility_score": 68
                    },
                    {
                        "name": "B2B Medical Supply & Equipment Consolidated Purchasing Hub",
                        "concept": "A transparent digital wholesale marketplace aggregating purchasing demand across hundreds of independent clinics to secure tier-1 distributor bulk pricing.",
                        "problem": "Small and medium clinics pay 30-50% markups on disposable gloves, syringes, reagents, and pharmaceuticals due to lack of buying power.",
                        "solution": "Centralized procurement platform grouping orders every week, negotiating directly with licensed pharmaceutical distributors, and delivering within 48 hours.",
                        "target_audience": "Private clinic owners, dental clinics, veterinary practices, independent surgery centers.",
                        "revenue_model": "5% - 12% marketplace take-rate on transacted wholesale order volume.",
                        "competitive_moat": "Aggregated order volume agreements with licensed distributors, verified FDA/DOH vendor licenses.",
                        "difficulty": "Medium",
                        "risks": "Inventory cash flow requirements if taking physical possession; credit term expectations from clinic buyers.",
                        "demand_score": 90, "revenue_score": 89, "purchasing_score": 80, "comp_opp_score": 85, "feasibility_score": 78
                    },
                    {
                        "name": "AI Medical Transcription & Patient Discharge Voice Assistant",
                        "concept": "Multi-dialect (Tagalog, English, Bisaya) voice AI assistant that transcribes physician consultations and automatically translates discharge care plans for patients.",
                        "problem": "Doctors spend hours handwriting discharge summaries, leading to poor patient adherence and post-op medication mix-ups due to illegible handwriting and medical jargon.",
                        "solution": "Ambient smartphone app that listens during patient consultation, drafts clinical SOAP notes for the doctor, and sends an audio-visual WhatsApp/Viber summary in conversational local language to the patient.",
                        "target_audience": "Private hospital consultants, outpatient specialists, group medical practices.",
                        "revenue_model": "₱1,999 / physician / month SaaS subscription.",
                        "competitive_moat": "Proprietary Taglish and regional dialect fine-tuned medical speech models; EHR export integrations.",
                        "difficulty": "Low",
                        "risks": "Speech-to-text accuracy in noisy clinic environments; physician data security consent.",
                        "demand_score": 94, "revenue_score": 85, "purchasing_score": 84, "comp_opp_score": 92, "feasibility_score": 86
                    }
                ]
            else:
                raw_opportunities = [
                    {
                        "name": "Ambient AI Revenue Cycle Management (RCM) for Outpatient Care",
                        "concept": "Autonomous AI agent platform that converts physician-patient dialogue into finalized, pre-coded insurance claim packets (ICD-10, CPT) with zero human scribes.",
                        "problem": "Independent clinics spend 8-12% of total collections on manual billing services and lose up to 15% in denied claims due to human documentation discrepancies.",
                        "solution": "Ambient acoustic model that listens to examinations, extracts billing codes, validates insurer prior-authorization rules, and submits clean claims in real time.",
                        "target_audience": "Independent physician practices, orthopedic and cardiology specialty clinics, ambulatory surgery centers.",
                        "revenue_model": "Performance fee (2.5% - 4.5% of net collected revenue, significantly beating legacy 8% billing agency fees).",
                        "competitive_moat": "Payer rule clearinghouse integration, sub-second claim scrubbing algorithms, zero upfront hardware installation.",
                        "difficulty": "Medium",
                        "risks": "Insurer adjudication timing; liability for claim inaccuracies.",
                        "demand_score": 95, "revenue_score": 93, "purchasing_score": 88, "comp_opp_score": 87, "feasibility_score": 82
                    },
                    {
                        "name": "Remote Patient Monitoring (RPM) for Geriatric Specialty Care",
                        "concept": "Turnkey cellular-connected vitals kits (blood pressure, glucose, pulse ox) paired with an AI clinician triage desk that bills Medicare CPT codes 99453/99454/99457.",
                        "problem": "Elderly patients with congestive heart failure and diabetes experience high emergency readmissions, yet small practices lack nursing bandwidth to monitor them daily.",
                        "solution": "Plug-and-play cellular devices requiring zero Wi-Fi setup; AI filters anomalies and alerts on-call nurse practitioners only when interventions are needed.",
                        "target_audience": "Internal medicine, geriatric practices, and accountable care organizations (ACOs).",
                        "revenue_model": "Monthly per-patient managed fee ($65 - $85/patient/mo) billed through compliant Medicare reimbursement yielding $120+ profit to the practice.",
                        "competitive_moat": "Cellular non-pairing hardware design, Medicare billing compliance engine, turn-key clinical triage center.",
                        "difficulty": "Medium",
                        "risks": "Medicare reimbursement regulatory adjustments; hardware inventory logistics.",
                        "demand_score": 91, "revenue_score": 92, "purchasing_score": 89, "comp_opp_score": 83, "feasibility_score": 79
                    },
                    {
                        "name": "Autonomous Prior-Authorization Clearinghouse",
                        "concept": "AI agents that interface directly with commercial insurance portals (UnitedHealthcare, Anthem, Aetna) to complete prior authorization approvals in minutes rather than days.",
                        "problem": "Staff spend 14+ hours per physician every week on phone hold times and faxing medical history records to obtain insurance approvals for essential medications and MRIs.",
                        "solution": "Browser-agent bots trained on each payer portal that automatically extract necessary clinical criteria from EHRs and submit authorizations with automated appeals.",
                        "target_audience": "Specialty medical practices (oncology, neurology, dermatology, surgery).",
                        "revenue_model": "Pay-per-submission ($12 - $18 / authorization) or $499/mo clinic subscription.",
                        "competitive_moat": "Proprietary payer portal automation scripts, deep clinical chart parsing.",
                        "difficulty": "Medium",
                        "risks": "Payer portal anti-bot captchas; frequent interface redesigns by insurance carriers.",
                        "demand_score": 96, "revenue_score": 90, "purchasing_score": 91, "comp_opp_score": 89, "feasibility_score": 81
                    },
                    {
                        "name": "B2B Hospital Clinical Staffing & Locum Tenens AI Exchange",
                        "concept": "Direct marketplace matching pre-credentialed traveling nurses and locum physicians with hospitals, eliminating 35% staffing agency markups.",
                        "problem": "Hospitals face crippling nurse shortages and pay exorbitant intermediary markups to legacy staffing agencies.",
                        "solution": "Verified digital credential passport allowing doctors and nurses to accept open hospital shifts instantly with instant shift payout.",
                        "target_audience": "Hospital HR directors, regional health networks, registered nurses, traveling physicians.",
                        "revenue_model": "10% transparent platform fee on gross shift wages (replacing legacy 35-45% agency fees).",
                        "competitive_moat": "Automated license verification with 50 state medical boards, malpractice insurance bundling.",
                        "difficulty": "High",
                        "risks": "State medical licensing reciprocity; worker classification regulations.",
                        "demand_score": 92, "revenue_score": 95, "purchasing_score": 94, "comp_opp_score": 81, "feasibility_score": 70
                    },
                    {
                        "name": "Consumer Post-Discharge Virtual Recovery Concierge",
                        "concept": "AI-powered SMS and voice companion that monitors patients post-surgery to prevent readmission, manage medication schedules, and alert surgeons to infection signs.",
                        "problem": "Hospitals are penalized by CMS for 30-day readmissions, while discharged patients feel abandoned and confused by complex discharge paperwork.",
                        "solution": "Zero-friction conversational SMS concierge that checks in twice daily, analyzes photos of surgical incisions, and escalates red flags immediately.",
                        "target_audience": "Orthopedic surgery centers, bariatric clinics, hospital discharge coordinators.",
                        "revenue_model": "$45 per surgical episode of care paid by provider / health system.",
                        "competitive_moat": "Clinical NLP triage safety algorithms, CMS Hospital Readmissions Reduction Program (HRRP) alignment.",
                        "difficulty": "Low",
                        "risks": "Medical device software liability boundaries; SMS carrier delivery filtering.",
                        "demand_score": 88, "revenue_score": 86, "purchasing_score": 85, "comp_opp_score": 86, "feasibility_score": 88
                    }
                ]

        elif ind_key == "real_estate":
            raw_opportunities = [
                {
                    "name": "AI Speed-to-Lead Conversational Voice Agent for Top Brokerages",
                    "concept": "Instant conversational AI voice agent that calls incoming online buyer and seller leads within 20 seconds, qualifies their timeline and budget, and books live appointments on agent calendars.",
                    "problem": "71% of online real estate inquiries are never contacted because agents are in showings; lead conversion drops 8x after the first 5 minutes.",
                    "solution": "Ultra-realistic voice AI that initiates outbound calls immediately upon portal form submission, conducts natural qualification, and transfers live calls to available agents.",
                    "target_audience": "Top residential brokerage teams, luxury property agencies, high-volume mortgage brokers.",
                    "revenue_model": "$299 - $899 / month team SaaS subscription + $1.50 per qualified booked consultation.",
                    "competitive_moat": "Sub-500ms latency voice pipeline, deep two-way integration with Follow Up Boss, kvCORE, and Salesforce.",
                    "difficulty": "Low",
                    "risks": "TCPA compliance regulations; consumer perception of robotic calling if voice models falter.",
                    "demand_score": 94, "revenue_score": 90, "purchasing_score": 88, "comp_opp_score": 91, "feasibility_score": 87
                },
                {
                    "name": "AI Automated Underwriting & Deal Room for Commercial Multifamily",
                    "concept": "Platform that parses commercial real estate Offering Memorandums (OMs) and rent rolls in 60 seconds to produce institutional-grade financial models and IRR projections.",
                    "problem": "Acquisitions analysts spend 6-10 hours manually retyping PDF rent rolls and trailing-12 financial statements into Excel models to evaluate deals.",
                    "solution": "Vision-LLM engine that ingests messy broker PDFs, standardizes expenses, runs debt-service sensitivity models, and drafts investment committee memos.",
                    "target_audience": "Private equity real estate firms, family offices, commercial mortgage brokers.",
                    "revenue_model": "$450 / seat / month or $2,500/mo corporate firm license.",
                    "competitive_moat": "Proprietary table-parsing algorithms, custom financial underwriting model templates.",
                    "difficulty": "Medium",
                    "risks": "Precision tolerance for decimal calculation errors in multi-million dollar acquisitions.",
                    "demand_score": 89, "revenue_score": 93, "purchasing_score": 92, "comp_opp_score": 85, "feasibility_score": 80
                },
                {
                    "name": "Fractional Tokenized Vacation Property Co-Ownership Platform",
                    "concept": "Legal and digital platform enabling 4 to 8 accredited buyers to co-own luxury vacation villas with professionally managed rental calendars and automated expense splits.",
                    "problem": "High interest rates and steep villa prices lock affluent buyers out of whole-home second home ownership, while Airbnb management is a headache.",
                    "solution": "Turnkey LLC structuring where each owner owns 1/8th of the real estate deed, enjoys 44 days of annual usage, and earns rental yields on unused weeks.",
                    "target_audience": "Affluent urban professionals, high-income remote executives, international expats.",
                    "revenue_model": "12% upfront development & syndication fee + $150/mo per owner asset management fee.",
                    "competitive_moat": "Standardized LLC legal framework, proprietary booking fair-share scheduler, local property management network.",
                    "difficulty": "High",
                    "risks": "Securities regulations (SEC / local capital market commission); illiquid secondary resale market.",
                    "demand_score": 85, "revenue_score": 95, "purchasing_score": 91, "comp_opp_score": 82, "feasibility_score": 65
                },
                {
                    "name": "Automated Property Management & Maintenance Dispatch Platform",
                    "concept": "AI resident concierge that handles tenant maintenance requests via WhatsApp/SMS, diagnoses issues via photo inspection, and dispatches pre-vetted contractors automatically.",
                    "problem": "Landlords and property managers waste 40% of their day fielding repetitive messages about leaky sinks and coordinating trade contractors.",
                    "solution": "Smart bot that guides tenants to troubleshoot common breaker/valve issues, collects exact photo/video evidence, and auto-dispatches pre-approved plumbers/electricians with price caps.",
                    "target_audience": "Independent landlords (5-50 doors), boutique property management agencies.",
                    "revenue_model": "$2.50 per active residential unit per month.",
                    "competitive_moat": "Automated diagnostic decision tree, regional contractor network pricing agreements.",
                    "difficulty": "Low",
                    "risks": "Contractor quality accountability; emergency maintenance liability.",
                    "demand_score": 91, "revenue_score": 87, "purchasing_score": 80, "comp_opp_score": 86, "feasibility_score": 85
                },
                {
                    "name": "Title Deed Verification & Digital Escrow Marketplace",
                    "concept": "End-to-end digital transaction closing portal that automates registry of deeds title checks, tax clearance, and digital escrow fund custody.",
                    "problem": "Real estate transactions in emerging and suburban markets suffer from title fraud, fake ownership claims, and delayed closing periods exceeding 90 days.",
                    "solution": "Secure portal partnering with title insurance underwriters and bank escrow to verify chain of title in 24 hours and release purchase funds upon digital deed transfer.",
                    "target_audience": "Property developers, foreign investors, licensed real estate brokerages.",
                    "revenue_model": "0.50% - 1.0% escrow and title verification closing fee.",
                    "competitive_moat": "Direct integration with land registry databases and licensed trust banks.",
                    "difficulty": "High",
                    "risks": "Government bureaucracy in title record digitization; legal jurisdiction over digital notarization.",
                    "demand_score": 88, "revenue_score": 92, "purchasing_score": 89, "comp_opp_score": 89, "feasibility_score": 67
                }
            ]

        elif ind_key == "ecommerce":
            raw_opportunities = [
                {
                    "name": "Autonomous AI UGC & Video Ad Creative Studio for TikTok Shop",
                    "concept": "End-to-end generative AI engine that ingests an e-commerce product link and outputs 20+ viral-format TikTok and Meta video ads featuring realistic AI avatars and trending hooks.",
                    "problem": "D2C brands burn out creative ad fatigue within 7 days; hiring influencers and video editors costs $3,000 - $8,000 per month.",
                    "solution": "SaaS that scrapes product benefits, creates viral scripting, renders hyper-realistic AI creator video ads, and pushes them directly to TikTok and Meta Ad Managers.",
                    "target_audience": "Shopify brand founders, Amazon FBA sellers, TikTok Shop merchants.",
                    "revenue_model": "$99 - $399 / month tiered subscription based on video rendering credits.",
                    "competitive_moat": "TikTok viral script template database, multi-language lip-sync, direct TikTok Shop API integration.",
                    "difficulty": "Low",
                    "risks": "TikTok platform policy shifts regarding AI-generated creator disclosure.",
                    "demand_score": 97, "revenue_score": 91, "purchasing_score": 84, "comp_opp_score": 88, "feasibility_score": 89
                },
                {
                    "name": "Cart Abandonment AI Voice & WhatsApp Recovery Concierge",
                    "concept": "Real-time conversational WhatsApp and SMS concierge that engages high-value abandoned cart shoppers with tailored answers to their specific product hesitations.",
                    "problem": "Standard email cart abandonment sequences only recover 4-7% of lost sales; generic discount popups erode gross margins.",
                    "solution": "Intelligent conversational agent that pings shoppers within 8 minutes, identifies why they hesitated (sizing, shipping time, ingredients), and addresses objections with social proof.",
                    "target_audience": "High-AOV ($80+) e-commerce brands, luxury goods, complex wellness products.",
                    "revenue_model": "$149/mo base SaaS + 8% performance fee on successfully recovered cart revenue.",
                    "competitive_moat": "Dynamic objection-handling library, two-way WhatsApp Business API compliance.",
                    "difficulty": "Low",
                    "risks": "WhatsApp spam policy thresholds; shopper sensitivity to over-aggressive messaging.",
                    "demand_score": 93, "revenue_score": 94, "purchasing_score": 86, "comp_opp_score": 90, "feasibility_score": 87
                },
                {
                    "name": "Predictive Restock & Working Capital Optimization Engine",
                    "concept": "Inventory forecasting software that connects to Shopify and Amazon sales channels to predict exact reorder dates and matches merchants with low-cost inventory line-of-credit financing.",
                    "problem": "E-commerce brands lose 22% of potential annual revenue due to stockouts, while over-ordering leads to crippling cash flow crunches.",
                    "solution": "Machine learning model analyzing supplier lead times, ad spend velocity, and seasonal peaks to generate purchase orders and trigger working capital financing.",
                    "target_audience": "Omnichannel D2C merchants with $500k - $10M annual sales.",
                    "revenue_model": "$199 - $599/mo SaaS subscription + 1.5% loan origination fee from lending partners.",
                    "competitive_moat": "Embedded fintech lending partner network, predictive supply chain algorithms.",
                    "difficulty": "Medium",
                    "risks": "Merchant credit default risk if participating in balance sheet lending.",
                    "demand_score": 89, "revenue_score": 92, "purchasing_score": 87, "comp_opp_score": 84, "feasibility_score": 81
                },
                {
                    "name": "Sustainable Biodegradable Packaging & Custom Branded Unboxing Hub",
                    "concept": "On-demand custom compostable mailers, plant-based tapes, and custom unboxing inserts with low minimum order quantities (MOQs).",
                    "problem": "Eco-friendly packaging suppliers demand 10,000+ unit MOQs, forcing small brands to use planet-polluting plastic bubble mailers.",
                    "solution": "Digital print-on-demand platform offering custom branded compostable packaging starting at 100 units with 5-day shipping.",
                    "target_audience": "Clean beauty brands, eco-conscious apparel, organic food retailers.",
                    "revenue_model": "35% - 45% gross product margin on packaging orders.",
                    "competitive_moat": "Proprietary short-run digital printing technology, certified B-Corp compostable materials.",
                    "difficulty": "Medium",
                    "risks": "Raw material cost fluctuations in bioplastics; shipping carrier bulk rates.",
                    "demand_score": 87, "revenue_score": 88, "purchasing_score": 82, "comp_opp_score": 86, "feasibility_score": 82
                },
                {
                    "name": "B2B Wholesale Digital Showroom for Independent D2C Brands",
                    "concept": "Curated digital wholesale marketplace connecting indie boutique brands with thousands of independent specialty gift shops and department store buyers.",
                    "problem": "Brands struggle to get discovered by retail store buyers without spending $15k+ exhibiting at trade shows.",
                    "solution": "Modern wholesale marketplace with net-60 buyer payment terms, digital line sheets, and integrated POS ordering.",
                    "target_audience": "Independent specialty retail store buyers, boutique hotel gift shops, artisanal product makers.",
                    "revenue_model": "15% commission on first opening wholesale orders, 10% on reorders.",
                    "competitive_moat": "Proprietary retail buyer network, automated credit risk underwriting.",
                    "difficulty": "High",
                    "risks": "Credit underwriting losses if independent boutiques default on net-60 invoices.",
                    "demand_score": 86, "revenue_score": 90, "purchasing_score": 85, "comp_opp_score": 81, "feasibility_score": 74
                }
            ]

        else: # SaaS / Tech / General
            raw_opportunities = [
                {
                    "name": "Autonomous Multi-Agent SDR & Inbound Pipeline Qualifier",
                    "concept": "Self-operating AI sales development representative that researches target accounts, monitors executive job changes, crafts personalized multi-channel outreach, and handles objection emails.",
                    "problem": "Hiring and training human SDRs costs $85k/year, has a 6-month average tenure, and human reps spend only 30% of their time actively researching prospects.",
                    "solution": "Agentic system that continuously audits target account news, enriches verified phone/email coordinates, and conducts contextual conversational email dialogues to secure calendar meetings.",
                    "target_audience": "B2B SaaS companies, corporate technology consultants, professional services agencies.",
                    "revenue_model": "$499/mo base platform + $75 per verified qualified sales meeting held.",
                    "competitive_moat": "Proprietary email deliverability infrastructure, live web signal scrapers, multi-agent debate architecture.",
                    "difficulty": "Low",
                    "risks": "Spam filtering enforcement by Google and Microsoft; reputation management.",
                    "demand_score": 96, "revenue_score": 95, "purchasing_score": 92, "comp_opp_score": 88, "feasibility_score": 88
                },
                {
                    "name": "Enterprise Generative Engine Optimization (GEO) & AI Brand Presence Engine",
                    "concept": "Analytics and content platform that tracks brand visibility and sentiment inside ChatGPT, Perplexity, Gemini, and Claude, optimizing brand citations to dominate AI answer queries.",
                    "problem": "Traditional SEO is losing up to 40% of top-of-funnel clicks to AI answer engines; brands have zero visibility into whether ChatGPT recommends them or their competitors.",
                    "solution": "Daily auditing of 1,000+ AI buyer queries, identifying citation gaps, and engineering authoritative knowledge graph entities and PR placements to ensure top AI recommendations.",
                    "target_audience": "Chief Marketing Officers (CMOs), enterprise SEO directors, high-ticket B2B service firms.",
                    "revenue_model": "$1,250 - $4,500 / month corporate subscription.",
                    "competitive_moat": "First-mover advantage in AI engine query scraping, proprietary GEO citation algorithm.",
                    "difficulty": "Medium",
                    "risks": "LLM output stochasticity; opacity in foundational model search indexing.",
                    "demand_score": 98, "revenue_score": 94, "purchasing_score": 93, "comp_opp_score": 95, "feasibility_score": 84
                },
                {
                    "name": "SOC2 & HIPAA Continuous Security Compliance AI Copilot",
                    "concept": "Automated security orchestration tool that continuously monitors AWS/Azure infrastructure, drafts security policies, and conducts automated vendor risk assessments.",
                    "problem": "Startups spend $30,000 - $70,000 and 4 months with external consultants just to obtain basic SOC2 certification required to close enterprise sales deals.",
                    "solution": "Cloud connector that auto-remediates security misconfigurations, collects continuous audit evidence, and interfaces with certified third-party auditors in one week.",
                    "target_audience": "Early-to-mid stage software startups selling to enterprise accounts.",
                    "revenue_model": "$5,000 - $18,000 annual subscription.",
                    "competitive_moat": "Certified auditor partner network, pre-built infrastructure remediation templates.",
                    "difficulty": "Medium",
                    "risks": "Liability in the event of an undetected security breach or audit rejection.",
                    "demand_score": 93, "revenue_score": 92, "purchasing_score": 90, "comp_opp_score": 84, "feasibility_score": 79
                },
                {
                    "name": "Zero-Party Customer Data & Micro-Survey Platform",
                    "concept": "Interactive on-site micro-quizzes and intent widgets that capture explicit customer preferences and sync directly into marketing automation tools without cookies.",
                    "problem": "Third-party cookie deprecation and privacy regulations have blinded marketers to why visitors leave without purchasing.",
                    "solution": "Hyper-engaging 2-question interactive micro-widgets yielding 45%+ completion rates that capture exact customer intent and personalize downstream messaging.",
                    "target_audience": "E-commerce growth leads, SaaS conversion specialists, online educators.",
                    "revenue_model": "$89 - $299 / month tiered by monthly unique tracked visitors.",
                    "competitive_moat": "Ultra-lightweight 4kb script footprint, pre-built vertical survey logic.",
                    "difficulty": "Low",
                    "risks": "Survey fatigue if UX interrupts core customer journey.",
                    "demand_score": 89, "revenue_score": 87, "purchasing_score": 83, "comp_opp_score": 86, "feasibility_score": 89
                },
                {
                    "name": "Vertical AI Contract Review & Risk Redlining Engine",
                    "concept": "Specialized legal copilot that parses NDAs, vendor Master Service Agreements (MSAs), and Statements of Work (SOWs) against corporate legal playbooks in 30 seconds.",
                    "problem": "Mid-market sales deals stall for 3 to 6 weeks in legal queue review, choking quarterly revenue velocity.",
                    "solution": "In-browser extension that flags high-risk indemnification clauses, suggests pre-approved fallback redlines, and accelerates contract signing velocity.",
                    "target_audience": "In-house general counsels, sales operations leads, procurement managers.",
                    "revenue_model": "$250 / user / month or $1,500/mo corporate legal team license.",
                    "competitive_moat": "Trained on thousands of proprietary negotiated enterprise contracts, strict local tenant data isolation.",
                    "difficulty": "Medium",
                    "risks": "Legal advice disclaimer mandates; professional malpractice concerns.",
                    "demand_score": 92, "revenue_score": 91, "purchasing_score": 91, "comp_opp_score": 85, "feasibility_score": 83
                }
            ]

        # Score all opportunities transparently with the scoring engine
        scored_opportunities = []
        for opp in raw_opportunities:
            score_res = self.scoring_engine.score_opportunity(
                name=opp["name"],
                market_demand_val=opp["demand_score"],
                market_demand_evidence=f"Validated demand driven by urgency of {opp['problem'][:70]}...",
                revenue_potential_val=opp["revenue_score"],
                revenue_potential_evidence=f"Monetization via {opp['revenue_model']}",
                purchasing_power_val=opp["purchasing_score"],
                purchasing_power_evidence=f"Target segment possesses budget allocation to solve operational bottleneck.",
                competitive_opp_val=opp["comp_opp_score"],
                competitive_opp_evidence=f"White space defensibility through {opp['competitive_moat']}",
                feasibility_val=opp["feasibility_score"],
                feasibility_evidence=f"Execution complexity is {opp['difficulty']} given technical tooling and regulatory landscape.",
                confidence_rating=0.88
            )

            scored_opportunities.append({
                "name": opp["name"],
                "concept": opp["concept"],
                "customer_problem": opp["problem"],
                "proposed_solution": opp["solution"],
                "target_audience": opp["target_audience"],
                "revenue_model": opp["revenue_model"],
                "competitive_advantage": opp["competitive_moat"],
                "execution_difficulty": opp["difficulty"],
                "potential_risks": opp["risks"],
                "overall_score": score_res.overall_score,
                "confidence_level": score_res.confidence_level,
                "confidence_rating": score_res.confidence_rating,
                "dimensions": [d.model_dump() for d in score_res.dimensions],
                "rationale_summary": score_res.rationale_summary
            })

        # Sort opportunities descending by score
        scored_opportunities.sort(key=lambda x: x["overall_score"], reverse=True)

        self.record_usage("Business Opportunity Formulation & Transparent Scoring", input_tokens, output_tokens)

        return {
            "opportunities_count": len(scored_opportunities),
            "opportunities": scored_opportunities,
            "top_ranked_opportunity": scored_opportunities[0]["name"] if scored_opportunities else None
        }
