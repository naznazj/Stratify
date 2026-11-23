"""
STRATIFY Opportunity Scoring Engine
Calculates a transparent, weighted score (0-100) across 5 core dimensions:
1. Market Demand (25%)
2. Revenue Potential (25%)
3. Customer Purchasing Power (20%)
4. Competitive Opportunity / White Space (15%)
5. Execution Feasibility (15%)

Allows configurable weights and provides evidence, assumptions, and confidence ratings.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ScoringDimension(BaseModel):
    name: str
    key: str
    weight: float
    score: float  # 0 to 100
    weighted_score: float
    evidence: str
    assumptions: str

class OpportunityScoreResult(BaseModel):
    overall_score: float
    confidence_level: str  # High, Moderate, Preliminary
    confidence_rating: float  # 0.0 - 1.0
    dimensions: List[ScoringDimension]
    execution_difficulty: str  # Low, Medium, High
    revenue_model: str
    moat_strength: str
    rationale_summary: str

class OpportunityScoringEngine:
    DEFAULT_WEIGHTS = {
        "market_demand": 0.25,
        "revenue_potential": 0.25,
        "purchasing_power": 0.20,
        "competitive_opportunity": 0.15,
        "execution_feasibility": 0.15
    }

    def __init__(self, custom_weights: Optional[Dict[str, float]] = None):
        self.weights = custom_weights if custom_weights else self.DEFAULT_WEIGHTS.copy()
        # Normalize weights so sum equals 1.0
        total_w = sum(self.weights.values())
        if total_w > 0:
            self.weights = {k: v / total_w for k, v in self.weights.items()}

    def score_opportunity(
        self,
        name: str,
        market_demand_val: float,
        market_demand_evidence: str,
        revenue_potential_val: float,
        revenue_potential_evidence: str,
        purchasing_power_val: float,
        purchasing_power_evidence: str,
        competitive_opp_val: float,
        competitive_opp_evidence: str,
        feasibility_val: float,
        feasibility_evidence: str,
        confidence_rating: float = 0.85,
        assumptions: Optional[Dict[str, str]] = None
    ) -> OpportunityScoreResult:
        if assumptions is None:
            assumptions = {
                "market_demand": "Based on search volume growth and industry CAGR projections.",
                "revenue_potential": "Assumes standard monetization benchmarks for target segment.",
                "purchasing_power": "Derived from firmographic revenue bands or consumer discretionary income.",
                "competitive_opportunity": "Based on observed unserved gaps and competitor pricing ceilings.",
                "execution_feasibility": "Reflects tech complexity, capital requirement, and regulatory friction."
            }

        dims_data = [
            ("Market Demand", "market_demand", market_demand_val, market_demand_evidence, assumptions.get("market_demand", "")),
            ("Revenue Potential", "revenue_potential", revenue_potential_val, revenue_potential_evidence, assumptions.get("revenue_potential", "")),
            ("Customer Purchasing Power", "purchasing_power", purchasing_power_val, purchasing_power_evidence, assumptions.get("purchasing_power", "")),
            ("Competitive Opportunity", "competitive_opportunity", competitive_opp_val, competitive_opp_evidence, assumptions.get("competitive_opportunity", "")),
            ("Execution Feasibility", "execution_feasibility", feasibility_val, feasibility_evidence, assumptions.get("execution_feasibility", ""))
        ]

        scored_dimensions: List[ScoringDimension] = []
        overall_total = 0.0

        for label, key, raw_score, evidence, assumption in dims_data:
            clamped_score = max(0.0, min(100.0, float(raw_score)))
            w = self.weights.get(key, 0.20)
            weighted = clamped_score * w
            overall_total += weighted

            scored_dimensions.append(ScoringDimension(
                name=label,
                key=key,
                weight=round(w, 2),
                score=round(clamped_score, 1),
                weighted_score=round(weighted, 1),
                evidence=evidence,
                assumptions=assumption
            ))

        # Determine confidence level string
        if confidence_rating >= 0.80:
            conf_level = "High (Empirical & Industry Backed)"
        elif confidence_rating >= 0.60:
            conf_level = "Moderate (Research-Based Model)"
        else:
            conf_level = "Preliminary (Early Stage Signal)"

        # Difficulty classification
        if feasibility_val >= 75:
            diff = "Low (Fast Time-to-Market)"
        elif feasibility_val >= 50:
            diff = "Medium (Moderate Capital/Dev Required)"
        else:
            diff = "High (Significant Regulatory/Engineering Barrier)"

        return OpportunityScoreResult(
            overall_score=round(overall_total, 1),
            confidence_level=conf_level,
            confidence_rating=round(confidence_rating, 2),
            dimensions=scored_dimensions,
            execution_difficulty=diff,
            revenue_model="Value-Aligned Subscription / Take-Rate",
            moat_strength="High Switching Costs & Regulatory Moat" if competitive_opp_val >= 75 else "Moderate Defensibility",
            rationale_summary=f"Scored {round(overall_total, 1)}/100 driven by strong {dims_data[0][0].lower()} ({market_demand_val:.0f}) and {dims_data[1][0].lower()} ({revenue_potential_val:.0f})."
        )
