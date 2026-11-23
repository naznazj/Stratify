"""
Test Suite for STRATIFY Intellectual Property & License Compliance System
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stratify_core.license_compliance import (
    LicenseComplianceRegistry,
    ApprovalCategory,
    SkillLicenseRecord
)

class TestLicenseCompliance(unittest.TestCase):
    def setUp(self):
        self.registry = LicenseComplianceRegistry()

    def test_01_core_catalog_initialized_as_approved(self):
        """Verifies all 21 core skills are independently developed and APPROVED under MIT."""
        records = self.registry.list_records()
        self.assertEqual(len(records), 21)
        for r in records:
            self.assertEqual(r.author, "naznazj")
            self.assertEqual(r.license_type, "MIT")
            self.assertEqual(r.approval_category, ApprovalCategory.APPROVED)
            self.assertTrue(r.commercial_use_permitted)
            self.assertIn("naznazj", r.attribution_notice)

    def test_02_license_evaluation_logic(self):
        """Verifies license string evaluation across all approval categories."""
        # APPROVED: MIT, Apache, BSD
        cat, comm, _, _ = self.registry.evaluate_license("MIT")
        self.assertEqual(cat, ApprovalCategory.APPROVED)
        self.assertTrue(comm)

        cat, comm, _, _ = self.registry.evaluate_license("Apache-2.0")
        self.assertEqual(cat, ApprovalCategory.APPROVED)
        self.assertTrue(comm)

        # CONDITIONAL: CC-BY-SA, LGPL
        cat, comm, src_req, _ = self.registry.evaluate_license("CC-BY-SA-4.0")
        self.assertEqual(cat, ApprovalCategory.CONDITIONAL)
        self.assertTrue(src_req)

        # RESTRICTED: GPL, CC-BY-NC
        cat, comm, _, _ = self.registry.evaluate_license("GPL-3.0")
        self.assertEqual(cat, ApprovalCategory.RESTRICTED)

        cat, comm, _, _ = self.registry.evaluate_license("CC-BY-NC-4.0")
        self.assertEqual(cat, ApprovalCategory.RESTRICTED)
        self.assertFalse(comm)

        # UNKNOWN: Unrecognized or unlicensed
        cat, comm, _, _ = self.registry.evaluate_license("SomeCustomNonStandardThing")
        self.assertEqual(cat, ApprovalCategory.UNKNOWN)
        self.assertFalse(comm)

    def test_03_third_party_skill_intake_validation(self):
        """Tests the 7-step intake validator for third-party skills."""
        # 1. Permissive external skill
        rec = self.registry.validate_third_party_skill(
            skill_id="community-lead-scraper",
            skill_name="Community Lead Scraper",
            author="DevJane",
            repository_url="https://github.com/devjane/lead-scraper",
            license_type="MIT"
        )
        self.assertEqual(rec.approval_category, ApprovalCategory.APPROVED)
        self.assertTrue(rec.commercial_use_permitted)
        self.assertIn("DevJane", rec.attribution_notice)

        # 2. Incomplete provenance (missing author or repo) -> UNKNOWN
        rec_bad = self.registry.validate_third_party_skill(
            skill_id="anonymous-skill",
            skill_name="Anonymous Skill",
            author="",
            repository_url="",
            license_type="MIT"
        )
        self.assertEqual(rec_bad.approval_category, ApprovalCategory.UNKNOWN)

    def test_04_execution_guardrails(self):
        """Verifies policy enforcement blocks RESTRICTED and UNKNOWN skills from running."""
        # Built-in approved skill can execute
        can_run, _ = self.registry.is_skill_executable("market-research")
        self.assertTrue(can_run)

        # Register a restricted skill
        self.registry.validate_third_party_skill(
            skill_id="gpl-skill",
            skill_name="GPL Copyleft Skill",
            author="CopyleftOrg",
            repository_url="https://github.com/copyleft/skill",
            license_type="GPL-3.0"
        )
        can_run_gpl, msg = self.registry.is_skill_executable("gpl-skill")
        self.assertFalse(can_run_gpl)
        self.assertIn("RESTRICTED", msg)

        # Non-registered skill is blocked
        can_run_unregistered, _ = self.registry.is_skill_executable("non-existent-skill")
        self.assertFalse(can_run_unregistered)

    def test_05_marketplace_readiness_audit(self):
        """Verifies marketplace audit passes for core catalog and flags non-compliant components."""
        audit = self.registry.audit_registry()
        self.assertTrue(audit.is_commercially_compliant)
        self.assertTrue(audit.marketplace_readiness["Agensi.io"])

        # Inject an unknown skill and re-audit
        self.registry.register_skill(SkillLicenseRecord(
            skill_id="unlicensed-tool",
            skill_name="Unlicensed Tool",
            author="Unknown",
            approval_category=ApprovalCategory.UNKNOWN,
            commercial_use_permitted=False
        ))
        tainted_audit = self.registry.audit_registry()
        self.assertFalse(tainted_audit.is_commercially_compliant)
        self.assertFalse(tainted_audit.marketplace_readiness["Agensi.io"])
        self.assertGreaterEqual(len(tainted_audit.issues), 1)

    def test_06_markdown_registry_generation(self):
        """Verifies THIRD_PARTY_LICENSES.md generation contains required sections."""
        md_text = self.registry.generate_third_party_licenses_md()
        self.assertIn("# THIRD-PARTY INTELLECTUAL PROPERTY & LICENSE REGISTRY", md_text)
        self.assertIn("Agensi.io", md_text)
        self.assertIn("naznazj", md_text)
        self.assertIn("APPROVED", md_text)
        self.assertIn("market-research", md_text)

if __name__ == "__main__":
    unittest.main()
