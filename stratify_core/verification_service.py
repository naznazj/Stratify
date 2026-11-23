"""
STRATIFY Research Verification Service
Strictly tracks citations, verified URLs, publication dates, and classifies factual claims into:
1. VERIFIED_FACT (Official government data, public SEC filings, company websites)
2. RESEARCH_ESTIMATE (Reputable analyst projections from Gartner, Statista, McKinsey)
3. AI_HYPOTHESIS (Engineered strategic opportunity or recommended positioning)
4. DATA_UNAVAILABLE (Explicit limitation when evidence is insufficient)
"""
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import datetime

class FactClassification(str, Enum):
    VERIFIED_FACT = "VERIFIED_FACT"
    RESEARCH_ESTIMATE = "RESEARCH_ESTIMATE"
    AI_HYPOTHESIS = "AI_HYPOTHESIS"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"

class Citation(BaseModel):
    id: str
    claim: str
    classification: FactClassification
    source_name: str
    source_url: str
    publication_year: Optional[int] = None
    research_date: str = Field(default_factory=lambda: datetime.date.today().isoformat())
    confidence_score: float = 0.90
    data_limitation_notes: Optional[str] = None

class VerificationService:
    def __init__(self):
        self.citations: Dict[str, Citation] = {}

    def register_citation(
        self,
        citation_id: str,
        claim: str,
        classification: FactClassification,
        source_name: str,
        source_url: str,
        publication_year: Optional[int] = None,
        confidence_score: float = 0.90,
        limitation_notes: Optional[str] = None
    ) -> Citation:
        cit = Citation(
            id=citation_id,
            claim=claim,
            classification=classification,
            source_name=source_name,
            source_url=source_url,
            publication_year=publication_year,
            confidence_score=confidence_score,
            data_limitation_notes=limitation_notes
        )
        self.citations[citation_id] = cit
        return cit

    def get_citation(self, citation_id: str) -> Optional[Citation]:
        return self.citations.get(citation_id)

    def list_citations(self) -> List[Citation]:
        return list(self.citations.values())

    def get_credibility_summary(self) -> Dict[str, Any]:
        total = len(self.citations)
        if total == 0:
            return {"total_citations": 0, "avg_confidence": 0.0, "distribution": {}}

        counts = {
            FactClassification.VERIFIED_FACT.value: 0,
            FactClassification.RESEARCH_ESTIMATE.value: 0,
            FactClassification.AI_HYPOTHESIS.value: 0,
            FactClassification.DATA_UNAVAILABLE.value: 0
        }
        total_conf = 0.0
        for c in self.citations.values():
            counts[c.classification.value] += 1
            total_conf += c.confidence_score

        return {
            "total_citations": total,
            "avg_confidence": round(total_conf / total, 2),
            "distribution": counts
        }
