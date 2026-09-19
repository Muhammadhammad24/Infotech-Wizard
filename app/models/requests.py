from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """A question for the assistant."""

    query: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    top_k: Optional[int] = Field(
        default=None, ge=1, le=20, description="Number of knowledge-base entries to retrieve"
    )
    max_tokens: Optional[int] = Field(
        default=None, ge=50, le=500, description="Upper bound on the generated answer length"
    )


class HealthCheckResponse(BaseModel):
    status: str
    version: str
    models_loaded: bool
