import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_chatbot_service
from app.models.responses import ChatResponse, SearchResult
from main import app


class _Probe:
    def __init__(self, ready: bool):
        self.model = object() if ready else None
        self._ready = ready

    def is_loaded(self) -> bool:
        return self._ready


class FakeChatbot:
    """Stands in for ChatbotService so tests never download or load models."""

    def __init__(self, ready: bool = True):
        self.ready = ready
        self.embeddings = _Probe(ready)
        self.database = _Probe(ready)
        self.llm = _Probe(ready)
        self.calls = []

    def is_ready(self) -> bool:
        return self.ready

    async def process_query(self, query, top_k=None, max_tokens=None):
        self.calls.append({"query": query, "top_k": top_k, "max_tokens": max_tokens})
        return ChatResponse(
            response="Open Settings, then Accounts, then Reset password.",
            query=query,
            context_used="Password reset steps",
            search_results=[
                SearchResult(subject="Password reset", answer="Settings > Accounts", score=0.91)
            ],
            processing_time=0.01,
        )


@pytest.fixture
def chatbot():
    return FakeChatbot()


@pytest.fixture
def client(chatbot):
    app.dependency_overrides[get_chatbot_service] = lambda: chatbot
    yield TestClient(app)
    app.dependency_overrides.clear()
