"""
STRATIFY Industry Classifier
Understands industry domains, sub-verticals, market maturity, regulatory environments,
and establishes intelligent default geographic locations if none are provided.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class IndustryProfile(BaseModel):
    industry_key: str
    display_name: str
    subindustries: List[str]
    business_models: List[str]
    customer_types: List[str]
    market_maturity: str
    regulatory_frameworks: List[str]
    key_drivers: List[str]
    risk_factors: List[str]
    default_location: str
    geographic_market: str
    recommended_skills: List[str]

INDUSTRY_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "healthcare": {
        "key": "healthcare",
        "display_name": "Healthcare & Life Sciences",
        "aliases": ["health", "medical", "hospital", "biotech", "pharma", "clinical", "telehealth", "medicine"],
        "subindustries": [
            "Digital Health & Telemedicine",
            "Clinical Workflow & EHR Software",
            "Medical Devices & Diagnostics",
            "Outpatient & Ambulatory Care",
            "Specialized Diagnostics & Laboratory Networks",
            "Elderly Care & Home Health Assistance"
        ],
        "business_models": ["B2B SaaS", "B2B Medical Supply", "B2C Care Services", "B2B2C Insurance Programs"],
        "customer_types": ["Hospitals & Health Systems", "Private Clinics", "Diagnostic Laboratories", "Patients & Caregivers", "Health Insurers"],
        "market_maturity": "Mature with Rapid Digital Transition",
        "regulatory_frameworks": ["HIPAA (US)", "FDA 510(k) Cleared Software", "DOH / FDA (PH)", "GDPR Health Annex (EU)"],
        "key_drivers": ["Aging populations", "Shift to preventive care", "Chronic disease management", "Shortage of medical staff"],
        "risk_factors": ["Lengthy procurement cycles (6-18 months)", "Severe privacy liability", "Reimbursement uncertainties"],
        "default_location": "United States & Global",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "customer-segmentation",
            "ideal-customer-profile",
            "buyer-persona",
            "competitor-intelligence",
            "business-opportunity-discovery",
            "prospect-research",
            "sales-strategy",
            "seo-geo",
            "content-marketing",
            "go-to-market-strategy"
        ]
    },
    "real_estate": {
        "key": "real_estate",
        "display_name": "Real Estate & PropTech",
        "aliases": ["real estate", "property", "proptech", "brokerage", "housing", "realty", "reit", "mortgage"],
        "subindustries": [
            "Residential Property Brokerage & Marketplaces",
            "Commercial Real Estate & Coworking",
            "Property Management Software (PropTech)",
            "Short-term Rental Management (Airbnb / Hospitality)",
            "Real Estate Investment & Crowdfunding"
        ],
        "business_models": ["Transaction Commission", "SaaS Subscription", "Asset Management Fee", "Lead Generation Fee"],
        "customer_types": ["Property Developers", "Licensed Brokers & Agents", "Institutional & Retail Investors", "Homebuyers & Tenants"],
        "market_maturity": "Mature (Digitally Evolving)",
        "regulatory_frameworks": ["RESPA (US)", "Fair Housing Act", "DHSUD & PRC Real Estate Service Act (PH)", "Anti-Money Laundering (AMLA)"],
        "key_drivers": ["Urbanization", "Interest rate fluctuations", "Demand for tech-enabled tenant experiences", "Remote work migration"],
        "risk_factors": ["High sensitivity to interest rate spikes", "Illiquid asset cycles", "Regional zoning restrictions"],
        "default_location": "United States",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "customer-research",
            "buyer-persona",
            "competitor-intelligence",
            "business-opportunity-discovery",
            "prospect-research",
            "seo-geo",
            "paid-advertising",
            "conversion-rate-optimization",
            "go-to-market-strategy"
        ]
    },
    "ecommerce": {
        "key": "ecommerce",
        "display_name": "E-commerce & Direct-to-Consumer (D2C)",
        "aliases": ["ecommerce", "e-commerce", "retail", "online store", "d2c", "dropshipping", "shopping"],
        "subindustries": [
            "Omnichannel Consumer Goods & D2C Brands",
            "E-commerce Enablement & Fulfillment Tech",
            "Social Commerce & Live Shopping Platforms",
            "B2B Wholesale Digital Marketplaces",
            "Subscription Commerce & Personalized Retail"
        ],
        "business_models": ["Direct-to-Consumer (D2C)", "B2B Marketplace", "Subscription Box", "Drop-ship / White-label"],
        "customer_types": ["Online Shoppers", "B2B Wholesalers", "D2C Brand Merchants", "Omnichannel Retailers"],
        "market_maturity": "High Growth & Highly Competitive",
        "regulatory_frameworks": ["FTC Endorsement Guides", "Consumer Product Safety (CPSC)", "PCI-DSS Payment Compliance", "Data Privacy (GDPR/CCPA)"],
        "key_drivers": ["Mobile shopping penetration", "AI personalization", "Social commerce on TikTok/Instagram", "Fast logistics demand"],
        "risk_factors": ["Rising Customer Acquisition Costs (CAC)", "Supply chain delays", "High product return rates"],
        "default_location": "Global / North America",
        "recommended_skills": [
            "market-research",
            "customer-research",
            "competitor-intelligence",
            "business-opportunity-discovery",
            "pricing-strategy",
            "product-marketing",
            "marketing-psychology",
            "paid-advertising",
            "conversion-rate-optimization",
            "social-media-marketing",
            "seo-geo",
            "analytics-performance"
        ]
    },
    "automotive": {
        "key": "automotive",
        "display_name": "Automotive & Mobility",
        "aliases": ["automotive", "auto", "car", "vehicles", "electric vehicles", "ev", "fleet", "mobility"],
        "subindustries": [
            "Electric Vehicle (EV) Infrastructure & Software",
            "Connected Fleet Telematics & Asset Tracking",
            "Automotive Aftermarket & Parts Distribution",
            "Dealership Management Systems (DMS)",
            "Autonomous Driving Tech & ADAS"
        ],
        "business_models": ["B2B Fleet SaaS", "B2B Parts Wholesaling", "Dealership Retainer", "Consumer Financing & Lease"],
        "customer_types": ["Commercial Fleet Operators", "Auto Dealerships", "Independent Repair Workshops", "Tier 1 & 2 Suppliers", "Individual Motorists"],
        "market_maturity": "Transformational (ICE to EV transition)",
        "regulatory_frameworks": ["NHTSA / FMVSS (US)", "EPA Emission Mandates", "UNECE Cyber Security Regulation R155", "LTO / LTFRB (PH)"],
        "key_drivers": ["Decarbonization mandates", "IoT connectivity in vehicles", "Rising fleet operational costs", "EV charging network expansion"],
        "risk_factors": ["High capital expenditure", "Semiconductor & battery material volatility", "Strict safety liabilities"],
        "default_location": "United States & Global",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "competitor-intelligence",
            "ideal-customer-profile",
            "prospect-research",
            "business-opportunity-discovery",
            "sales-strategy",
            "pricing-strategy",
            "go-to-market-strategy"
        ]
    },
    "saas": {
        "key": "saas",
        "display_name": "Technology, Software & SaaS",
        "aliases": ["saas", "software", "tech", "technology", "artificial intelligence", "ai", "cloud", "b2b saas"],
        "subindustries": [
            "Vertical AI & Workflow Automation",
            "Enterprise Cybersecurity & Identity Governance",
            "Developer Tools & Cloud Infrastructure",
            "Revenue Operations & CRM Systems",
            "Fintech & Embedded Financial Infrastructure"
        ],
        "business_models": ["Subscription ARR/MRR", "Usage-based / Consumption Pricing", "Product-Led Growth (Freemium)", "Enterprise Sales"],
        "customer_types": ["Chief Information Officers (CIOs)", "CTOs & Engineering Leads", "Operations & HR Executives", "SMB Business Owners"],
        "market_maturity": "Mature with Generative AI Disruption",
        "regulatory_frameworks": ["SOC 2 Type II", "ISO 27001", "EU AI Act", "GDPR & CCPA"],
        "key_drivers": ["Generative AI integration", "OpEx efficiency pressure", "Automation of repetitive manual knowledge work"],
        "risk_factors": ["High software churn in SMB tier", "Rapid commoditization of basic wrappers", "Prolonged enterprise security reviews"],
        "default_location": "United States & Global",
        "recommended_skills": [
            "market-research",
            "competitor-intelligence",
            "customer-segmentation",
            "ideal-customer-profile",
            "buyer-persona",
            "business-opportunity-discovery",
            "pricing-strategy",
            "product-marketing",
            "go-to-market-strategy",
            "sales-strategy",
            "seo-geo",
            "content-marketing",
            "conversion-rate-optimization",
            "analytics-performance"
        ]
    },
    "financial_services": {
        "key": "financial_services",
        "display_name": "Financial Services & FinTech",
        "aliases": ["finance", "fintech", "banking", "financial services", "insurance", "wealth", "lending", "credit"],
        "subindustries": [
            "Digital Lending & Micro-Financing",
            "Payment Gateways & Cross-Border Remittances",
            "InsurTech & Automated Underwriting",
            "Wealth Management & Algorithmic Robo-Advisory",
            "RegTech & AML/KYC Compliance Automation"
        ],
        "business_models": ["Basis Point Transaction Fee", "Interchange", "SaaS License", "Net Interest Margin (NIM)"],
        "customer_types": ["Retail Banking Customers", "SMEs seeking Working Capital", "Family Offices & HNWIs", "Commercial Banks"],
        "market_maturity": "Mature with High FinTech Inroads",
        "regulatory_frameworks": ["SEC & FINRA (US)", "BSP (Bangko Sentral ng Pilipinas)", "PCI-DSS", "Consumer Financial Protection (CFPB)"],
        "key_drivers": ["Financial inclusion in emerging markets", "Instant payment rails", "AI fraud detection"],
        "risk_factors": ["Intense regulatory oversight and licensing hurdles", "Cybersecurity breaches", "Credit default volatility"],
        "default_location": "United States & Emerging Markets",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "competitor-intelligence",
            "customer-segmentation",
            "prospect-research",
            "business-opportunity-discovery",
            "pricing-strategy",
            "sales-strategy",
            "content-marketing",
            "go-to-market-strategy"
        ]
    },
    "food_and_beverage": {
        "key": "food_and_beverage",
        "display_name": "Food & Beverage (F&B) & FoodTech",
        "aliases": ["food", "beverage", "restaurant", "food and beverage", "f&b", "hospitality", "dining", "catering"],
        "subindustries": [
            "Ghost Kitchens & Cloud Dining Concepts",
            "Functional Health & Organic Packaged Foods",
            "Restaurant POS & Kitchen Display Automation",
            "B2B Wholesale Ingredients Procurement Platforms",
            "Ready-to-Eat Meal Prep & Delivery Subscriptions"
        ],
        "business_models": ["Direct Retail / Dining Margin", "Franchise Royalty", "B2B Distribution Margin", "Subscription"],
        "customer_types": ["General Consumers", "Health-conscious Diners", "Restaurant Owners & Operators", "Catering Directors"],
        "market_maturity": "Mature / Low-Margin High-Volume",
        "regulatory_frameworks": ["FDA Food Safety Modernization Act (FSMA)", "Health Inspection Sanitation", "Nutritional Labeling Mandates"],
        "key_drivers": ["Health & functional food craze", "Delivery app convenience", "Automation of back-of-house kitchen operations"],
        "risk_factors": ["Perishable inventory spoilage", "Labor turnover", "High food cost inflation"],
        "default_location": "North America & Southeast Asia",
        "recommended_skills": [
            "market-research",
            "customer-research",
            "buyer-persona",
            "competitor-intelligence",
            "business-opportunity-discovery",
            "pricing-strategy",
            "social-media-marketing",
            "marketing-psychology",
            "paid-advertising",
            "go-to-market-strategy"
        ]
    },
    "construction": {
        "key": "construction",
        "display_name": "Construction & ConTech",
        "aliases": ["construction", "building", "contractor", "civil engineering", "architecture", "infrastructure"],
        "subindustries": [
            "Prefabricated & Modular Building Systems",
            "Job Site Telematics & Safety Monitoring Software",
            "Building Information Modeling (BIM) & 3D Scanning",
            "Heavy Equipment Rental & Fleet Management",
            "Sustainable Green Building Materials"
        ],
        "business_models": ["Fixed-Price Contract", "Time & Materials", "ConTech SaaS Subscription", "Equipment Rental"],
        "customer_types": ["General Contractors (GCs)", "Subcontractors & Trades", "Civil Engineering Firms", "Real Estate Developers", "Municipalities"],
        "market_maturity": "Mature (Digitally Laggard, Rapidly Modernizing)",
        "regulatory_frameworks": ["OSHA Safety Standards", "Municipal Building Codes (IBC)", "Environmental Impact Statements (NEPA)"],
        "key_drivers": ["Infrastructure spending programs", "Labor shortages driving prefabrication", "Green building codes"],
        "risk_factors": ["Supply chain raw material delays (steel/cement)", "Cost overruns", "Subcontractor default risk"],
        "default_location": "United States & Developing Markets",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "competitor-intelligence",
            "ideal-customer-profile",
            "prospect-research",
            "business-opportunity-discovery",
            "sales-strategy",
            "pricing-strategy",
            "go-to-market-strategy"
        ]
    },
    "agriculture": {
        "key": "agriculture",
        "display_name": "Agriculture & AgriTech",
        "aliases": ["agriculture", "farming", "agritech", "crops", "livestock", "agribusiness", "aquaculture"],
        "subindustries": [
            "Precision Agriculture & Satellite Crop Telemetry",
            "Controlled Environment Agriculture (Vertical Farming)",
            "Automated Drone Spraying & Soil Health Diagnostics",
            "Agri-Financing & Crop Insurance Technology",
            "Farm-to-Market Supply Chain Traceability"
        ],
        "business_models": ["SaaS / DaaS (Data-as-a-Service)", "Input Sales Margin", "Offtake Commission", "Equipment Financing"],
        "customer_types": ["Commercial Farm Enterprises", "Smallholder Cooperatives", "Agrochemical & Seed Distributors", "Food Processors"],
        "market_maturity": "Developing (High Tech Potential)",
        "regulatory_frameworks": ["USDA & EPA Pesticide Regulations", "GlobalGAP Certification", "Department of Agriculture (PH)"],
        "key_drivers": ["Climate volatility adaptation", "Water conservation imperatives", "Yield optimization per hectare"],
        "risk_factors": ["Extreme weather vulnerability", "Seasonal cash flow fluctuations", "Slow farmer tech adoption"],
        "default_location": "United States, Latin America, & Southeast Asia",
        "recommended_skills": [
            "market-research",
            "industry-analysis",
            "customer-research",
            "ideal-customer-profile",
            "prospect-research",
            "business-opportunity-discovery",
            "sales-strategy",
            "go-to-market-strategy"
        ]
    },
    "digital_marketing": {
        "key": "digital_marketing",
        "display_name": "Digital Marketing & AdTech",
        "aliases": ["digital marketing", "marketing agency", "adtech", "advertising", "seo", "content agency", "media"],
        "subindustries": [
            "AI-Powered Content & Creative Production Studios",
            "GEO (Generative Engine Optimization) & AI Search Advisory",
            "Performance Marketing & B2B ABM Media Buying",
            "Influencer & Creator Economy Management Platforms",
            "Retention Marketing & Omnichannel Lifecycle Automation"
        ],
        "business_models": ["Monthly Retainer", "Performance % of Ad Spend", "Project Fee", "SaaS Tooling License"],
        "customer_types": ["E-commerce Brand Owners", "B2B SaaS Growth Leads", "Local Service Businesses", "Enterprise CMOs"],
        "market_maturity": "Mature & Undergoing Generative AI Disruption",
        "regulatory_frameworks": ["FTC Disclosure Guidelines", "CAN-SPAM Act", "Cookieless Tracking / Privacy Sandbox"],
        "key_drivers": ["Generative AI creative scaling", "Deprecation of third-party cookies", "GEO / AI Search replacing traditional SEO"],
        "risk_factors": ["High client churn rate", "Low barrier to entry for solo operators", "Platform algorithm volatility"],
        "default_location": "United States & Global",
        "recommended_skills": [
            "market-research",
            "competitor-intelligence",
            "customer-research",
            "ideal-customer-profile",
            "business-opportunity-discovery",
            "seo-geo",
            "keyword-research",
            "content-marketing",
            "paid-advertising",
            "social-media-marketing",
            "conversion-rate-optimization",
            "analytics-performance",
            "sales-strategy"
        ]
    }
}

class IndustryClassifier:
    def __init__(self):
        self.kb = INDUSTRY_KNOWLEDGE_BASE

    def classify(self, industry_query: str, requested_location: Optional[str] = None) -> IndustryProfile:
        q = industry_query.lower().strip()
        
        # Match against knowledge base keys and aliases
        matched_profile = None
        for key, data in self.kb.items():
            if key in q or data["display_name"].lower() in q:
                matched_profile = data
                break
            for alias in data["aliases"]:
                if alias in q:
                    matched_profile = data
                    break
            if matched_profile:
                break
                
        # If not directly matched, build a dynamic generalized profile
        if not matched_profile:
            matched_profile = {
                "key": q.replace(" ", "_"),
                "display_name": industry_query.title(),
                "subindustries": [
                    f"Core {industry_query.title()} Services",
                    f"Digital {industry_query.title()} Solutions",
                    f"B2B {industry_query.title()} Enablement",
                    f"Specialized {industry_query.title()} Products"
                ],
                "business_models": ["B2B Services", "Direct-to-Customer", "SaaS & Digital Delivery", "Marketplace"],
                "customer_types": ["Enterprise Buyers", "Mid-Market Companies", "SMEs", "End-Consumers"],
                "market_maturity": "Growth & Modernizing",
                "regulatory_frameworks": ["Standard Commercial & Consumer Protection Regulations", "Data Privacy & Trade Standards"],
                "key_drivers": ["Digital modernization", "Customer experience improvements", "Operational cost efficiency"],
                "risk_factors": ["Market fragmentation", "Macroeconomic headwinds", "Customer acquisition costs"],
                "default_location": "United States & Global",
                "recommended_skills": [
                    "market-research",
                    "industry-analysis",
                    "competitor-intelligence",
                    "customer-segmentation",
                    "ideal-customer-profile",
                    "buyer-persona",
                    "business-opportunity-discovery",
                    "prospect-research",
                    "pricing-strategy",
                    "go-to-market-strategy",
                    "sales-strategy",
                    "seo-geo"
                ]
            }

        effective_location = requested_location.strip() if requested_location else matched_profile["default_location"]

        return IndustryProfile(
            industry_key=matched_profile["key"],
            display_name=matched_profile["display_name"],
            subindustries=matched_profile["subindustries"],
            business_models=matched_profile["business_models"],
            customer_types=matched_profile["customer_types"],
            market_maturity=matched_profile["market_maturity"],
            regulatory_frameworks=matched_profile["regulatory_frameworks"],
            key_drivers=matched_profile["key_drivers"],
            risk_factors=matched_profile["risk_factors"],
            default_location=matched_profile["default_location"],
            geographic_market=effective_location,
            recommended_skills=matched_profile["recommended_skills"]
        )
