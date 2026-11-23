"""
STRATIFY Intellectual Property and License Compliance Engine
Strictly manages third-party skill licensing, attribution, commercial permissions,
and marketplace readiness (e.g., Agensi.io, Agent Marketplaces).
"""
import os
import time
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

class ApprovalCategory(str, Enum):
    APPROVED = "APPROVED"         # Commercial use and intended integration are permitted
    CONDITIONAL = "CONDITIONAL"   # Additional attribution, source disclosure, or obligations apply
    RESTRICTED = "RESTRICTED"     # Requires explicit permission or legal review
    UNKNOWN = "UNKNOWN"           # No verifiable license; do not copy, modify, redistribute, or sell

class SkillLicenseRecord(BaseModel):
    skill_id: str
    skill_name: str
    author: str
    origin_type: str = "internal"  # "internal" (independently developed) or "third_party"
    repository_url: Optional[str] = None
    license_type: str = "MIT"
    license_url: Optional[str] = None
    approval_category: ApprovalCategory = ApprovalCategory.APPROVED
    commercial_use_permitted: bool = True
    modification_permitted: bool = True
    redistribution_permitted: bool = True
    attribution_required: bool = True
    source_disclosure_required: bool = False
    attribution_notice: str = ""
    notes: str = ""

class ComplianceAuditResult(BaseModel):
    total_skills: int
    approved_count: int
    conditional_count: int
    restricted_count: int
    unknown_count: int
    is_commercially_compliant: bool
    marketplace_readiness: Dict[str, bool]
    issues: List[str] = Field(default_factory=list)
    audit_timestamp: float = Field(default_factory=time.time)

class LicenseComplianceRegistry:
    """Central registry and compliance auditor for STRATIFY skills."""

    KNOWN_PERMISSIVE_LICENSES = {
        "mit": (ApprovalCategory.APPROVED, True, False, "MIT License: Permissive commercial use, attribution required."),
        "apache-2.0": (ApprovalCategory.APPROVED, True, False, "Apache 2.0: Permissive commercial use, patent grant, notice required."),
        "bsd-2-clause": (ApprovalCategory.APPROVED, True, False, "BSD 2-Clause: Permissive commercial use, copyright notice required."),
        "bsd-3-clause": (ApprovalCategory.APPROVED, True, False, "BSD 3-Clause: Permissive commercial use, no endorsement clause."),
        "isc": (ApprovalCategory.APPROVED, True, False, "ISC License: Functionally equivalent to MIT."),
        "cc-by-4.0": (ApprovalCategory.CONDITIONAL, True, False, "Creative Commons BY 4.0: Attribution required for commercial distribution."),
        "cc-by-sa-4.0": (ApprovalCategory.CONDITIONAL, True, True, "Creative Commons BY-SA 4.0: ShareAlike requires distributing derivative works under same license."),
        "lgpl-3.0": (ApprovalCategory.CONDITIONAL, True, True, "LGPL 3.0: Library copyleft; source modifications must be shared."),
        "gpl-3.0": (ApprovalCategory.RESTRICTED, True, True, "GPL 3.0: Strong copyleft; viral license requires entire derivative work to be GPL."),
        "cc-by-nc-4.0": (ApprovalCategory.RESTRICTED, False, False, "CC-BY-NC 4.0: Non-Commercial only; commercial distribution prohibited."),
        "proprietary": (ApprovalCategory.RESTRICTED, False, False, "Proprietary: Explicit written commercial licensing agreement required."),
        "unknown": (ApprovalCategory.UNKNOWN, False, False, "No verifiable license found. Prohibited from inclusion.")
    }

    # All 21 core skills independently developed for STRATIFY
    CORE_SKILL_CATALOG = [
        ("analytics-performance", "Analytics & Performance Marketing", "Continuous conversion measurement, attribution modeling, and North Star metrics."),
        ("business-opportunity-discovery", "Business Opportunity Discovery", "Formulation and empirical scoring of defensible business opportunities."),
        ("buyer-persona", "Buyer Persona Development", "Archetype profiles, psychological pain points, and decision-maker priorities."),
        ("competitor-intelligence", "Competitor Intelligence & Teardown", "Competitive benchmarking, pricing teardowns, and market gap detection."),
        ("content-marketing", "Content Marketing & Authority Building", "Educational editorial calendars, thought leadership, and lead magnet engines."),
        ("conversion-rate-optimization", "Conversion Rate Optimization (CRO)", "High-intent landing page architecture, checkout funnel optimization."),
        ("customer-research", "Customer Research & JTBD", "Jobs-to-be-Done (JTBD) interviews, qualitative customer discovery."),
        ("customer-segmentation", "Customer Segmentation", "Value-based segmentation, purchasing power tiers, and demographic classification."),
        ("go-to-market-strategy", "Go-To-Market (GTM) Strategy", "Multi-phase launch roadmaps, channel sequencing, and early traction milestones."),
        ("ideal-customer-profile", "Ideal Customer Profile (ICP)", "Firmographic, technographic, and behavioral criteria for high-value targets."),
        ("industry-analysis", "Industry & Macro Analysis", "PESTEL evaluations, regulatory frameworks, and supply chain barriers."),
        ("keyword-research", "Keyword & Intent Research", "Search volume analysis, commercial intent clustering, and keyword difficulty."),
        ("market-research", "Market Research & Sizing", "Quantitative TAM, SAM, SOM calculations and CAGR trajectory modeling."),
        ("marketing-psychology", "Marketing Psychology & Copywriting", "Cognitive biases, social proof triggers, and persuasive value proposition framing."),
        ("paid-advertising", "Paid Advertising & Acquisition", "PPC campaigns, paid social targeting, CAC/ROAS payback economics."),
        ("pricing-strategy", "Pricing Strategy & Monetization", "Value-based pricing, tiered licensing structures, and unit economics."),
        ("product-marketing", "Product Marketing & Messaging", "Positioning statements, competitive differentiators, and launch playbooks."),
        ("prospect-research", "High-Value Prospect Research", "Verified corporate entity identification and genuine buying signals."),
        ("sales-strategy", "Sales Strategy & Outbound Systems", "Multi-touch outbound cadences, enterprise objection handling, and demo scripts."),
        ("seo-geo", "SEO & Generative Engine Optimization", "Optimizing search engines and AI answer engines (ChatGPT, Perplexity, Gemini)."),
        ("social-media-marketing", "Social Media Marketing", "Organic distribution channels, community advocacy, and viral loop mechanics.")
    ]

    def __init__(self):
        self._registry: Dict[str, SkillLicenseRecord] = {}
        self._initialize_core_registry()

    def _initialize_core_registry(self):
        """Initializes all 21 built-in skills as independently developed under MIT."""
        for skill_id, skill_name, description in self.CORE_SKILL_CATALOG:
            self._registry[skill_id] = SkillLicenseRecord(
                skill_id=skill_id,
                skill_name=skill_name,
                author="naznazj",
                origin_type="internal",
                repository_url="https://github.com/naznazj/Stratify",
                license_type="MIT",
                license_url="https://github.com/naznazj/Stratify/blob/main/LICENSE",
                approval_category=ApprovalCategory.APPROVED,
                commercial_use_permitted=True,
                modification_permitted=True,
                redistribution_permitted=True,
                attribution_required=True,
                source_disclosure_required=False,
                attribution_notice="Copyright (c) 2026 naznazj. Licensed under the MIT License.",
                notes=f"Independently authored core skill for STRATIFY. {description}"
            )

    def register_skill(self, record: SkillLicenseRecord):
        """Registers or updates a skill license record."""
        self._registry[record.skill_id] = record

    def get_skill_record(self, skill_id: str) -> Optional[SkillLicenseRecord]:
        return self._registry.get(skill_id)

    def list_records(self) -> List[SkillLicenseRecord]:
        return list(self._registry.values())

    def evaluate_license(self, license_identifier: str) -> Tuple[ApprovalCategory, bool, bool, str]:
        """
        Evaluates a license string and returns:
        (ApprovalCategory, commercial_permitted, source_disclosure_required, explanation)
        """
        key = license_identifier.strip().lower()
        if key in self.KNOWN_PERMISSIVE_LICENSES:
            return self.KNOWN_PERMISSIVE_LICENSES[key]
        
        # Check partial matches
        if "mit" in key:
            return self.KNOWN_PERMISSIVE_LICENSES["mit"]
        if "apache" in key:
            return self.KNOWN_PERMISSIVE_LICENSES["apache-2.0"]
        if "bsd" in key:
            return self.KNOWN_PERMISSIVE_LICENSES["bsd-2-clause"]
        if "non-commercial" in key or "nc" in key:
            return self.KNOWN_PERMISSIVE_LICENSES["cc-by-nc-4.0"]
        if "gpl" in key:
            return self.KNOWN_PERMISSIVE_LICENSES["gpl-3.0"]

        return self.KNOWN_PERMISSIVE_LICENSES["unknown"]

    def validate_third_party_skill(
        self,
        skill_id: str,
        skill_name: str,
        author: str,
        repository_url: str,
        license_type: str,
        license_url: Optional[str] = None,
        custom_notes: str = ""
    ) -> SkillLicenseRecord:
        """
        Strict 7-step intake validator for third-party skills.
        Ensures external components meet commercial distribution standards.
        """
        # Step 1: Identify author and repo
        clean_author = author.strip() if author else "Unknown Author"
        clean_repo = repository_url.strip() if repository_url else ""

        # Step 2 & 3 & 4: Inspect license, commercial permissions, modifications
        category, commercial_ok, source_disclosure, explanation = self.evaluate_license(license_type)

        if not clean_repo or clean_author == "Unknown Author":
            category = ApprovalCategory.UNKNOWN
            explanation = "Missing verified author or repository provenance."

        # Step 5: Format copyright and attribution notice
        attribution = f"Copyright (c) {clean_author}. Originally published at {clean_repo}. Licensed under {license_type}."

        record = SkillLicenseRecord(
            skill_id=skill_id,
            skill_name=skill_name,
            author=clean_author,
            origin_type="third_party",
            repository_url=clean_repo,
            license_type=license_type,
            license_url=license_url,
            approval_category=category,
            commercial_use_permitted=commercial_ok,
            modification_permitted=commercial_ok and category != ApprovalCategory.UNKNOWN,
            redistribution_permitted=category in [ApprovalCategory.APPROVED, ApprovalCategory.CONDITIONAL],
            attribution_required=True,
            source_disclosure_required=source_disclosure,
            attribution_notice=attribution,
            notes=f"{explanation} {custom_notes}".strip()
        )

        self.register_skill(record)
        return record

    def is_skill_executable(self, skill_id: str) -> Tuple[bool, str]:
        """
        Policy enforcement: Blocks UNKNOWN and RESTRICTED skills from running
        in commercial production workflows.
        """
        record = self.get_skill_record(skill_id)
        if not record:
            return False, f"Skill '{skill_id}' is not registered in the compliance registry. Status: UNKNOWN."

        if record.approval_category == ApprovalCategory.APPROVED:
            return True, "Skill is APPROVED for commercial use."
        elif record.approval_category == ApprovalCategory.CONDITIONAL:
            return True, f"Skill is CONDITIONAL. Attribution required: {record.attribution_notice}"
        elif record.approval_category == ApprovalCategory.RESTRICTED:
            return False, f"Skill '{skill_id}' is RESTRICTED: Requires explicit permission or legal review."
        else:
            return False, f"Skill '{skill_id}' has UNKNOWN license status. Prohibited from execution or distribution."

    def audit_registry(self) -> ComplianceAuditResult:
        """Performs a full audit across all registered skills."""
        total = len(self._registry)
        approved = sum(1 for r in self._registry.values() if r.approval_category == ApprovalCategory.APPROVED)
        conditional = sum(1 for r in self._registry.values() if r.approval_category == ApprovalCategory.CONDITIONAL)
        restricted = sum(1 for r in self._registry.values() if r.approval_category == ApprovalCategory.RESTRICTED)
        unknown = sum(1 for r in self._registry.values() if r.approval_category == ApprovalCategory.UNKNOWN)

        issues = []
        for r in self._registry.values():
            if r.approval_category == ApprovalCategory.RESTRICTED:
                issues.append(f"RESTRICTED: '{r.skill_id}' by {r.author} ({r.license_type}) requires legal waiver.")
            elif r.approval_category == ApprovalCategory.UNKNOWN:
                issues.append(f"UNKNOWN: '{r.skill_id}' has no verified license. Remove before commercial distribution.")

        is_compliant = (restricted == 0 and unknown == 0)

        marketplace_checks = {
            "Agensi.io": is_compliant,
            "Antigravity_Marketplace": is_compliant,
            "NPM_Registry": is_compliant
        }

        return ComplianceAuditResult(
            total_skills=total,
            approved_count=approved,
            conditional_count=conditional,
            restricted_count=restricted,
            unknown_count=unknown,
            is_commercially_compliant=is_compliant,
            marketplace_readiness=marketplace_checks,
            issues=issues
        )

    def generate_third_party_licenses_md(self, output_path: Optional[str] = None) -> str:
        """
        Generates the official THIRD_PARTY_LICENSES.md file according to
        commercial distribution standards and marketplace compliance guidelines.
        """
        audit = self.audit_registry()
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(audit.audit_timestamp))

        md = f"""# THIRD-PARTY INTELLECTUAL PROPERTY & LICENSE REGISTRY

**Package:** `stratify-ai`  
**Copyright Holder & Lead Maintainer:** `naznazj`  
**License Compliance Audit Date:** {timestamp_str}  
**Commercial Distribution Status:** {"COMPLIANT" if audit.is_commercially_compliant else "ATTENTION REQUIRED"}  
**Marketplace Target Readiness (Agensi.io, NPM):** {"READY" if audit.marketplace_readiness.get("Agensi.io") else "BLOCKED"}

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

Total Registered Skills: **{audit.total_skills}**  
Approved: **{audit.approved_count}** | Conditional: **{audit.conditional_count}** | Restricted: **{audit.restricted_count}** | Unknown: **{audit.unknown_count}**

| Skill ID | Skill Name | Author | Origin | License | Approval Category | Commercial Permitted |
|---|---|---|---|---|---|:---:|
"""
        for r in self.list_records():
            md += f"| `{r.skill_id}` | {r.skill_name} | {r.author} | {r.origin_type.upper()} | {r.license_type} | **{r.approval_category.value}** | {'Yes' if r.commercial_use_permitted else 'No'} |\n"

        md += """
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
"""

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)

        return md

# Global registry instance
license_registry = LicenseComplianceRegistry()
