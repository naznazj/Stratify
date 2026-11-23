"""
STRATIFY Central Research Orchestrator
Coordinates the 7 specialized AI agents, dynamic skill router, scoring engine,
token tracker, and verification service across the complete 7-step STRATIFY workflow.
"""
import uuid
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from stratify_core.command_parser import parse_stratify_command, StratifyCommand
from stratify_core.industry_classifier import IndustryClassifier, IndustryProfile
from stratify_core.skill_discovery import SkillDiscovery
from stratify_core.skill_router import DynamicSkillRouter, SkillRoutingPlan
from stratify_core.token_tracker import TokenTracker
from stratify_core.scoring_engine import OpportunityScoringEngine
from stratify_core.verification_service import VerificationService
from stratify_core.data_store import StratifyDataStore

from stratify_core.agents.market_intel_agent import MarketIntelligenceAgent
from stratify_core.agents.competitor_agent import CompetitorIntelligenceAgent
from stratify_core.agents.customer_intel_agent import CustomerIntelligenceAgent
from stratify_core.agents.opportunity_agent import BusinessOpportunityAgent
from stratify_core.agents.prospect_agent import HighValueProspectAgent
from stratify_core.agents.marketing_agent import MarketingStrategistAgent
from stratify_core.agents.strategy_agent import BusinessStrategyAgent

class StratifyOrchestrator:
    def __init__(self, data_store: Optional[StratifyDataStore] = None):
        self.data_store = data_store if data_store else StratifyDataStore()
        self.classifier = IndustryClassifier()
        self.discovery = SkillDiscovery()
        self.router = DynamicSkillRouter(self.discovery)

    def execute_command(self, raw_command: str) -> Dict[str, Any]:
        """Main entry point: parses command and runs appropriate research workflow."""
        command = parse_stratify_command(raw_command)

        # Handle Comparison Workflow: /stratify compare X vs Y
        if command.action == "compare" and command.target_industry_2:
            return self._run_comparison(command)

        # Handle Sub-Commands or Full Research
        return self._run_research_workflow(command)

    def _run_research_workflow(self, command: StratifyCommand) -> Dict[str, Any]:
        session_id = f"stratify_{uuid.uuid4().hex[:10]}"
        start_time = time.time()

        # Step 1: Industry Identification
        profile = self.classifier.classify(command.industry, command.location)

        # Dynamic Skill Routing & Token Savings Calculation
        routing_plan = self.router.route_skills(command, profile)

        # Initialize Token Tracking & Verification Service
        token_tracker = TokenTracker(session_id=session_id, token_budget=command.token_budget)
        token_tracker.record_routing_savings(
            saved_tokens=routing_plan.total_token_weight_saved,
            active_skills_count=routing_plan.selected_count
        )
        verification_service = VerificationService()

        # Configure Opportunity Scoring Engine (loads custom weights if saved)
        custom_weights = self.data_store.get_setting("scoring_weights", None)
        scoring_engine = OpportunityScoringEngine(custom_weights)

        # Initialize Agents
        market_agent = MarketIntelligenceAgent(token_tracker, verification_service)
        competitor_agent = CompetitorIntelligenceAgent(token_tracker, verification_service)
        customer_agent = CustomerIntelligenceAgent(token_tracker, verification_service)
        opportunity_agent = BusinessOpportunityAgent(token_tracker, verification_service, scoring_engine)
        prospect_agent = HighValueProspectAgent(token_tracker, verification_service)
        marketing_agent = MarketingStrategistAgent(token_tracker, verification_service)
        strategy_agent = BusinessStrategyAgent(token_tracker, verification_service)

        shared_context: Dict[str, Any] = {
            "profile": profile.model_dump(),
            "command": command.model_dump(),
            "routing_plan": routing_plan.model_dump()
        }

        # Step 2: Market Research (Agent 1)
        market_res = market_agent.execute(command, profile, shared_context)
        shared_context["market_intel"] = market_res

        # Step 3: Customer Discovery (Agent 3)
        customer_res = customer_agent.execute(command, profile, shared_context)
        shared_context["customer_intel"] = customer_res

        # Step 4: Business Opportunity Discovery (Agent 4)
        opportunity_res = opportunity_agent.execute(command, profile, shared_context)
        shared_context["opportunities"] = opportunity_res

        # Step 5: High-Value Target Discovery (Agent 6)
        prospect_res = prospect_agent.execute(command, profile, shared_context)
        shared_context["prospects"] = prospect_res

        # Step 6: Competitor Analysis (Agent 2)
        competitor_res = competitor_agent.execute(command, profile, shared_context)
        shared_context["competitor_intel"] = competitor_res

        # Step 7: Marketing Strategy & Strategic Action Plan (Agents 5 & 7)
        marketing_res = marketing_agent.execute(command, profile, shared_context)
        strategy_res = strategy_agent.execute(command, profile, shared_context)

        # Consolidate Findings & Metrics
        token_summary = token_tracker.get_summary()
        credibility_summary = verification_service.get_credibility_summary()
        citations_list = [c.model_dump() for c in verification_service.list_citations()]

        execution_duration = round(time.time() - start_time, 2)
        top_score = opportunity_res["opportunities"][0]["overall_score"] if opportunity_res["opportunities"] else 0.0

        report = {
            "report_id": session_id,
            "command": command.raw_command,
            "action": command.action,
            "industry": profile.display_name,
            "industry_key": profile.industry_key,
            "location": profile.geographic_market,
            "is_default_location": command.location is None,
            "depth": command.depth,
            "execution_duration_sec": execution_duration,
            "created_at": time.time(),
            "top_opportunity_score": top_score,

            # Section A: Market Overview
            "market_overview": market_res,

            # Section B: Business Opportunities
            "opportunities": opportunity_res["opportunities"],
            "top_ranked_opportunity": opportunity_res.get("top_ranked_opportunity"),

            # Section C: Customer Intelligence
            "customer_intelligence": customer_res,

            # Section D: High-Value Targets
            "prospects": prospect_res["prospects"],

            # Section E: Competitor Intelligence
            "competitor_intelligence": competitor_res,

            # Section F: Marketing Strategy
            "marketing_strategy": marketing_res,

            # Section G: Strategic Action Plan & Business Model
            "business_strategy": strategy_res,

            # Skill Routing & Optimization telemetry
            "skill_routing": routing_plan.model_dump(),

            # Token Tracking & Performance Metrics
            "token_metrics": token_summary,

            # Research Verification & Citations
            "citations": citations_list,
            "credibility_metrics": credibility_summary
        }

        # Persist report to database
        self.data_store.save_report(report)

        return report

    def _run_comparison(self, command: StratifyCommand) -> Dict[str, Any]:
        """Runs side-by-side research comparing two industries."""
        comp_id = f"cmp_{uuid.uuid4().hex[:10]}"
        
        cmd1 = StratifyCommand(
            raw_command=f"/stratify {command.industry}",
            action="full_research",
            industry=command.industry,
            location=command.location,
            depth=command.depth
        )
        cmd2 = StratifyCommand(
            raw_command=f"/stratify {command.target_industry_2}",
            action="full_research",
            industry=command.target_industry_2 or "Wellness",
            location=command.location,
            depth=command.depth
        )

        res1 = self._run_research_workflow(cmd1)
        res2 = self._run_research_workflow(cmd2)

        comparison_payload = {
            "comparison_id": comp_id,
            "industry_1_name": res1["industry"],
            "industry_2_name": res2["industry"],
            "location": res1["location"],
            "industry_1": {
                "name": res1["industry"],
                "tam": res1["market_overview"]["tam"],
                "cagr": res1["market_overview"]["cagr"],
                "top_opportunity_score": res1["top_opportunity_score"],
                "top_opportunity_name": res1["top_ranked_opportunity"],
                "prospects_count": len(res1["prospects"]),
                "competitors_count": len(res1["competitor_intelligence"]["competitors"]),
                "report_id": res1["report_id"]
            },
            "industry_2": {
                "name": res2["industry"],
                "tam": res2["market_overview"]["tam"],
                "cagr": res2["market_overview"]["cagr"],
                "top_opportunity_score": res2["top_opportunity_score"],
                "top_opportunity_name": res2["top_ranked_opportunity"],
                "prospects_count": len(res2["prospects"]),
                "competitors_count": len(res2["competitor_intelligence"]["competitors"]),
                "report_id": res2["report_id"]
            },
            "winner_summary": f"{res1['industry'] if res1['top_opportunity_score'] >= res2['top_opportunity_score'] else res2['industry']} leads in opportunity score ({max(res1['top_opportunity_score'], res2['top_opportunity_score']):.1f} vs {min(res1['top_opportunity_score'], res2['top_opportunity_score']):.1f}).",
            "created_at": time.time()
        }

        self.data_store.save_comparison(comp_id, res1["industry"], res2["industry"], comparison_payload)
        return comparison_payload
