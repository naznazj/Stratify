"""
Agent 3: Customer Intelligence Analyst
Responsibilities:
- Customer segmentation (B2B, B2C, Enterprise, SMEs, Niche)
- Ideal Customer Profile (ICP) definitions
- Buyer Persona archetypes (roles, KPIs, pain points, objections)
- Customer purchasing power estimation and budget allocation
- Buying motivations, triggers, and willingness-to-pay (WTP)
"""
from typing import Dict, Any, List
from stratify_core.agents.base_agent import BaseAgent
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand

class CustomerIntelligenceAgent(BaseAgent):
    def __init__(self, token_tracker, verification_service):
        super().__init__(
            name="customer_intel_agent",
            role_title="Customer Intelligence Analyst",
            token_tracker=token_tracker,
            verification_service=verification_service
        )

    def execute(self, command: StratifyCommand, profile: IndustryProfile, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        ind_key = profile.industry_key
        loc = profile.geographic_market
        is_ph = "philippines" in loc.lower() or "ph" in loc.lower()

        input_tokens = 920
        output_tokens = 890

        if ind_key == "healthcare":
            segments = [
                {
                    "name": "Mid-Sized Private Hospitals & Health Networks",
                    "type": "B2B Enterprise",
                    "share_of_market": "35%",
                    "purchasing_power": "High ($150,000 - $1.5M Annual IT/Ops Budget)",
                    "pain_points": [
                        "Severe nursing and administrative staff shortages",
                        "High claims rejection rates and slow health insurance reimbursements",
                        "Fragmented departmental silos between pharmacy, laboratory, and billing"
                    ],
                    "buying_motivation": "Protect operational margins, accelerate claims turnaround, improve bed turnover"
                },
                {
                    "name": "Independent Multi-Specialty Clinics & Diagnostic Centers",
                    "type": "B2B SME",
                    "share_of_market": "40%",
                    "purchasing_power": "Medium ($10,000 - $60,000 Annual IT Budget)",
                    "pain_points": [
                        "High patient no-show rates (up to 25-30%) without automated SMS reminders",
                        "Laborious paper-based medical records risking loss and non-compliance",
                        "Lack of digital marketing and search visibility to attract new local patients"
                    ],
                    "buying_motivation": "Fill empty appointment slots, eliminate paper clutter, speed up patient intake"
                },
                {
                    "name": "Chronic Care & Elderly Patients",
                    "type": "B2C / Family Caregivers",
                    "share_of_market": "25%",
                    "purchasing_power": "Variable ($800 - $4,500 Out-of-Pocket Annual Healthcare Spend)",
                    "pain_points": [
                        "Exhausting multi-hour traffic trips and hospital waiting room lines for simple routine checkups",
                        "High cost of brand-name prescription drugs",
                        "Fragmented lab records across different providers"
                    ],
                    "buying_motivation": "Fast access to trusted doctors, medication delivery, peace of mind for family members"
                }
            ]
            personas = [
                {
                    "title": "Dr. Cynthia Ramos, Medical Director & Clinic Co-Owner",
                    "demographics": "Age 48, Board Certified Internist, manages 12 associate physicians",
                    "primary_kpi": "Patient satisfaction rating (NPS), clinic utilization rate, zero regulatory audit failures",
                    "core_pain": "Spending 3 hours every evening completing delayed EHR notes and approving insurance prior-authorizations",
                    "major_objection": "'Our older physicians will refuse to learn a complicated new software interface.'",
                    "decision_authority": "Final Sign-off on Clinic Software & Medical Equipment"
                },
                {
                    "title": "Mark Gonzales, Hospital Chief Operating Officer (COO)",
                    "demographics": "Age 52, MBA in Healthcare Administration, oversees 250-bed private facility",
                    "primary_kpi": "Days in Accounts Receivable (A/R < 42 days), average patient wait time, operating margin",
                    "core_pain": "PhilHealth and private HMO claims getting delayed for 90+ days due to tiny documentation errors",
                    "major_objection": "'Does this integrate directly with our existing HL7 server without downtime?'",
                    "decision_authority": "Budget Allocation for Enterprise Systems ($250k+)"
                }
            ]

        elif ind_key == "real_estate":
            segments = [
                {
                    "name": "Top-Producing Real Estate Brokerages & Agencies",
                    "type": "B2B",
                    "share_of_market": "30%",
                    "purchasing_power": "High ($35,000 - $250,000 Annual Marketing & Tech Budget)",
                    "pain_points": [
                        "Agent turnover and lack of centralized lead nurturing infrastructure",
                        "Wasted ad spend on low-intent portal inquiries that never answer the phone",
                        "Manual, error-prone compliance and commission split tracking"
                    ],
                    "buying_motivation": "Equip top agents with speed-to-lead automation and protect brokerage market share"
                },
                {
                    "name": "Mid-Tier Property Developers",
                    "type": "B2B Enterprise",
                    "share_of_market": "25%",
                    "purchasing_power": "Very High ($200,000 - $2M Annual Marketing Budget)",
                    "pain_points": [
                        "Inventory holding costs during sluggish pre-selling phases",
                        "High customer acquisition cost per buyer unit sold",
                        "Lack of transparent digital reservation and overseas buyer escrow portals"
                    ],
                    "buying_motivation": "Rapid sell-out of presale residential towers and overseas expat/OFW investor reach"
                },
                {
                    "name": "Accredited Real Estate Investors & Landlords",
                    "type": "B2C / High-Net-Worth Individuals (HNWI)",
                    "share_of_market": "45%",
                    "purchasing_power": "High ($150,000 - $1.5M Capital Deployable per Acquisition)",
                    "pain_points": [
                        "Late rent payments, tenant disputes, and unreliable property management handoffs",
                        "Lack of reliable rental yield projections and hidden condo dues",
                        "Illiquidity and complicated title transfer bureaucracy"
                    ],
                    "buying_motivation": "Passive rental yield (6-8%+ net), capital appreciation, effortless tenant management"
                }
            ]
            personas = [
                {
                    "title": "Patricia Tan, Managing Broker / Agency Principal",
                    "demographics": "Age 44, 18 years in residential & commercial brokerage, leads 40 licensed agents",
                    "primary_kpi": "Total transaction volume (GTV), agent productivity per month, lead-to-close ratio",
                    "core_pain": "Spending $5,000/mo on portal leads, but 70% are never contacted within the first critical 15 minutes",
                    "major_objection": "'Our agents are independent contractors; I can't force them to use a system they find annoying.'",
                    "decision_authority": "Full Agency P&L and Tech Stack Owner"
                }
            ]

        elif ind_key == "ecommerce":
            segments = [
                {
                    "name": "Scaling Direct-to-Consumer (D2C) Brands ($1M - $20M ARR)",
                    "type": "B2B SME / High Growth",
                    "share_of_market": "45%",
                    "purchasing_power": "High ($4,000 - $25,000 / month tech & marketing budget)",
                    "pain_points": [
                        "Meta and Google ROAS compression post-iOS privacy tracking updates",
                        "High cart abandonment rates (72%+ on mobile)",
                        "Fragmented customer data spread across Shopify, Klaviyo, Gorgias, and Meta"
                    ],
                    "buying_motivation": "Increase customer lifetime value (LTV), lower blended CAC, automate repeat purchases"
                },
                {
                    "name": "Emerging E-commerce Merchants & Solo Founders (<$1M ARR)",
                    "type": "B2B Micro / SMB",
                    "share_of_market": "55%",
                    "purchasing_power": "Low to Moderate ($300 - $1,500 / month software spend)",
                    "pain_points": [
                        "Overwhelmed by managing creative production, ad buying, and fulfillment alone",
                        "High Shopify app stack costs eating into early margins",
                        "Inventory stockouts or over-purchasing dead stock"
                    ],
                    "buying_motivation": "All-in-one automation that replaces expensive agencies and freelance contractors"
                }
            ]
            personas = [
                {
                    "title": "Ethan Cole, Co-Founder & Head of Growth",
                    "demographics": "Age 31, Performance marketer turned D2C brand owner (Health & Wellness brand)",
                    "primary_kpi": "Contribution Margin, Blended CAC, Net 90-Day LTV:CAC ratio",
                    "core_pain": "Tired of wasting 15 hours a week manually producing UGC iterations and tweaking ad campaign bids",
                    "major_objection": "'Will this actually drive incremental sales, or is it just another vanity metrics dashboard?'",
                    "decision_authority": "Sole Decision Maker on Growth Tooling"
                }
            ]

        else: # SaaS / Tech / General
            segments = [
                {
                    "name": "Mid-Market Enterprise Teams (100 - 1,000 Employees)",
                    "type": "B2B Mid-Market",
                    "share_of_market": "40%",
                    "purchasing_power": "High ($50,000 - $350,000 Annual Software Budget)",
                    "pain_points": [
                        "Disjointed spreadsheets and legacy ERPs causing cross-departmental bottlenecks",
                        "Executive mandate to adopt AI without exposing proprietary corporate data",
                        "Lengthy employee onboarding cycles on complex tools"
                    ],
                    "buying_motivation": "Boost operational team efficiency by 30%+, prove rapid ROI within 60 days"
                },
                {
                    "name": "High-Growth Tech Startups & Modern Agencies",
                    "type": "B2B SME",
                    "share_of_market": "35%",
                    "purchasing_power": "Medium ($12,000 - $60,000 Annual SaaS Budget)",
                    "pain_points": [
                        "Lean teams forced to execute multi-role tasks without dedicated headcount",
                        "High software fatigue from juggling 15 different point solutions",
                        "Demanding instant time-to-value with zero implementation professional services"
                    ],
                    "buying_motivation": "Autonomous execution of repetitive workflows; pay-as-you-grow pricing"
                }
            ]
            personas = [
                {
                    "title": "Sarah Jenkins, VP of Revenue Operations",
                    "demographics": "Age 39, 12 years in B2B software operations, oversees CRM & sales tech stack",
                    "primary_kpi": "Sales cycle velocity, pipeline conversion rate, CAC payback period (<12 months)",
                    "core_pain": "Sales reps spend only 32% of their day actually selling; the rest is consumed by data entry and prep",
                    "major_objection": "'Our sales team will riot if they have to log into yet another standalone portal.'",
                    "decision_authority": "Primary Evaluator and Budget Recommender to CFO"
                }
            ]

        self.record_usage("Customer Segmentation & Persona Profiling", input_tokens, output_tokens)

        return {
            "segments_count": len(segments),
            "customer_segments": segments,
            "buyer_personas": personas,
            "purchasing_power_summary": "High purchasing power concentrated in Mid-Market and Enterprise operators seeking workflow margin defense."
        }
