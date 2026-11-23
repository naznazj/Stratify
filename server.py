"""
STRATIFY Web Server (FastAPI + Uvicorn)
Serves the STRATIFY SaaS Dashboard and REST API endpoints.
"""
import os
import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from stratify_core.orchestrator import StratifyOrchestrator
from stratify_core.command_parser import parse_stratify_command
from stratify_core.data_store import StratifyDataStore
from stratify_core.skill_discovery import SkillDiscovery

app = FastAPI(title="STRATIFY Business Intelligence & Strategic Marketing Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_store = StratifyDataStore()
orchestrator = StratifyOrchestrator(data_store=data_store)
discovery = SkillDiscovery()

class RunRequest(BaseModel):
    command: Optional[str] = Field(default=None, max_length=1000)
    industry: Optional[str] = Field(default=None, max_length=150)
    location: Optional[str] = Field(default=None, max_length=150)
    depth: str = Field(default="standard", pattern=r"^(quick|standard|deep)$")
    token_budget: Optional[int] = Field(default=None, ge=100, le=10_000_000)

class CompareRequest(BaseModel):
    industry_1: str = Field(max_length=150)
    industry_2: str = Field(max_length=150)
    location: Optional[str] = Field(default=None, max_length=150)
    depth: str = Field(default="standard", pattern=r"^(quick|standard|deep)$")

class WeightUpdateRequest(BaseModel):
    market_demand: float = Field(default=0.25, ge=0.0, le=1.0)
    revenue_potential: float = Field(default=0.25, ge=0.0, le=1.0)
    purchasing_power: float = Field(default=0.20, ge=0.0, le=1.0)
    competitive_opportunity: float = Field(default=0.15, ge=0.0, le=1.0)
    execution_feasibility: float = Field(default=0.15, ge=0.0, le=1.0)

@app.post("/api/stratify/run")
async def run_stratify(req: RunRequest):
    try:
        if req.command and req.command.strip():
            raw_cmd = req.command.strip()
        else:
            ind = req.industry if req.industry else "Technology and SaaS"
            loc_flag = f" --location {req.location}" if req.location else ""
            depth_flag = f" --depth {req.depth}" if req.depth else ""
            raw_cmd = f"/stratify {ind}{loc_flag}{depth_flag}"

        report = orchestrator.execute_command(raw_cmd)
        return {"success": True, "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stratify/history")
async def get_history(limit: int = 50):
    reports = data_store.list_reports(limit=limit)
    return {"reports": reports}

@app.get("/api/stratify/report/{report_id}")
async def get_report(report_id: str):
    report = data_store.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report": report}

@app.delete("/api/stratify/report/{report_id}")
async def delete_report(report_id: str):
    success = data_store.delete_report(report_id)
    return {"success": success}

@app.post("/api/stratify/compare")
async def compare_industries(req: CompareRequest):
    loc_flag = f" --location {req.location}" if req.location else ""
    cmd = f"/stratify compare {req.industry_1} vs {req.industry_2}{loc_flag} --depth {req.depth}"
    comparison = orchestrator.execute_command(cmd)
    return {"success": True, "comparison": comparison}

@app.get("/api/skills")
async def list_skills():
    skills = discovery.discover_skills()
    return {"skills": [s.model_dump() for s in skills.values()]}

@app.get("/api/config/weights")
async def get_weights():
    weights = data_store.get_setting("scoring_weights", {
        "market_demand": 0.25,
        "revenue_potential": 0.25,
        "purchasing_power": 0.20,
        "competitive_opportunity": 0.15,
        "execution_feasibility": 0.15
    })
    return {"weights": weights}

@app.post("/api/config/weights")
async def update_weights(req: WeightUpdateRequest):
    weights = req.model_dump()
    data_store.set_setting("scoring_weights", weights)
    return {"success": True, "weights": weights}

@app.get("/api/stratify/export/{report_id}")
async def export_report(report_id: str, format: str = "markdown"):
    report = data_store.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if format == "json":
        return Response(
            content=json_dumps(report),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=stratify_{report['industry_key']}.json"}
        )

    # Generate Markdown export
    md = f"""# STRATIFY Research Report: {report['industry']}
**Location:** {report['location']} | **Depth:** {report['depth'].upper()} | **Date:** {time.strftime('%Y-%m-%d', time.localtime(report['created_at']))}
**Top Opportunity Score:** {report['top_opportunity_score']}/100

---

## 1. Market Overview & Sizing
- **TAM:** {report['market_overview']['tam']}
- **SAM:** {report['market_overview']['sam']}
- **SOM:** {report['market_overview']['som']}
- **CAGR:** {report['market_overview']['cagr']}

{report['market_overview']['market_overview']}

### Industry Trends
{chr(10).join(f"- {t}" for t in report['market_overview']['key_trends'])}

---

## 2. Business Opportunities
{chr(10).join(f"### {o['name']} (Score: {o['overall_score']}/100)\n- **Concept:** {o['concept']}\n- **Target Audience:** {o['target_audience']}\n- **Revenue Model:** {o['revenue_model']}\n- **Competitive Advantage:** {o['competitive_advantage']}\n- **Difficulty:** {o['execution_difficulty']}\n" for o in report['opportunities'])}

---

## 3. High-Value Verified Prospects
{chr(10).join(f"- **{p['company_name']}** ({p['location']}) - Fit Score: {p['fit_score']}/100\n  - Website: {p['website']}\n  - Signal: {p['public_buying_signals']}\n  - Recommended Outreach: {p['recommended_outreach']}" for p in report['prospects'])}

---

## 4. Competitors
{chr(10).join(f"- **{c['name']}** ({c['type']}) - {c['website']}\n  - Pricing: {c['pricing']}\n  - Market Gap: {c['market_gap']}" for c in report['competitor_intelligence']['competitors'])}

---

## 5. Marketing Strategy
- **Positioning:** {report['marketing_strategy']['positioning_statement']}

### Recommended Channels
{chr(10).join(f"- **{ch['channel']}** ({ch['priority']}): {ch['rationale']}" for ch in report['marketing_strategy']['recommended_channels'])}

---

## 6. Strategic Action Plan (First 90 Days)
### First 7 Days
{chr(10).join(f"- [ ] {s['task']} *(KPI: {s['kpi']})*" for s in report['business_strategy']['strategic_action_plan']['first_7_days'])}

### First 30 Days
{chr(10).join(f"- [ ] {s['task']} *(KPI: {s['kpi']})*" for s in report['business_strategy']['strategic_action_plan']['first_30_days'])}

---

## 7. Token Usage & Optimization
- **Total Tokens Consumed:** {report['token_metrics']['total_tokens']:,}
- **Tokens Saved via Dynamic Routing:** {report['token_metrics']['tokens_saved_by_routing']:,}
- **Estimated API Cost:** ${report['token_metrics']['estimated_total_cost_usd']:.5f}
"""
    return Response(
        content=md,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=stratify_{report['industry_key']}.md"}
    )

def json_dumps(data):
    import json
    return json.dumps(data, indent=2)

# Mount web static directory
web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
static_dir = os.path.join(web_dir, "static")
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_path = os.path.join(web_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>STRATIFY Dashboard loading...</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
