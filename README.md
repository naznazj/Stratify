# STRATIFY — Business Intelligence & Strategic Marketing Skill

An installable AI agent skill for autonomous business research, market discovery, verified prospecting, and marketing strategy with token-saving dynamic skill routing.

---

## What is STRATIFY?

STRATIFY is an AI agent skill that adds business intelligence and marketing strategy capabilities to your AI agent environment (Google Antigravity, Claude Code, Cursor, AutoGPT, and Gemini-based agents).

Instead of dumping massive, monolithic prompts that exhaust context windows and waste thousands of tokens, STRATIFY functions like a clean modular ponytail: it houses a catalog of 21 specialized sub-skills and dynamically routes only the exact skills needed for a given industry and research depth. This eliminates context clutter and cuts token consumption by 50% to 70%.

---

## How to Install the Skill

### Method 1: One-Command Auto-Installer (Recommended)

Run via npx to automatically detect and install STRATIFY into your local AI agent skills directory:

```bash
npx stratify-ai --install-skill
```

This scans and installs STRATIFY into:
- Google Antigravity: `~/.gemini/antigravity/skills/stratify`
- Universal Agent Directory: `~/.agent/skills/stratify`
- Cursor Skills Directory: `~/.cursor/skills/stratify`

### Method 2: Git Clone into Agent Skills Folder

Clone this repository directly into your agent's skills path:

```bash
# For Google Antigravity:
git clone https://github.com/naznazj/Stratify.git ~/.gemini/antigravity/skills/stratify

# For Cursor / Claude Code / other agents:
git clone https://github.com/naznazj/Stratify.git ~/.agent/skills/stratify

# Or within a local project workspace:
git clone https://github.com/naznazj/Stratify.git skills/stratify
```

### Method 3: Global NPM Install

```bash
npm install -g stratify-ai
stratify --install-skill
```

---

## How to Use the Skill

Once installed, your AI agent automatically recognizes the `/stratify` command in chat:

```text
/stratify [industry]
```

### Examples:

- `/stratify Healthcare`
- `/stratify Healthcare --location Philippines`
- `/stratify Real Estate --location USA --depth deep`
- `/stratify Automotive`
- `/stratify E-commerce`
- `/stratify Technology and SaaS`
- `/stratify Financial Services`

### Targeted Sub-Commands:

- `/stratify expand healthcare opportunities`
- `/stratify competitors in automotive`
- `/stratify find high-value real estate clients`
- `/stratify marketing strategy for e-commerce`
- `/stratify compare Healthcare vs Real Estate`

---

## Token-Saving Dynamic Skill Routing

Most marketing prompts inject dozens of generic rules into every request, bloating token counts. STRATIFY solves this with a Dynamic Skill Router that selects only relevant sub-skills:

- Quick Depth: Loads 4-5 anchor skills (~55% token weight reduction).
- Standard Depth: Loads 8-10 targeted skills (~40% token weight reduction).
- Deep Depth: Loads 14-16 comprehensive skills for full-spectrum research.

### Sub-Skills Catalog (`skills/`):

1. `market-research`: TAM/SAM/SOM sizing and macroeconomic trends.
2. `industry-analysis`: Value chain structure and regulatory scanning.
3. `competitor-intelligence`: Teardowns, pricing benchmarks, and white-space gaps.
4. `customer-research`: Jobs-to-be-Done (JTBD) and willingness-to-pay.
5. `customer-segmentation`: B2B, B2C, Enterprise, and SME tier purchasing power.
6. `ideal-customer-profile`: Firmographic and technographic ICP qualification.
7. `buyer-persona`: Decision-maker archetypes, KPIs, and objections.
8. `prospect-research`: Verified corporate entities and buying signals (zero hallucinated contacts).
9. `business-opportunity-discovery`: Differentiated business concepts solving validated pains.
10. `product-marketing`: Value proposition narratives and core messaging.
11. `pricing-strategy`: Value-based pricing, unit economics, and margin optimization.
12. `go-to-market-strategy`: Launch blueprint, beachhead wedge, and milestone timeline.
13. `marketing-psychology`: Loss aversion, social proof, and decision architecture.
14. `sales-strategy`: Multi-touch outbound prospecting and qualification frameworks.
15. `seo-geo`: Generative Engine Optimization for ChatGPT, Perplexity, and Gemini.
16. `keyword-research`: High-intent commercial and transactional search queries.
17. `content-marketing`: Editorial strategy, TOFU/MOFU/BOFU funnels, and lead magnets.
18. `social-media-marketing`: Channel prioritization (LinkedIn, TikTok, YouTube).
19. `paid-advertising`: CAC/ROAS economic guardrails and ad unit structures.
20. `conversion-rate-optimization`: Landing page heuristics and friction reduction.
21. `analytics-performance`: North Star metrics, cohort retention, and attribution.

---

## Standalone CLI & SaaS Dashboard

STRATIFY also includes a standalone Python CLI and an optional SaaS dashboard:

### Terminal CLI:

```bash
# Run research from terminal:
python stratify.py "/stratify Healthcare --location Philippines"

# Interactive REPL mode:
python stratify.py --repl
```

### SaaS Web Dashboard:

```bash
python server.py
# Open http://127.0.0.1:8000
```

---

## Verification & Automated Tests

All core research workflows, sub-commands, routing savings, and API endpoints are covered by automated unit tests:

```bash
# Run core skill tests:
python -m unittest tests/test_stratify.py

# Run API endpoint tests:
python -m unittest tests/test_api_endpoints.py
```

---

## License

MIT
