# THIRD-PARTY INTELLECTUAL PROPERTY & LICENSE REGISTRY

**Package:** `stratify-ai`  
**Copyright Holder & Lead Maintainer:** `naznazj`  
**License Compliance Audit Date:** 2026-11-23 09:36:28 UTC  
**Commercial Distribution Status:** COMPLIANT  
**Marketplace Target Readiness (Agensi.io, NPM):** READY

---

## 1. Compliance Statement & IP Architecture

STRATIFY is an open-source business intelligence and strategic marketing engine designed for commercial and enterprise agent workflows. To protect commercial distributability and maintain strict respect for third-party intellectual property:

1. **Separation of Concerns:** STRATIFY's core multi-agent orchestrator (`stratify_core/`), dynamic skill router, and opportunity scoring engine are original, proprietary intellectual property independently authored by **naznazj** and distributed under the **MIT License**.
2. **Third-Party Skill Isolation:** Any external or modular skills integrated into the `skills/` directory are maintained under their original licenses with full author attribution preserved.
3. **Zero Proprietary Infringement:** Proprietary or unlicensed skills without explicit commercial grants are strictly forbidden from distribution in STRATIFY.

---

## 2. Skill Intake & Approval Categories

Before integrating any external skill, STRATIFY follows a mandatory 7-step intake protocol:
1. Identify original author and repository provenance.
2. Locate and inspect its formal `LICENSE` file.
3. Verify whether commercial use is explicitly granted.
4. Check modification, attribution, and redistribution clauses.
5. Preserve original copyright notices and contributor credits.
6. Record original repository URLs and licensing texts in this registry.
7. Enforce programmatic runtime compliance checks.

### Classification Matrix

| Approval Category | Commercial Use Permitted | Requirements / Restrictions |
|---|---|---|
| **APPROVED** | Yes | Permissive license (MIT, Apache 2.0, BSD-2/3, ISC). Fully cleared for commercial bundling. |
| **CONDITIONAL** | Yes (With Notice) | Attribution or ShareAlike notice required (CC-BY-4.0, CC-BY-SA, LGPL). Notice must be presented in build. |
| **RESTRICTED** | No / Requires Review | Strong copyleft (GPL) or non-commercial (CC-BY-NC). Requires explicit commercial waiver or legal sign-off. |
| **UNKNOWN** | Prohibited | No verifiable license found. **Strictly forbidden: do not copy, modify, redistribute, or sell.** |

---

## 3. Registered Skill Catalog & Licensing Status

Total Registered Skills: **21**  
Approved: **21** | Conditional: **0** | Restricted: **0** | Unknown: **0**

| Skill ID | Skill Name | Author | Origin | License | Approval Category | Commercial Permitted |
|---|---|---|---|---|---|:---:|
| `analytics-performance` | Analytics & Performance Marketing | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `business-opportunity-discovery` | Business Opportunity Discovery | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `buyer-persona` | Buyer Persona Development | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `competitor-intelligence` | Competitor Intelligence & Teardown | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `content-marketing` | Content Marketing & Authority Building | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `conversion-rate-optimization` | Conversion Rate Optimization (CRO) | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `customer-research` | Customer Research & JTBD | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `customer-segmentation` | Customer Segmentation | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `go-to-market-strategy` | Go-To-Market (GTM) Strategy | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `ideal-customer-profile` | Ideal Customer Profile (ICP) | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `industry-analysis` | Industry & Macro Analysis | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `keyword-research` | Keyword & Intent Research | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `market-research` | Market Research & Sizing | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `marketing-psychology` | Marketing Psychology & Copywriting | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `paid-advertising` | Paid Advertising & Acquisition | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `pricing-strategy` | Pricing Strategy & Monetization | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `product-marketing` | Product Marketing & Messaging | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `prospect-research` | High-Value Prospect Research | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `sales-strategy` | Sales Strategy & Outbound Systems | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `seo-geo` | SEO & Generative Engine Optimization | naznazj | INTERNAL | MIT | **APPROVED** | Yes |
| `social-media-marketing` | Social Media Marketing | naznazj | INTERNAL | MIT | **APPROVED** | Yes |

---

## 4. Attribution Notices & Provenance

### Core STRATIFY Skills (21 Built-In Skills)
All 21 skills located in `skills/` were independently authored for the STRATIFY project:
```text
Copyright (c) 2026 naznazj
Licensed under the MIT License.
Repository: https://github.com/naznazj/Stratify
```
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the MIT License.

---

## 5. Marketplace Compliance Checklist (Agensi.io / Agent Hubs)

Before publishing STRATIFY bundles to third-party marketplaces (such as **Agensi.io**, Cursor Directory, or Antigravity Plugin Marketplaces):

- [x] All 21 core skills verified with valid `APPROVED` commercial license records.
- [x] No `UNKNOWN` or unlicensed skill folders present in `skills/`.
- [x] No copyleft-contaminated components (GPL) bundling into proprietary runtime distributions.
- [x] Original copyright notice (`Copyright (c) 2026 naznazj`) present in root `LICENSE`.
- [x] `THIRD_PARTY_LICENSES.md` generated and updated.
- [x] Dynamic routing telemetry and runtime validation checks active.

---

## 6. How to Submit External Skills for Integration

Third-party skill authors wishing to integrate with STRATIFY must submit:
1. Full author name and organization.
2. Link to official upstream Git repository.
3. Open-source license (must be an SPDX-recognized permissive license, e.g., MIT, Apache-2.0, or BSD).
4. Explicit consent for commercial redistribution via `stratify-ai` npm package and Agensi.io marketplace.
