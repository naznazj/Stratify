"""
STRATIFY Base Agent
Base class providing token tracking, execution logging, verification linking, and shared context.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from stratify_core.token_tracker import TokenTracker
from stratify_core.verification_service import VerificationService
from stratify_core.industry_classifier import IndustryProfile
from stratify_core.command_parser import StratifyCommand

class BaseAgent(ABC):
    def __init__(self, name: str, role_title: str, token_tracker: TokenTracker, verification_service: VerificationService):
        self.name = name
        self.role_title = role_title
        self.token_tracker = token_tracker
        self.verification_service = verification_service

    @abstractmethod
    def execute(self, command: StratifyCommand, profile: IndustryProfile, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the specialized research task and returns structured findings."""
        pass

    def record_usage(self, task_name: str, input_tokens: int, output_tokens: int, cached: int = 0, is_exact: bool = False):
        self.token_tracker.record_agent_usage(
            agent_name=self.role_title,
            task_name=task_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached,
            is_exact=is_exact
        )
