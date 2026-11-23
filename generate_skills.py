"""
Skill generator script to establish the full 21 Core Skills for STRATIFY.
Each skill contains YAML frontmatter and comprehensive execution guidelines.
"""
import os

SKILLS_DEFINITIONS = [
    {
        "id": "market-research",
        "name": "Market Research",
        "category": "Market Intelligence",
        "description": "Systematic collection, analysis, and interpretation of market size, TAM/SAM/SOM, growth trajectories, and macroeconomic factors.",
        "industries": ["all", "healthcare", "real-estate", "ecommerce", "automotive", "saas", "financial-services"],
        "token_weight": 850,
        "content": """# Market Research Skill

## Overview
The Market Research skill conducts empirical quantitative and qualitative market assessments. It calculates Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM), analyzes CAGR, evaluates macroeconomic drivers, and discovers emerging opportunities.

## Methodology
1. **TAM / SAM / SOM Modeling**:
   - TAM: Total market demand for product/service category globally or nationally.
   - SAM: Market portion targeted by products/services within geographic reach.
   - SOM: Realistic market share captured within 2-3 years considering competition and resources.
2. **Growth & Trend Synthesis**:
   - CAGR projections backed by industry reports (e.g. Grand View Research, Statista, McKinsey).
   - Demand drivers (demographics, regulatory shifts, tech adoption).
3. **Macro Environmental Factors**:
   - PESTEL analysis (Political, Economic, Social, Technological, Environmental, Legal).
4. **Verification Requirement**:
   - Every metric must cite source, publication year, and state whether it is verified data or an empirical estimate.
"""
    },
    {
        "id": "industry-analysis",
        "name": "Industry Analysis",
        "category": "Market Intelligence",
        "description": "Evaluation of industry structure, maturity, regulatory environment, value chain dynamics, and structural barriers to entry.",
        "industries": ["all", "healthcare", "automotive", "construction", "agriculture"],
        "token_weight": 780,
        "content": """# Industry Analysis Skill

## Overview
Deconstructs industry maturity, Porter's Five Forces, regulatory frameworks, supply chain bottlenecks, and competitive dynamics.

## Methodology
1. **Industry Maturity Cycle**:
   - Embryonic, Growth, Shakeout, Mature, or Decline.
2. **Porter's Five Forces Assessment**:
   - Threat of New Entrants, Bargaining Power of Buyers, Bargaining Power of Suppliers, Threat of Substitutes, Rivalry among Existing Competitors.
3. **Regulatory & Compliance Scan**:
   - Sector-specific statutory mandates (e.g., HIPAA/FDA for healthcare, RESPA/DHSUD for real estate, DOT/NHTSA for automotive).
4. **Value Chain Mapping**:
   - Upstream suppliers -> Midstream processors/distributors -> Downstream retailers/end-users.
"""
    },
    {
        "id": "competitor-intelligence",
        "name": "Competitor Intelligence",
        "category": "Competitive Analysis",
        "description": "Deep competitor benchmarking, product teardowns, pricing models, positioning, customer sentiment, and market vulnerability discovery.",
        "industries": ["all", "saas", "ecommerce", "healthcare", "real-estate", "automotive"],
        "token_weight": 920,
        "content": """# Competitor Intelligence Skill

## Overview
Researches direct, indirect, and tertiary competitors. Gathers verifiable pricing data, feature matrix comparisons, review sentiment, and pinpoints exploitables gaps.

## Methodology
1. **Competitor Categorization**:
   - Direct Competitors (same solution, same audience).
   - Indirect Competitors (different solution, same underlying problem).
   - Potential Entrants (adjacent platforms expanding into category).
2. **Competitor Teardown Metrics**:
   - Offerings & Key USPs.
   - Public Pricing Tiers & Billing models.
   - Perceived Strengths (what customers praise).
   - Documented Weaknesses (common 1-star / 2-star complaints, G2/Capterra/Trustpilot/Reddit complaints).
3. **Market White Space Identification**:
   - Unmet needs, overpriced tiers, neglected customer tiers (e.g. SMBs vs Enterprise).
"""
    },
    {
        "id": "customer-research",
        "name": "Customer Research",
        "category": "Customer Intelligence",
        "description": "Investigation into user behaviors, friction points, operational bottlenecks, emotional triggers, and willingness-to-pay.",
        "industries": ["all", "healthcare", "real-estate", "ecommerce", "saas", "food-and-beverage"],
        "token_weight": 800,
        "content": """# Customer Research Skill

## Overview
Investigates the psychology, workflow pains, operational headaches, and economic consequences of unsolved customer problems.

## Methodology
1. **Jobs-to-be-Done (JTBD)**:
   - Functional Jobs (what task must be done).
   - Emotional Jobs (how they want to feel).
   - Social Jobs (how they want to be perceived).
2. **Pain Point Severity Matrix**:
   - High Frequency + High Severity (Critical to solve).
   - Low Frequency + High Severity (Insurance / Risk mitigation).
3. **Budget & Willingness-to-Pay (WTP)**:
   - ROI threshold required to trigger a purchasing decision.
"""
    },
    {
        "id": "customer-segmentation",
        "name": "Customer Segmentation",
        "category": "Customer Intelligence",
        "description": "Categorizes target market into distinct B2B, B2C, Enterprise, SME, and niche customer tiers with estimated purchasing power.",
        "industries": ["all", "saas", "ecommerce", "healthcare", "financial-services"],
        "token_weight": 750,
        "content": """# Customer Segmentation Skill

## Overview
Breaks down the broader market into high-yield segments based on firmographics, demographics, psychographics, and transactional capacity.

## Methodology
1. **Segmentation Dimensions**:
   - Enterprise ($100M+ revenue or 1000+ employees).
   - Mid-Market ($10M-$100M revenue, 100-999 employees).
   - SMB ($1M-$10M revenue, 10-99 employees).
   - Micro / Solopreneur (<$1M revenue, 1-9 employees).
   - Direct-to-Consumer / Household income tiers.
2. **Purchasing Power Index**:
   - Estimation of annual discretionary budget allocated to solution category.
"""
    },
    {
        "id": "ideal-customer-profile",
        "name": "Ideal Customer Profile (ICP)",
        "category": "Customer Intelligence",
        "description": "Rigorous definition of companies or accounts that derive the highest value from and present the lowest churn risk for the solution.",
        "industries": ["saas", "healthcare", "automotive", "financial-services", "construction", "b2b"],
        "token_weight": 700,
        "content": """# Ideal Customer Profile (ICP) Skill

## Overview
Defines exact firmographic, technographic, and environmental parameters that characterize the most profitable and satisfied target accounts.

## Methodology
1. **Firmographic Criteria**:
   - Industry sub-vertical, employee count range, ARR/revenue range, geographic headquarters.
2. **Technographic & Operational Fit**:
   - Existing tech stack, digital maturity level, regulatory oversight requirements.
3. **Trigger Events / Buying Signals**:
   - New funding round, C-level executive change, hiring spree, compliance deadline.
"""
    },
    {
        "id": "buyer-persona",
        "name": "Buyer Persona Development",
        "category": "Customer Intelligence",
        "description": "Detailed archetype modeling of key economic buyers, technical evaluators, internal champions, and blockers.",
        "industries": ["all", "saas", "ecommerce", "healthcare", "real-estate"],
        "token_weight": 720,
        "content": """# Buyer Persona Development Skill

## Overview
Constructs actionable behavioral personas detailing title, responsibilities, KPIs, objections, and preferred communication style.

## Methodology
1. **Persona Demographics & Role**:
   - Primary Title, Decision Power (Economic Buyer, Champion, Gatekeeper, End-User).
2. **KPIs & Goals**:
   - What metrics determine their bonus or promotion.
3. **Key Objections**:
   - Budget constraints, risk of failure, implementation complexity.
"""
    },
    {
        "id": "prospect-research",
        "name": "Prospect Research",
        "category": "Sales & Lead Generation",
        "description": "Identification and verification of real target companies, public domain buying signals, verified URLs, and tailored outreach hooks.",
        "industries": ["all", "b2b", "healthcare", "real-estate", "automotive", "saas"],
        "token_weight": 950,
        "content": """# Prospect Research Skill

## Overview
Identifies actual, verifiable companies operating in the specified industry and geographic region. STRICT RULE: Never invent companies or fabricated contact information.

## Methodology
1. **Verified Entity Discovery**:
   - Genuine company name, verified domain/website, confirmed geographic location.
2. **Contextual Fit Evaluation**:
   - Fit Score (0-100) based on industry relevance, scale, and operational alignment.
3. **Public Buying Signals**:
   - Verifiable expansion news, job openings, tech stack migrations, public tenders.
4. **Outreach Angle**:
   - Non-spammy, value-oriented conversation starter tailored to their public initiatives.
"""
    },
    {
        "id": "business-opportunity-discovery",
        "name": "Business Opportunity Discovery",
        "category": "Strategy & Innovation",
        "description": "Synthesizes market gaps into 5+ differentiated, actionable business concepts with business models and barrier assessments.",
        "industries": ["all", "healthcare", "real-estate", "ecommerce", "automotive", "saas"],
        "token_weight": 900,
        "content": """# Business Opportunity Discovery Skill

## Overview
Engineers high-margin business ideas that address verified pain points. Each opportunity includes concept, target customer, revenue model, and feasibility.

## Methodology
1. **Problem-Solution Pairings**:
   - Identified Pain Point -> Novel / Optimized Solution Mechanism.
2. **Opportunity Profile**:
   - Name & Concept Summary.
   - Target Customer Tier.
   - Proposed Revenue Model (SaaS, Commission, Retainer, Usage, Marketplace).
   - Competitive Moat (Data network effect, regulatory compliance, speed).
   - Execution Complexity (Low, Medium, High).
"""
    },
    {
        "id": "product-marketing",
        "name": "Product Marketing",
        "category": "Marketing Strategy",
        "description": "Product positioning, value proposition formulation, core messaging pillars, and feature-to-benefit translation.",
        "industries": ["saas", "ecommerce", "healthcare", "digital-marketing"],
        "token_weight": 760,
        "content": """# Product Marketing Skill

## Overview
Crafts compelling product positioning, differentiation narratives, and modular value messaging matrices.

## Methodology
1. **Positioning Statement Formula**:
   - For [target audience] who [urgent problem], [Solution] is a [product category] that [primary benefit]. Unlike [primary alternative], our solution [unique differentiator].
2. **Value Pillars**:
   - Speed/Efficiency, Cost Reduction, Revenue Acceleration, Risk Mitigation.
"""
    },
    {
        "id": "pricing-strategy",
        "name": "Pricing Strategy",
        "category": "Strategy & Innovation",
        "description": "Value-based pricing models, tiered packaging, unit economics, discounting thresholds, and margin optimization.",
        "industries": ["all", "saas", "ecommerce", "healthcare", "financial-services"],
        "token_weight": 740,
        "content": """# Pricing Strategy Skill

## Overview
Develops optimal monetization architecture matching customer willingness-to-pay and unit economics.

## Methodology
1. **Pricing Architectures**:
   - Tiered Subscription (Good/Better/Best), Usage-based, Flat-rate, Performance/Contingency fee.
2. **Unit Economics & Margin Target**:
   - Gross Margin target (e.g. 70-80% SaaS, 40-50% e-commerce, 50-60% services).
"""
    },
    {
        "id": "go-to-market-strategy",
        "name": "Go-To-Market Strategy",
        "category": "Strategy & Innovation",
        "description": "End-to-end launch blueprint, distribution channels, early adopter acquisition, partnership ecosystem, and milestone timelines.",
        "industries": ["all", "saas", "ecommerce", "real-estate", "healthcare"],
        "token_weight": 860,
        "content": """# Go-To-Market (GTM) Strategy Skill

## Overview
Designs the holistic launch plan, sales motion (PLG vs SLG), strategic partnerships, and 30-60-90 day milestone roadmap.

## Methodology
1. **Motion Selection**:
   - Product-Led Growth (PLG), Sales-Led Growth (SLG), Channel Partner Led, or Inbound Community Led.
2. **Beachhead Strategy**:
   - Identifying the easiest wedge to penetrate the market before expanding laterally.
3. **Phased Milestone Roadmap**:
   - First 7 Days, 30 Days, 60 Days, 90 Days.
"""
    },
    {
        "id": "marketing-psychology",
        "name": "Marketing Psychology",
        "category": "Marketing Strategy",
        "description": "Applies cognitive biases, behavioral economics principles, loss aversion, social proof, and decision architecture.",
        "industries": ["ecommerce", "real-estate", "healthcare", "digital-marketing"],
        "token_weight": 680,
        "content": """# Marketing Psychology Skill

## Overview
Leverages proven cognitive and behavioral economics principles (Cialdini, Kahneman) to optimize conversion and trust.

## Methodology
1. **Cognitive Triggers**:
   - Loss Aversion, Social Proof, Authority Signatures, Anchoring, Scarcity & Urgency.
2. **Risk Reversal**:
   - Guarantees, free trials, compliance certifications, zero-lock-in policies.
"""
    },
    {
        "id": "sales-strategy",
        "name": "Sales Strategy",
        "category": "Sales & Lead Generation",
        "description": "Outbound prospecting cadences, discovery call frameworks, enterprise objection handling, and deal closing tactics.",
        "industries": ["b2b", "saas", "healthcare", "real-estate", "automotive", "financial-services"],
        "token_weight": 810,
        "content": """# Sales Strategy Skill

## Overview
Structures effective enterprise and mid-market sales motions, qualification criteria (BANT / MEDDPICC), and objection scripts.

## Methodology
1. **Sales Cadence Architecture**:
   - Multi-touch outreach (Email, LinkedIn, Phone, Video).
2. **Qualification Frameworks**:
   - Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion, Competition.
"""
    },
    {
        "id": "seo-geo",
        "name": "SEO and GEO (Generative Engine Optimization)",
        "category": "Growth & Distribution",
        "description": "Search engine optimization and Generative Engine Optimization strategies for AI search engines (ChatGPT, Gemini, Perplexity).",
        "industries": ["all", "ecommerce", "saas", "healthcare", "real-estate", "digital-marketing"],
        "token_weight": 840,
        "content": """# SEO and GEO (Generative Engine Optimization) Skill

## Overview
Synthesizes traditional algorithmic search ranking with modern Generative AI citation optimization (ChatGPT Search, Perplexity, Google SGE/AI Overviews).

## Methodology
1. **Algorithmic Search**:
   - High-intent commercial keywords, technical site structure, backlink authority.
2. **Generative Engine Optimization (GEO)**:
   - Authority citations, structured entity data, factual clarity, brand presence on trusted directories (Wikidata, G2, TechCrunch, Reddit).
"""
    },
    {
        "id": "keyword-research",
        "name": "Keyword Research",
        "category": "Growth & Distribution",
        "description": "Discovery of high-intent transactional, informational, and navigational search queries with difficulty and volume metrics.",
        "industries": ["ecommerce", "saas", "real-estate", "healthcare", "digital-marketing"],
        "token_weight": 720,
        "content": """# Keyword Research Skill

## Overview
Identifies high-value search terms grouped by user intent and purchase readiness.

## Methodology
1. **Search Intent Clusters**:
   - Informational ('what is X') -> Commercial ('best X tools') -> Transactional ('X pricing / buy X').
2. **Long-tail High Conversion Keywords**:
   - Low competition, high-converting specific queries.
"""
    },
    {
        "id": "content-marketing",
        "name": "Content Marketing",
        "category": "Growth & Distribution",
        "description": "Editorial strategy, thought leadership frameworks, whitepapers, case study formats, and educational funnels.",
        "industries": ["saas", "healthcare", "financial-services", "digital-marketing", "real-estate"],
        "token_weight": 750,
        "content": """# Content Marketing Skill

## Overview
Builds compound organic demand through authoritative thought leadership, educational lead magnets, and customer case studies.

## Methodology
1. **Content Funnel Mapping**:
   - Top of Funnel (TOFU): Industry trends, diagnostic quizzes, industry reports.
   - Middle of Funnel (MOFU): Comparison guides, ROI calculators, vendor checklists.
   - Bottom of Funnel (BOFU): Customer case studies, proof of concept playbooks.
"""
    },
    {
        "id": "social-media-marketing",
        "name": "Social Media Marketing",
        "category": "Growth & Distribution",
        "description": "Platform-specific content strategies (LinkedIn for B2B, TikTok/Instagram for B2C/DTC, YouTube for technical depth).",
        "industries": ["ecommerce", "food-and-beverage", "real-estate", "saas", "automotive"],
        "token_weight": 700,
        "content": """# Social Media Marketing Skill

## Overview
Selects the exact high-performing social channels matching the target demographic rather than spraying generic content everywhere.

## Methodology
1. **Channel Selection Matrix**:
   - LinkedIn: B2B decision makers, executive thought leadership.
   - YouTube: In-depth product reviews, walkthroughs, educational guides.
   - Instagram / TikTok: Visual lifestyle, D2C consumer goods, real estate tours.
"""
    },
    {
        "id": "paid-advertising",
        "name": "Paid Advertising",
        "category": "Growth & Distribution",
        "description": "Paid media acquisition across Google Search, LinkedIn Ads, Meta Ads, and programmatic networks with CPA/ROAS targets.",
        "industries": ["ecommerce", "saas", "real-estate", "healthcare", "automotive"],
        "token_weight": 790,
        "content": """# Paid Advertising Skill

## Overview
Structures high-efficiency paid acquisition campaigns with strict Customer Acquisition Cost (CAC) and Return on Ad Spend (ROAS) guidelines.

## Methodology
1. **Channel Alignment**:
   - Google Search Ads: Capture immediate active intent.
   - LinkedIn Ads: Target specific job titles, company sizes, and industries.
   - Meta Ads: Retargeting, lookalike audiences, visual creative storytelling.
2. **Unit Economic Guardrails**:
   - Max allowable CAC based on Customer Lifetime Value (LTV:CAC >= 3:1).
"""
    },
    {
        "id": "conversion-rate-optimization",
        "name": "Conversion Rate Optimization (CRO)",
        "category": "Growth & Distribution",
        "description": "Landing page architecture, friction reduction, CTA hierarchy, form optimization, and behavioral tracking.",
        "industries": ["ecommerce", "saas", "real-estate", "digital-marketing"],
        "token_weight": 730,
        "content": """# Conversion Rate Optimization (CRO) Skill

## Overview
Maximizes visitor-to-lead and visitor-to-customer conversion efficiency through rigorous heuristics and behavioral UX design.

## Methodology
1. **Landing Page Architecture**:
   - Above-the-fold value proposition, immediate CTA, proof badge ribbon, interactive demo/calculator.
2. **Friction Minimization**:
   - Single-field email capture, social logins, transparent pricing previews.
"""
    },
    {
        "id": "analytics-performance",
        "name": "Analytics and Performance Measurement",
        "category": "Market Intelligence",
        "description": "KPI frameworks, marketing attribution modeling, cohort retention analysis, and revenue telemetry.",
        "industries": ["all", "saas", "ecommerce", "financial-services", "digital-marketing"],
        "token_weight": 710,
        "content": """# Analytics and Performance Measurement Skill

## Overview
Establishes the quantitative dashboards, North Star metrics, customer acquisition economics, and attribution tracking models.

## Methodology
1. **Key Performance Indicators (KPIs)**:
   - Acquisition: CAC, MQLs, SQLs, CPL.
   - Retention: Churn rate, Net Revenue Retention (NRR), LTV.
   - Conversion: Lead-to-Opportunity rate, Opportunity-to-Win rate.
"""
    }
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, "skills")
    os.makedirs(skills_dir, exist_ok=True)
    
    for s in SKILLS_DEFINITIONS:
        skill_path = os.path.join(skills_dir, s["id"])
        os.makedirs(skill_path, exist_ok=True)
        file_path = os.path.join(skill_path, "SKILL.md")
        
        yaml_header = f"""---
name: "{s['name']}"
id: "{s['id']}"
category: "{s['category']}"
description: "{s['description']}"
industry_affinity: {s['industries']}
token_weight: {s['token_weight']}
---
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(yaml_header + "\n" + s["content"].strip() + "\n")
        print(f"Generated {s['id']}/SKILL.md")
        
    print(f"Successfully created all {len(SKILLS_DEFINITIONS)} skills!")

if __name__ == "__main__":
    main()
