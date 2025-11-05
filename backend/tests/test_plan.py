from app.main import app

import pytest
def test_plan_endpoint():
    from fastapi.testclient import TestClient
    # initialize test client
    client = TestClient(app)
    payload = {
        "query": "Plan a trip to Paris",
        "days": 5,
        "preferences": {"food": "vegan", "activities": ["museums", "parks"]}
    }
    response = client.post("/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert data["title"] == f"Plan for: {payload['query']}"
    assert "days" in data
    assert len(data["days"]) == payload["days"]
    for day_plan in data["days"]:
        # later we can expand this to check contents of day
        assert "day" in day_plan
        # later we can expand this to check contents of items
        assert "items" in day_plan
        assert isinstance(day_plan["items"], list)

