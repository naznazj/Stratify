"""
API Endpoints Test Suite for STRATIFY Web Server
Direct invocation test suite avoiding Starlette AnyIO portal IPC deadlocks on Windows sandbox.
"""
import unittest
import os
import sys
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server import (
    app,
    serve_dashboard,
    run_stratify,
    get_history,
    get_report,
    delete_report,
    compare_industries,
    list_skills,
    get_license_compliance,
    get_weights,
    update_weights,
    export_report,
    RunRequest,
    CompareRequest,
    WeightUpdateRequest
)

def resolve(coro):
    """Executes a synchronous async def coroutine directly without spawning an event loop."""
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value
    raise RuntimeError("Coroutine did not complete synchronously")

class DummyClient:
    host = "127.0.0.1"

class DummyRequest:
    client = DummyClient()

class TestServerEndpoints(unittest.TestCase):
    def test_01_serve_dashboard(self):
        """Verifies dashboard HTML serving."""
        html = resolve(serve_dashboard())
        self.assertIn("STRATIFY", html)
        self.assertIn("Business Intelligence & Strategic Marketing Engine", html)

    def test_02_run_api(self):
        """Verifies research execution and report retrieval."""
        req = RunRequest(industry="Healthcare", location="Philippines", depth="standard")
        res = resolve(run_stratify(req, DummyRequest()))
        self.assertTrue(res["success"])
        report = res["report"]
        self.assertEqual(report["industry"], "Healthcare & Life Sciences")
        self.assertEqual(report["location"], "Philippines")
        self.assertGreaterEqual(len(report["opportunities"]), 5)
        self.assertIn("report_id", report)

        rep_id = report["report_id"]

        # History
        hist = resolve(get_history(limit=50))
        self.assertTrue(any(r["id"] == rep_id for r in hist["reports"]))

        # Report retrieval
        rep = resolve(get_report(report_id=rep_id))
        self.assertEqual(rep["report"]["report_id"], rep_id)

        # Markdown Export
        exp_md = resolve(export_report(report_id=rep_id, format="markdown"))
        self.assertIn(b"# STRATIFY Research Report", exp_md.body)

        # JSON Export
        exp_json = resolve(export_report(report_id=rep_id, format="json"))
        self.assertIn(b"Healthcare & Life Sciences", exp_json.body)

    def test_03_compare_api(self):
        """Verifies compare API endpoint."""
        req = CompareRequest(
            industry_1="Healthcare",
            industry_2="Real Estate",
            location="Philippines",
            depth="standard"
        )
        res = resolve(compare_industries(req, DummyRequest()))
        self.assertTrue(res["success"])
        self.assertIn("comparison_id", res["comparison"])
        self.assertIn("winner_summary", res["comparison"])

    def test_04_skills_endpoint(self):
        """Verifies skills catalog endpoint."""
        res = resolve(list_skills())
        skills = res["skills"]
        self.assertGreaterEqual(len(skills), 21)

    def test_05_weights_config(self):
        """Verifies scoring weights get and update."""
        get_res = resolve(get_weights())
        self.assertIn("market_demand", get_res["weights"])

        update_req = WeightUpdateRequest(
            market_demand=0.30,
            revenue_potential=0.30,
            purchasing_power=0.20,
            competitive_opportunity=0.10,
            execution_feasibility=0.10
        )
        post_res = resolve(update_weights(update_req))
        self.assertTrue(post_res["success"])
        self.assertEqual(post_res["weights"]["market_demand"], 0.30)

    def test_06_input_validation_and_security(self):
        """Verifies strict input bounds and Pydantic validation."""
        # Test out-of-bounds depth
        with self.assertRaises(ValidationError):
            RunRequest(depth="invalid_depth_value")

        # Test out-of-bounds token budget
        with self.assertRaises(ValidationError):
            RunRequest(token_budget=50)  # ge=100

        # Test empty industry names in compare
        with self.assertRaises(ValidationError):
            CompareRequest(industry_1="", industry_2="Real Estate")

        # Test weights exceeding 1.0
        with self.assertRaises(ValidationError):
            WeightUpdateRequest(market_demand=1.5)

    def test_07_compliance_endpoint(self):
        """Verifies /api/compliance endpoint."""
        res = resolve(get_license_compliance())
        self.assertTrue(res["success"])
        self.assertTrue(res["audit"]["is_commercially_compliant"])
        self.assertEqual(len(res["records"]), 21)
        self.assertTrue(res["audit"]["marketplace_readiness"]["Agensi.io"])

if __name__ == "__main__":
    unittest.main()
