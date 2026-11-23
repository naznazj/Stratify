"""
STRATIFY Token Tracking & Optimization Engine
Tracks input/output tokens per session and per agent, estimates costs accurately,
monitors cache hits, and tracks savings achieved by dynamic skill routing.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time

class AgentTokenUsage(BaseModel):
    agent_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    task_name: str = ""

class SessionTokenMetrics(BaseModel):
    session_id: str
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    tokens_saved_by_routing: int = 0
    cached_tokens: int = 0
    estimated_total_cost_usd: float = 0.0
    active_skills_count: int = 0
    agent_breakdown: List[AgentTokenUsage] = Field(default_factory=list)
    token_budget: Optional[int] = None
    budget_exhausted: bool = False
    is_exact_provider_usage: bool = False
    timestamp: float = Field(default_factory=time.time)

class TokenTracker:
    # Standard pricing model estimates (e.g. $0.15/1M input, $0.60/1M output)
    INPUT_COST_PER_1M = 0.15
    OUTPUT_COST_PER_1M = 0.60

    def __init__(self, session_id: str, token_budget: Optional[int] = None):
        self.session_id = session_id
        self.token_budget = token_budget
        self.metrics = SessionTokenMetrics(session_id=session_id, token_budget=token_budget)

    def record_agent_usage(self, agent_name: str, task_name: str, input_tokens: int, output_tokens: int,
                           cached_tokens: int = 0, is_exact: bool = False):
        total = input_tokens + output_tokens
        cost = (input_tokens * self.INPUT_COST_PER_1M / 1_000_000.0) + (output_tokens * self.OUTPUT_COST_PER_1M / 1_000_000.0)

        # Check existing agent in breakdown
        existing = next((a for a in self.metrics.agent_breakdown if a.agent_name == agent_name and a.task_name == task_name), None)
        if existing:
            existing.input_tokens += input_tokens
            existing.output_tokens += output_tokens
            existing.total_tokens += total
            existing.estimated_cost_usd += round(cost, 6)
        else:
            self.metrics.agent_breakdown.append(AgentTokenUsage(
                agent_name=agent_name,
                task_name=task_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total,
                estimated_cost_usd=round(cost, 6)
            ))

        self.metrics.total_input_tokens += input_tokens
        self.metrics.total_output_tokens += output_tokens
        self.metrics.total_tokens += total
        self.metrics.cached_tokens += cached_tokens
        self.metrics.estimated_total_cost_usd += cost
        self.metrics.is_exact_provider_usage = is_exact

        # Enforce budget
        if self.token_budget and self.metrics.total_tokens >= self.token_budget:
            self.metrics.budget_exhausted = True

    def record_routing_savings(self, saved_tokens: int, active_skills_count: int):
        self.metrics.tokens_saved_by_routing += saved_tokens
        self.metrics.active_skills_count = active_skills_count

    def get_summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "total_input_tokens": self.metrics.total_input_tokens,
            "total_output_tokens": self.metrics.total_output_tokens,
            "total_tokens": self.metrics.total_tokens,
            "tokens_saved_by_routing": self.metrics.tokens_saved_by_routing,
            "cached_tokens": self.metrics.cached_tokens,
            "estimated_total_cost_usd": round(self.metrics.estimated_total_cost_usd, 5),
            "active_skills_count": self.metrics.active_skills_count,
            "token_budget": self.metrics.token_budget,
            "budget_exhausted": self.metrics.budget_exhausted,
            "is_exact_provider_usage": self.metrics.is_exact_provider_usage,
            "agent_breakdown": [a.model_dump() for a in self.metrics.agent_breakdown]
        }
