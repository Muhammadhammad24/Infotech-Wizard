from app.api.dependencies import get_chatbot_service
from main import app
from tests.conftest import FakeChatbot


def test_health_reports_version_and_readiness(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["models_loaded"] is True
    assert body["version"]


def test_chat_returns_answer_with_sources(client, chatbot):
    res = client.post("/api/v1/chat/", json={"query": "How do I reset my password?", "top_k": 3})
    assert res.status_code == 200
    body = res.json()
    assert body["response"].startswith("Open Settings")
    assert body["search_results"][0]["score"] == 0.91
    assert chatbot.calls == [{"query": "How do I reset my password?", "top_k": 3, "max_tokens": None}]


def test_chat_rejects_empty_query(client):
    assert client.post("/api/v1/chat/", json={"query": ""}).status_code == 422


def test_chat_rejects_out_of_range_top_k(client):
    assert client.post("/api/v1/chat/", json={"query": "vpn", "top_k": 50}).status_code == 422


def test_chat_is_unavailable_until_models_load(client):
    app.dependency_overrides[get_chatbot_service] = lambda: FakeChatbot(ready=False)
    res = client.post("/api/v1/chat/", json={"query": "vpn"})
    assert res.status_code == 503
    assert "not ready" in res.json()["detail"]
