"""
STRATIFY Dynamic Skill Router
Selects only necessary skills matching the identified industry, research depth, and task requirements.
Guarantees:
- Never loads all skills indiscriminately.
- Avoids duplicate skill execution.
- Calculates tokens saved by skipping irrelevant skills.
- Tracks skill execution metrics.
"""
from typing import Dict, Any, List, Set, Tuple
from pydantic import BaseModel, Field
from stratify_core.skill_discovery import SkillDiscovery, SkillMetadata
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand

class RoutedSkill(BaseModel):
    id: str
    name: str
    category: str
    token_weight: int
    selection_reason: str
    priority: int  # 1 = critical, 2 = supporting

class SkillRoutingPlan(BaseModel):
    selected_skills: List[RoutedSkill]
    skipped_skills: List[str]
    total_skills_available: int
    selected_count: int
    total_token_weight_selected: int
    total_token_weight_saved: int
    efficiency_percentage: float

class DynamicSkillRouter:
    def __init__(self, discovery: SkillDiscovery):
        self.discovery = discovery

    def route_skills(self, command: StratifyCommand, profile: IndustryProfile) -> SkillRoutingPlan:
        all_skills = self.discovery.discover_skills()
        total_available = len(all_skills)
        total_catalog_weight = sum(s.token_weight for s in all_skills.values())

        selected_skills: List[RoutedSkill] = []
        selected_ids: Set[str] = set()

        # Handle targeted sub-commands first
        if command.action == "competitors":
            target_ids = [("competitor-intelligence", 1, "Direct competitor teardown & pricing benchmark"),
                          ("pricing-strategy", 2, "Competitor pricing structure analysis")]
            self._add_skills_by_id(target_ids, all_skills, selected_skills, selected_ids)
            return self._build_plan(all_skills, selected_skills, total_catalog_weight)

        elif command.action == "expand_opportunities":
            target_ids = [("business-opportunity-discovery", 1, "Deep opportunity synthesis & gap analysis"),
                          ("market-research", 2, "Demand validation for proposed concepts"),
                          ("pricing-strategy", 2, "Monetization modeling")]
            self._add_skills_by_id(target_ids, all_skills, selected_skills, selected_ids)
            return self._build_plan(all_skills, selected_skills, total_catalog_weight)

        elif command.action == "find_prospects":
            target_ids = [("prospect-research", 1, "Verified company & decision-maker discovery"),
                          ("ideal-customer-profile", 1, "Target account qualification criteria"),
                          ("sales-strategy", 2, "Outreach angle formulation")]
            self._add_skills_by_id(target_ids, all_skills, selected_skills, selected_ids)
            return self._build_plan(all_skills, selected_skills, total_catalog_weight)

        elif command.action == "marketing_strategy":
            target_ids = [("go-to-market-strategy", 1, "Core launch & positioning blueprint"),
                          ("seo-geo", 1, "Search engine & Generative AI engine visibility"),
                          ("content-marketing", 2, "Editorial & authority content pipeline"),
                          ("paid-advertising", 2, "Paid acquisition & CAC optimization"),
                          ("social-media-marketing", 2, "Audience engagement channels")]
            self._add_skills_by_id(target_ids, all_skills, selected_skills, selected_ids)
            return self._build_plan(all_skills, selected_skills, total_catalog_weight)

        # Full research: Determine based on research depth and industry affinity
        depth = command.depth.lower()

        # Core anchor skills required for any credible business strategy
        anchor_skills = [
            ("market-research", 1, "Quantitative market sizing and macro trend evaluation"),
            ("business-opportunity-discovery", 1, "High-yield business concept formulation"),
            ("competitor-intelligence", 1, "Competitive landscape and gap identification")
        ]
        self._add_skills_by_id(anchor_skills, all_skills, selected_skills, selected_ids)

        # Depth: Quick -> Adds customer segmentation & GTM basics (total ~5-6)
        if depth == "quick":
            quick_skills = [
                ("customer-segmentation", 1, "High-level customer categorization"),
                ("go-to-market-strategy", 2, "Foundational market entry trajectory")
            ]
            self._add_skills_by_id(quick_skills, all_skills, selected_skills, selected_ids)

        # Depth: Standard -> Adds customer intelligence, real prospects, GTM, SEO/GEO (total ~9-11)
        elif depth == "standard":
            standard_skills = [
                ("customer-segmentation", 1, "Customer tier and purchasing power analysis"),
                ("buyer-persona", 2, "Decision-maker archetype and pain points"),
                ("prospect-research", 1, "Verified target company identification"),
                ("go-to-market-strategy", 1, "Multi-phase launch and distribution strategy"),
                ("seo-geo", 2, "AI Search and algorithmic ranking opportunities"),
                ("pricing-strategy", 2, "Monetization and unit economics modeling")
            ]
            self._add_skills_by_id(standard_skills, all_skills, selected_skills, selected_ids)

            # Industry-specific bonus skill
            if profile.industry_key in ["ecommerce", "digital_marketing"]:
                self._add_skills_by_id([("conversion-rate-optimization", 2, "E-commerce conversion funnel optimization")],
                                       all_skills, selected_skills, selected_ids)
            elif profile.industry_key in ["healthcare", "automotive", "construction"]:
                self._add_skills_by_id([("industry-analysis", 2, "Regulatory and supply chain constraints")],
                                       all_skills, selected_skills, selected_ids)
            elif profile.industry_key in ["saas", "financial_services"]:
                self._add_skills_by_id([("sales-strategy", 2, "Enterprise B2B qualification and sales motion")],
                                       all_skills, selected_skills, selected_ids)

        # Depth: Deep -> Adds comprehensive multi-agent skill suite (total ~14-16)
        else: # deep
            deep_skills = [
                ("industry-analysis", 1, "Structural value chain and regulatory barriers"),
                ("customer-research", 1, "Jobs-to-be-Done (JTBD) and behavioral pains"),
                ("customer-segmentation", 1, "Segment purchasing power indexing"),
                ("ideal-customer-profile", 1, "Firmographic and technographic ICP qualification"),
                ("buyer-persona", 2, "Multi-stakeholder persona profiling"),
                ("prospect-research", 1, "Deep verified account discovery and buying signals"),
                ("product-marketing", 2, "Value proposition narrative and positioning"),
                ("pricing-strategy", 1, "Tiered pricing architecture and margin targets"),
                ("go-to-market-strategy", 1, "90-day actionable milestone roadmap"),
                ("sales-strategy", 2, "Outbound cadence and enterprise objection handling"),
                ("seo-geo", 2, "Generative Engine Optimization (ChatGPT/Perplexity/Gemini)"),
                ("content-marketing", 2, "Authority content funnel creation"),
                ("paid-advertising", 2, "Paid media acquisition unit economics (CAC/ROAS)"),
                ("analytics-performance", 2, "North Star metrics and attribution telemetry")
            ]
            self._add_skills_by_id(deep_skills, all_skills, selected_skills, selected_ids)

        return self._build_plan(all_skills, selected_skills, total_catalog_weight)

    def _add_skills_by_id(self, targets: List[Tuple[str, int, str]], all_skills: Dict[str, SkillMetadata],
                          selected_skills: List[RoutedSkill], selected_ids: Set[str]):
        for skill_id, priority, reason in targets:
            if skill_id in all_skills and skill_id not in selected_ids:
                meta = all_skills[skill_id]
                selected_skills.append(RoutedSkill(
                    id=meta.id,
                    name=meta.name,
                    category=meta.category,
                    token_weight=meta.token_weight,
                    selection_reason=reason,
                    priority=priority
                ))
                selected_ids.add(skill_id)

    def _build_plan(self, all_skills: Dict[str, SkillMetadata], selected_skills: List[RoutedSkill], total_catalog_weight: int) -> SkillRoutingPlan:
        selected_ids = {s.id for s in selected_skills}
        skipped_ids = [sid for sid in all_skills.keys() if sid not in selected_ids]
        
        selected_weight = sum(s.token_weight for s in selected_skills)
        saved_weight = max(0, total_catalog_weight - selected_weight)
        efficiency = (saved_weight / total_catalog_weight * 100.0) if total_catalog_weight > 0 else 0.0

        return SkillRoutingPlan(
            selected_skills=selected_skills,
            skipped_skills=skipped_ids,
            total_skills_available=len(all_skills),
            selected_count=len(selected_skills),
            total_token_weight_selected=selected_weight,
            total_token_weight_saved=saved_weight,
            efficiency_percentage=round(efficiency, 1)
        )
