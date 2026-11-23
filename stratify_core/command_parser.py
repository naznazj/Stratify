"""
STRATIFY Command Parser
Parses official command: /stratify [industry] [--location <loc>] [--depth <quick|standard|deep>]
Also handles sub-commands and follow-up prompts:
- /stratify expand [industry] opportunities
- /stratify competitors in [industry]
- /stratify find high-value [industry] clients
- /stratify marketing strategy for [industry]
- /stratify compare [industry1] vs [industry2]
"""
import re
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class StratifyCommand(BaseModel):
    raw_command: str
    action: str = "full_research"  # full_research, expand_opportunities, competitors, find_prospects, marketing_strategy, compare
    industry: str
    target_industry_2: Optional[str] = None  # for comparison
    location: Optional[str] = None
    depth: str = "standard"  # quick, standard, deep
    token_budget: Optional[int] = None
    custom_filters: Dict[str, Any] = Field(default_factory=dict)

def parse_stratify_command(input_str: str) -> StratifyCommand:
    cleaned = input_str.strip()
    
    # Strip leading slash if present
    if cleaned.startswith("/stratify"):
        args_str = cleaned[len("/stratify"):].strip()
    elif cleaned.startswith("stratify"):
        args_str = cleaned[len("stratify"):].strip()
    else:
        # User may have entered plain industry name like "Healthcare"
        args_str = cleaned

    # Extract flags
    location = None
    depth = "standard"
    budget = None

    # Flag: --location or -l
    loc_match = re.search(r'--(?:location|loc|-l)\s+([^\s\-]+(?:\s+[^\s\-]+)*?)(?=\s+--|$)', args_str, re.IGNORECASE)
    if loc_match:
        location = loc_match.group(1).strip()
        args_str = args_str.replace(loc_match.group(0), "").strip()

    # Flag: --depth or -d (quick, standard, deep)
    depth_match = re.search(r'--(?:depth|-d)\s+(quick|standard|deep)', args_str, re.IGNORECASE)
    if depth_match:
        depth = depth_match.group(1).lower()
        args_str = args_str.replace(depth_match.group(0), "").strip()

    # Flag: --budget or -b
    budget_match = re.search(r'--(?:budget|-b)\s+(\d+)', args_str, re.IGNORECASE)
    if budget_match:
        budget = int(budget_match.group(1))
        args_str = args_str.replace(budget_match.group(0), "").strip()

    # Clean remaining string for command patterns
    core_text = " ".join(args_str.split())

    # Check for comparison: 'compare X vs Y', 'compare X and Y', or 'X vs Y'
    compare_match = re.search(r'^(?:compare\s+(.+?)\s+(?:vs\.?|versus|and)\s+(.+)|(.+?)\s+(?:vs\.?|versus)\s+(.+))$', core_text, re.IGNORECASE)
    if compare_match:
        if compare_match.group(1) and compare_match.group(2):
            ind1 = compare_match.group(1).strip()
            ind2 = compare_match.group(2).strip()
        else:
            ind1 = compare_match.group(3).strip()
            ind2 = compare_match.group(4).strip()
        return StratifyCommand(
            raw_command=input_str,
            action="compare",
            industry=ind1,
            target_industry_2=ind2,
            location=location,
            depth=depth,
            token_budget=budget
        )

    # Check for sub-commands:
    # 1. expand ... opportunities
    expand_match = re.search(r'^expand\s+(?:the\s+)?(.+?)(?:\s+opportunities)?$', core_text, re.IGNORECASE)
    if expand_match:
        ind = expand_match.group(1).strip()
        return StratifyCommand(
            raw_command=input_str,
            action="expand_opportunities",
            industry=ind,
            location=location,
            depth=depth,
            token_budget=budget
        )

    # 2. competitors in ...
    comp_match = re.search(r'^competitors?\s+(?:in|for)?\s*(.+)$', core_text, re.IGNORECASE)
    if comp_match:
        ind = comp_match.group(1).strip()
        return StratifyCommand(
            raw_command=input_str,
            action="competitors",
            industry=ind,
            location=location,
            depth=depth,
            token_budget=budget
        )

    # 3. find high-value ... clients/prospects/targets
    prospect_match = re.search(r'^(?:find\s+)?(?:high-value\s+|top\s+)?(.+?)(?:\s+clients|\s+prospects|\s+targets)?$', core_text, re.IGNORECASE)
    if "client" in core_text.lower() or "prospect" in core_text.lower() or "target" in core_text.lower() or "find" in core_text.lower():
        # Clean out tokens
        cleaned_ind = re.sub(r'find|high-value|clients?|prospects?|targets?|in|for', '', core_text, flags=re.IGNORECASE).strip()
        if cleaned_ind:
            return StratifyCommand(
                raw_command=input_str,
                action="find_prospects",
                industry=cleaned_ind,
                location=location,
                depth=depth,
                token_budget=budget
            )

    # 4. marketing strategy for ...
    mkt_match = re.search(r'^marketing\s+strategy\s+(?:for|in)?\s*(.+)$', core_text, re.IGNORECASE)
    if mkt_match:
        ind = mkt_match.group(1).strip()
        return StratifyCommand(
            raw_command=input_str,
            action="marketing_strategy",
            industry=ind,
            location=location,
            depth=depth,
            token_budget=budget
        )

    # Default to full_research with the provided industry
    default_industry = core_text if core_text else "Technology and SaaS"
    return StratifyCommand(
        raw_command=input_str,
        action="full_research",
        industry=default_industry,
        location=location,
        depth=depth,
        token_budget=budget
    )
