"""
API Endpoints Test Suite for STRATIFY Web Server
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from server import app

class TestServerEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_serve_dashboard(self):
        """Verifies GET / serves the HTML dashboard."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("STRATIFY", resp.text)
        self.assertIn("Business Intelligence & Strategic Marketing Engine", resp.text)

    def test_02_run_api(self):
        """Verifies POST /api/stratify/run generates research."""
        payload = {
            "industry": "Healthcare",
            "location": "Philippines",
            "depth": "standard"
        }
        resp = self.client.post("/api/stratify/run", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        report = data["report"]
        self.assertEqual(report["industry"], "Healthcare & Life Sciences")
        self.assertEqual(report["location"], "Philippines")
        self.assertGreaterEqual(len(report["opportunities"]), 5)
        self.assertIn("report_id", report)

        # Test history and report retrieval
        rep_id = report["report_id"]
        hist_resp = self.client.get("/api/stratify/history")
        self.assertEqual(hist_resp.status_code, 200)
        self.assertTrue(any(r["id"] == rep_id for r in hist_resp.json()["reports"]))

        get_resp = self.client.get(f"/api/stratify/report/{rep_id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["report"]["report_id"], rep_id)

        # Test export markdown
        exp_md = self.client.get(f"/api/stratify/export/{rep_id}?format=markdown")
        self.assertEqual(exp_md.status_code, 200)
        self.assertIn("# STRATIFY Research Report", exp_md.text)

        # Test export json
        exp_json = self.client.get(f"/api/stratify/export/{rep_id}?format=json")
        self.assertEqual(exp_json.status_code, 200)
        self.assertIn("Healthcare & Life Sciences", exp_json.text)

    def test_03_compare_api(self):
        """Verifies POST /api/stratify/compare compares two industries."""
        payload = {
            "industry_1": "Healthcare",
            "industry_2": "Real Estate",
            "location": "Philippines",
            "depth": "standard"
        }
        resp = self.client.post("/api/stratify/compare", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertIn("comparison_id", data["comparison"])
        self.assertIn("winner_summary", data["comparison"])

    def test_04_skills_endpoint(self):
        """Verifies GET /api/skills lists all installed core skills."""
        resp = self.client.get("/api/skills")
        self.assertEqual(resp.status_code, 200)
        skills = resp.json()["skills"]
        self.assertGreaterEqual(len(skills), 21)

    def test_05_weights_config(self):
        """Verifies GET and POST /api/config/weights."""
        get_resp = self.client.get("/api/config/weights")
        self.assertEqual(get_resp.status_code, 200)
        weights = get_resp.json()["weights"]
        self.assertIn("market_demand", weights)

        # Update weights
        new_weights = {
            "market_demand": 0.30,
            "revenue_potential": 0.30,
            "purchasing_power": 0.20,
            "competitive_opportunity": 0.10,
            "execution_feasibility": 0.10
        }
        post_resp = self.client.post("/api/config/weights", json=new_weights)
        self.assertEqual(post_resp.status_code, 200)
        self.assertTrue(post_resp.json()["success"])

if __name__ == "__main__":
    unittest.main()
