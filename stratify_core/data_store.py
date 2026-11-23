"""
STRATIFY Data Store
Persistent SQLite database management for:
- Research reports (full JSON, metadata, scores, timestamps)
- User history & session logs
- Industry comparison snapshots
- Custom opportunity scoring weights
"""
import sqlite3
import json
import os
import time
from typing import Dict, Any, List, Optional

class StratifyDataStore:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "stratify.db")
        else:
            self.db_path = db_path
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Reports table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                command TEXT NOT NULL,
                industry TEXT NOT NULL,
                industry_key TEXT NOT NULL,
                location TEXT NOT NULL,
                depth TEXT NOT NULL,
                top_opportunity_score REAL,
                total_tokens INTEGER,
                tokens_saved INTEGER,
                cost_usd REAL,
                created_at REAL NOT NULL,
                report_json TEXT NOT NULL
            )
            """)
            # Comparison table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparisons (
                id TEXT PRIMARY KEY,
                industry_1 TEXT NOT NULL,
                industry_2 TEXT NOT NULL,
                created_at REAL NOT NULL,
                comparison_json TEXT NOT NULL
            )
            """)
            # User preferences / scoring weights
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """)
            conn.commit()

    def save_report(self, report_data: Dict[str, Any]) -> str:
        report_id = report_data.get("report_id", f"rep_{int(time.time()*1000)}")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO reports (
                id, command, industry, industry_key, location, depth,
                top_opportunity_score, total_tokens, tokens_saved, cost_usd,
                created_at, report_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                report_id,
                report_data.get("command", ""),
                report_data.get("industry", ""),
                report_data.get("industry_key", ""),
                report_data.get("location", ""),
                report_data.get("depth", "standard"),
                report_data.get("top_opportunity_score", 0.0),
                report_data.get("token_metrics", {}).get("total_tokens", 0),
                report_data.get("token_metrics", {}).get("tokens_saved_by_routing", 0),
                report_data.get("token_metrics", {}).get("estimated_total_cost_usd", 0.0),
                time.time(),
                json.dumps(report_data)
            ))
            conn.commit()
        return report_id

    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT report_json FROM reports WHERE id = ?", (report_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row["report_json"])
        return None

    def list_reports(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, command, industry, industry_key, location, depth,
                   top_opportunity_score, total_tokens, tokens_saved, cost_usd, created_at
            FROM reports
            ORDER BY created_at DESC
            LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def delete_report(self, report_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
            conn.commit()
            return cursor.rowcount > 0

    def save_comparison(self, comp_id: str, ind1: str, ind2: str, data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO comparisons (id, industry_1, industry_2, created_at, comparison_json)
            VALUES (?, ?, ?, ?, ?)
            """, (comp_id, ind1, ind2, time.time(), json.dumps(data)))
            conn.commit()

    def get_setting(self, key: str, default: Any = None) -> Any:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row["value"])
        return default

    def set_setting(self, key: str, value: Any):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, json.dumps(value)))
            conn.commit()
