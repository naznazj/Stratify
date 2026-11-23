"""
Agent 5: Marketing Strategist
Responsibilities:
- Market positioning & core differentiation narrative
- Tailored marketing channel selection with explicit business rationale
- High-intent SEO and Generative Engine Optimization (GEO) keyword strategy
- Multi-stage customer acquisition funnel (TOFU, MOFU, BOFU)
- High-impact campaign concepts & copy frameworks
- Recommended marketing budget allocation
"""
from typing import Dict, Any, List
from stratify_core.agents.base_agent import BaseAgent
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand

class MarketingStrategistAgent(BaseAgent):
    def __init__(self, token_tracker, verification_service):
        super().__init__(
            name="marketing_agent",
            role_title="Marketing Strategist",
            token_tracker=token_tracker,
            verification_service=verification_service
        )

    def execute(self, command: StratifyCommand, profile: IndustryProfile, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        ind_key = profile.industry_key
        loc = profile.geographic_market

        input_tokens = 940
        output_tokens = 970

        if ind_key == "healthcare":
            positioning = "The Regulatory-Compliant, Physician-First Clinical Operating Infrastructure"
            channels = [
                {
                    "channel": "LinkedIn Account-Based Marketing (ABM)",
                    "priority": "Primary (35% Budget)",
                    "rationale": "Hospital C-suite (CMOs, CIOs, COOs) and medical directors are actively accessible on LinkedIn. Direct InMail and sponsored thought-leadership whitepapers build institutional credibility."
                },
                {
                    "channel": "Medical Association Conferences & Industry Roundtables",
                    "priority": "Primary (30% Budget)",
                    "rationale": "Healthcare procurement relies heavily on trust, peer recommendations, and clinical society endorsements (e.g. PMA, HIMSS, Hospital Association conferences)."
                },
                {
                    "channel": "GEO & High-Intent Search (Google + AI Search)",
                    "priority": "Secondary (20% Budget)",
                    "rationale": "Target physicians and clinic managers actively searching for 'PhilHealth eClaims software', 'clinic EHR with billing', and AI clinical documentation."
                },
                {
                    "channel": "Peer Referral Programs & Clinical Advisory Boards",
                    "priority": "Supporting (15% Budget)",
                    "rationale": "Offering revenue-sharing or free tier upgrades to prominent physician influencers who champion the software across their specialist networks."
                }
            ]
            keywords = [
                {"keyword": "philhealth accredited clinic ehr system", "intent": "Transactional / High Purchase", "volume": "High Local", "priority": "Tier 1"},
                {"keyword": "automated clinical documentation ambient scribe", "intent": "Commercial Investigation", "volume": "Medium High", "priority": "Tier 1"},
                {"keyword": "hospital revenue cycle management automation", "intent": "Commercial / B2B Enterprise", "volume": "Medium", "priority": "Tier 1"},
                {"keyword": "how to reduce clinic no show appointments", "intent": "Informational / TOFU Lead Magnet", "volume": "High", "priority": "Tier 2"}
            ]
            funnel = {
                "tofu": "State of Outpatient Healthcare & Claims Reimbursement Benchmark Report",
                "mofu": "Interactive Clinic Revenue Leakage Calculator & 15-Minute Live Product Teardown",
                "bofu": "30-Day Risk-Free Clinical Pilot with Dedicated Claims Onboarding Specialist"
            }
            campaign = {
                "name": "'Zero Denied Claims' 30-Day Hospital Challenge",
                "core_message": "Stop donating 12% of your hard-earned collections to claims paperwork errors.",
                "hook": "We guarantee a 99.2% clean-claim submission rate within 30 days, or we cover the difference."
            }

        elif ind_key == "real_estate":
            positioning = "The Ultra-Responsive Transaction Acceleration Engine for Real Estate Leaders"
            channels = [
                {
                    "channel": "Meta & Instagram Targeted Lead Generation",
                    "priority": "Primary (40% Budget)",
                    "rationale": "Real estate is intensely visual and lifestyle driven. Hyper-targeted Meta ads using carousel tours and instant lead forms capture active homebuyers and investors."
                },
                {
                    "channel": "Google Search Ads & Local SEO (Google Business Profile)",
                    "priority": "Primary (30% Budget)",
                    "rationale": "Captures high-intent searches from motivated buyers typing '[City] condos for sale' or '[Neighborhood] commercial properties for lease'."
                },
                {
                    "channel": "YouTube Video Property Tours & Neighborhood Guides",
                    "priority": "Secondary (20% Budget)",
                    "rationale": "High production 4K walkthroughs build immense organic search authority and reach overseas expat investors who cannot visit in person."
                },
                {
                    "channel": "WhatsApp / SMS Automated Nurture Sequences",
                    "priority": "Supporting (10% Budget)",
                    "rationale": "Maintains instant speed-to-lead and weekly curated inventory drops directly into the buyer's messaging inbox."
                }
            ]
            keywords = [
                {"keyword": "pre selling condo metro manila investment yield", "intent": "Transactional / High Value", "volume": "High Local", "priority": "Tier 1"},
                {"keyword": "speed to lead voice assistant real estate broker", "intent": "Commercial B2B", "volume": "Medium", "priority": "Tier 1"},
                {"keyword": "commercial multifamily underwriting software", "intent": "Transactional / FinTech", "volume": "Niche High-Intent", "priority": "Tier 1"},
                {"keyword": "best rental yield properties philippines 2025", "intent": "Commercial Research", "volume": "High", "priority": "Tier 2"}
            ]
            funnel = {
                "tofu": "Annual Real Estate Investment & Capital Growth Outlook PDF",
                "mofu": "Exclusive Virtual Property Showcase & Financial Yield Breakdown Webinar",
                "bofu": "Private 1-on-1 VIP Buyer Tour with Guaranteed Developer Pricing Incentives"
            }
            campaign = {
                "name": "'Never Miss a Million-Dollar Buyer' Speed-to-Lead Initiative",
                "core_message": "Your next commission check is slipping away because your competitors answer the phone 10 minutes faster.",
                "hook": "Connect with 100% of your incoming buyer inquiries within 25 seconds—automatically."
            }

        elif ind_key == "ecommerce":
            positioning = "Autonomous Retention & Conversion Acceleration for Scaled D2C Brands"
            channels = [
                {
                    "channel": "TikTok Shop & Creator Affiliate Engine",
                    "priority": "Primary (40% Budget)",
                    "rationale": "TikTok is the highest converting impulse-purchase engine on earth. In-feed shopping videos with native checkout generate explosive revenue."
                },
                {
                    "channel": "Meta Advantage+ Shopping Campaigns (ASC)",
                    "priority": "Primary (35% Budget)",
                    "rationale": "Machine learning driven broad audience prospecting on Instagram and Facebook remains the most scalable paid customer acquisition channel."
                },
                {
                    "channel": "Klaviyo Automated Retention & SMS Flows",
                    "priority": "Secondary (15% Budget)",
                    "rationale": "Automated welcome flows, browse abandonment, and VIP post-purchase loyalty programs generate 30%+ of total store revenue at near-zero marginal cost."
                },
                {
                    "channel": "Google Shopping (Performance Max)",
                    "priority": "Supporting (10% Budget)",
                    "rationale": "Captures high-intent branded search queries and users comparing product specs."
                }
            ]
            keywords = [
                {"keyword": "best eco friendly sustainable packaging small business", "intent": "Commercial / Transactional", "volume": "High", "priority": "Tier 1"},
                {"keyword": "ai ugc video ad generator tiktok shop", "intent": "High Intent Tooling", "volume": "Fast Growing", "priority": "Tier 1"},
                {"keyword": "how to recover abandoned carts without discounts", "intent": "Informational / Problem Aware", "volume": "High", "priority": "Tier 2"}
            ]
            funnel = {
                "tofu": "Viral TikTok UGC Problem-Aware Hook Video",
                "mofu": "Interactive 60-Second Skin/Style/Product Diagnostic Quiz with Instant Personalized Recommendation",
                "bofu": "Limited-Time Bundle Offer with 100% Money-Back Guarantee & Free Express Delivery"
            }
            campaign = {
                "name": "'Turn Abandoned Carts into VIP Customers'",
                "core_message": "Stop blasting desperate 20% discount codes to shoppers who just had a simple shipping question.",
                "hook": "Engage hesitating buyers with genuine AI conversational assistance and boost recovered revenue by 24%."
            }

        else: # SaaS / Tech / General
            positioning = "The Autonomous Execution Layer for High-Growth Enterprise Teams"
            channels = [
                {
                    "channel": "LinkedIn Account-Based Marketing & Founder Thought Leadership",
                    "priority": "Primary (40% Budget)",
                    "rationale": "Directly targets decision makers (VPs, Directors, C-Level) with engineering and ROI breakdowns of manual vs autonomous workflows."
                },
                {
                    "channel": "Generative Engine Optimization (GEO) & Technical Documentation",
                    "priority": "Primary (30% Budget)",
                    "rationale": "Ensures that when technical buyers ask ChatGPT, Perplexity, or Gemini 'What is the best tool for X', your platform is the authoritative #1 cited answer."
                },
                {
                    "channel": "Cold Outbound Multi-Touch Cadence (Email + LinkedIn)",
                    "priority": "Secondary (20% Budget)",
                    "rationale": "Highly tailored outbound targeting verified buying signals (e.g. company hiring sprees, executive changes, new software migrations)."
                },
                {
                    "channel": "Developer & Practitioner Community Sponsorships",
                    "priority": "Supporting (10% Budget)",
                    "rationale": "Grassroots technical adoption via podcasts, GitHub repositories, and specialized Discord / Slack groups."
                }
            ]
            keywords = [
                {"keyword": "autonomous multi agent workflow orchestration platform", "intent": "Commercial Evaluation", "volume": "High Growth", "priority": "Tier 1"},
                {"keyword": "generative engine optimization geo agency services", "intent": "High Transactional Intent", "volume": "Exploding", "priority": "Tier 1"},
                {"keyword": "automate sales pipeline qualification ai sdr", "intent": "Commercial Intent", "volume": "High", "priority": "Tier 1"}
            ]
            funnel = {
                "tofu": "The 2025 AI Workflow Benchmark & ROI Whitepaper",
                "mofu": "Interactive Live Workflow Simulator with Sample Data Ingestion",
                "bofu": "14-Day Production Pilot with Guaranteed 10x ROI or Full Refund"
            }
            campaign = {
                "name": "'Automate the Grind, Keep the Brains'",
                "core_message": "Free your highest-paid team members from repetitive administrative data entry.",
                "hook": "Deploy autonomous agents that complete 8 hours of manual research and qualification in 60 seconds."
            }

        self.record_usage("Marketing Positioning & Multi-Channel Strategy", input_tokens, output_tokens)

        return {
            "positioning_statement": positioning,
            "recommended_channels": channels,
            "high_intent_keywords": keywords,
            "acquisition_funnel": funnel,
            "flagship_campaign": campaign,
            "marketing_budget_recommendation": "Recommended starting budget: 15-20% of projected year-1 ARR, allocated heavily to highest intent validation channels."
        }
