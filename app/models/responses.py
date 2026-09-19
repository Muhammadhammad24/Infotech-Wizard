from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """One knowledge-base entry retrieved for a query."""

    subject: str
    answer: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    response: str
    query: str
    context_used: Optional[str] = None
    search_results: List[SearchResult] = Field(default_factory=list)
    processing_time: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    detail: str
