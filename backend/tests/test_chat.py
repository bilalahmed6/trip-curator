from app.routers.chat import router as chat_router



import pytest

# write proper documentation later
def test_chat_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app
    # initialize test client
    client = TestClient(app)
    payload = {
        "message": "Hello, how are you?",
        "user_id": "user123"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["reply"] == f"Echo (stub): {payload['message']}"
    assert "context" in data
    assert data["context"]["source"] == "stub"


