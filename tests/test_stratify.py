"""
STRATIFY Automated Verification & Test Suite
Tests all 5 primary industries: Healthcare, Real Estate, Automotive, E-commerce, SaaS.
Tests dynamic skill discovery, dynamic routing, token accounting, scoring engine,
source verification, and all sub-commands.
"""
import unittest
import os
import sys

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stratify_core.command_parser import parse_stratify_command
from stratify_core.industry_classifier import IndustryClassifier
from stratify_core.skill_discovery import SkillDiscovery
from stratify_core.skill_router import DynamicSkillRouter
from stratify_core.scoring_engine import OpportunityScoringEngine
from stratify_core.verification_service import VerificationService, FactClassification
from stratify_core.orchestrator import StratifyOrchestrator
from stratify_core.data_store import StratifyDataStore

class TestStratifyPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_store = StratifyDataStore()
        cls.orchestrator = StratifyOrchestrator(data_store=cls.data_store)
        cls.discovery = SkillDiscovery()
        cls.router = DynamicSkillRouter(cls.discovery)

    def test_01_skill_discovery(self):
        """Verifies that all 21 skills exist on disk and are parsed with frontmatter."""
        skills = self.discovery.discover_skills()
        self.assertGreaterEqual(len(skills), 21, "Expected at least 21 core skills")
        self.assertIn("market-research", skills)
        self.assertIn("competitor-intelligence", skills)
        self.assertIn("prospect-research", skills)
        self.assertIn("business-opportunity-discovery", skills)
        self.assertIn("go-to-market-strategy", skills)
        self.assertIn("seo-geo", skills)

        # Check instruction loader
        mr_text = self.discovery.load_skill_instructions("market-research")
        self.assertIsNotNone(mr_text)
        self.assertIn("TAM", mr_text)

    def test_02_dynamic_skill_routing_efficiency(self):
        """Verifies that the skill router selects only necessary skills and avoids loading all 21 skills."""
        classifier = IndustryClassifier()
        cmd_quick = parse_stratify_command("/stratify Healthcare --depth quick")
        profile = classifier.classify("Healthcare")
        plan_quick = self.router.route_skills(cmd_quick, profile)

        self.assertLess(plan_quick.selected_count, len(self.discovery.discover_skills()), "Quick depth should prune skills")
        self.assertGreater(plan_quick.total_token_weight_saved, 0, "Router should track token savings")
        self.assertGreater(plan_quick.efficiency_percentage, 50.0, "Quick depth should save >50% token weight")

    def test_03_healthcare_philippines(self):
        """Tests Healthcare research targeting the Philippines."""
        report = self.orchestrator.execute_command("/stratify Healthcare --location Philippines")
        self.assertEqual(report["industry"], "Healthcare & Life Sciences")
        self.assertEqual(report["location"], "Philippines")
        self.assertFalse(report["is_default_location"])
        self.assertGreaterEqual(len(report["opportunities"]), 5, "Should generate at least 5 opportunities")
        self.assertGreaterEqual(len(report["prospects"]), 3, "Should discover verified real prospects")
        self.assertTrue(any("Medical City" in p["company_name"] or "Luke" in p["company_name"] for p in report["prospects"]))
        self.assertGreaterEqual(len(report["citations"]), 4, "Should have verified citations")

    def test_04_real_estate(self):
        """Tests Real Estate research."""
        report = self.orchestrator.execute_command("/stratify Real Estate")
        self.assertEqual(report["industry"], "Real Estate & PropTech")
        self.assertTrue(report["is_default_location"])
        self.assertGreaterEqual(len(report["opportunities"]), 5)
        self.assertGreater(report["top_opportunity_score"], 80.0)

    def test_05_ecommerce(self):
        """Tests E-commerce research."""
        report = self.orchestrator.execute_command("/stratify E-commerce")
        self.assertEqual(report["industry"], "E-commerce & Direct-to-Consumer (D2C)")
        self.assertGreaterEqual(len(report["opportunities"]), 5)
        # Check channel rationale
        channels = [c["channel"] for c in report["marketing_strategy"]["recommended_channels"]]
        self.assertTrue(any("TikTok" in ch or "Meta" in ch for ch in channels))

    def test_06_automotive(self):
        """Tests Automotive research."""
        report = self.orchestrator.execute_command("/stratify Automotive")
        self.assertEqual(report["industry"], "Automotive & Mobility")
        self.assertGreaterEqual(len(report["competitor_intelligence"]["competitors"]), 3)

    def test_07_saas_technology(self):
        """Tests SaaS / Technology research."""
        report = self.orchestrator.execute_command("/stratify Technology and SaaS --depth deep")
        self.assertEqual(report["industry"], "Technology, Software & SaaS")
        self.assertEqual(report["depth"], "deep")
        self.assertGreaterEqual(report["skill_routing"]["selected_count"], 12, "Deep research activates comprehensive skill suite")

    def test_08_subcommands(self):
        """Tests all specialized sub-commands."""
        # 1. Expand opportunities
        rep_exp = self.orchestrator.execute_command("/stratify expand healthcare opportunities")
        self.assertEqual(rep_exp["action"], "expand_opportunities")

        # 2. Competitors
        rep_comp = self.orchestrator.execute_command("/stratify competitors in automotive")
        self.assertEqual(rep_comp["action"], "competitors")

        # 3. Find prospects
        rep_pros = self.orchestrator.execute_command("/stratify find high-value real estate clients")
        self.assertEqual(rep_pros["action"], "find_prospects")

        # 4. Marketing strategy
        rep_mkt = self.orchestrator.execute_command("/stratify marketing strategy for e-commerce")
        self.assertEqual(rep_mkt["action"], "marketing_strategy")

        # 5. Industry comparison
        rep_cmp = self.orchestrator.execute_command("/stratify compare Healthcare vs Real Estate")
        self.assertIn("comparison_id", rep_cmp)
        self.assertIn("winner_summary", rep_cmp)

    def test_09_scoring_engine_transparency(self):
        """Verifies opportunity scoring calculations and transparency."""
        engine = OpportunityScoringEngine()
        res = engine.score_opportunity(
            name="Test Concept",
            market_demand_val=90,
            market_demand_evidence="High search volume",
            revenue_potential_val=85,
            revenue_potential_evidence="SaaS pricing",
            purchasing_power_val=80,
            purchasing_power_evidence="Enterprise budget",
            competitive_opp_val=75,
            competitive_opp_evidence="Low competitor satisfaction",
            feasibility_val=80,
            feasibility_evidence="Existing APIs",
            confidence_rating=0.9
        )
        # Expected: 90*0.25 + 85*0.25 + 80*0.20 + 75*0.15 + 80*0.15 = 22.5 + 21.25 + 16.0 + 11.25 + 12.0 = 83.0
        self.assertAlmostEqual(res.overall_score, 83.0, places=1)
        self.assertEqual(len(res.dimensions), 5)
        self.assertIn("High", res.confidence_level)

    def test_10_datastore_persistence(self):
        """Verifies that reports and settings are saved and retrieved from SQLite."""
        report = self.orchestrator.execute_command("/stratify Financial Services --location Philippines")
        report_id = report["report_id"]
        saved = self.data_store.get_report(report_id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved["industry"], report["industry"])

if __name__ == "__main__":
    unittest.main()
