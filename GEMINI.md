# Antigravity Agent Instructions: STRATIFY Engine

When the user types `/stratify` or requests market intelligence, competitor teardowns, prospect discovery, or strategic marketing plans:

1. **Activate the STRATIFY Skill**:
   - Reference `SKILL.md` and the 21 modular skills in `skills/`.
2. **Execute the 7-Step Research Workflow**:
   - Step 1: Industry Identification & Sub-Industry Classification
   - Step 2: Market Overview, Sizing (TAM/SAM/SOM), and CAGR Growth
   - Step 3: Customer Intelligence, Purchasing Power, and Buyer Personas
   - Step 4: Differentiated Business Opportunities (0-100 Scored)
   - Step 5: High-Value Verified Prospects (100% genuine corporate entities; zero fabrication)
   - Step 6: Competitor Intelligence & White-Space Teardowns
   - Step 7: GTM Strategy, SEO/GEO Keywords, and 7/30/60/90-Day Roadmap
3. **Execution Commands**:
   - `/stratify [industry] [--location <loc>] [--depth <quick|standard|deep>]`
   - `/stratify compare [industry_1] vs [industry_2]`
   - `/stratify competitors in [industry]`
   - `/stratify find high-value [industry] clients`
   - `/stratify marketing strategy for [industry]`
4. **CLI Fallback**:
   - Can execute directly via `node bin/stratify.js [command]` or `python stratify.py [command]`.
