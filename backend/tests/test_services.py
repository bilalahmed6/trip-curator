from  app.services.llm_handler import generate_chat_reply, generate_plan

import pytest

def test_generate_chat_reply():
    message = "Hello, how are you?"
    user_id = "user123"
    response = generate_chat_reply(message, user_id)
    
    assert "reply" in response
    assert response["reply"] == f"Echo (stub): {message}"
    assert "context" in response
    assert response["context"]["source"] == "stub"

def test_generate_plan():
    query = "Plan a trip to Paris"
    days = 5
    preferences = {"food": "vegan", "activities": ["museums", "parks"]}
    response = generate_plan(query, days, preferences)
    assert "title" in response
    assert response["title"] == f"Plan for: {query}"
    assert "days" in response
    assert len(response["days"]) == days
    for day_plan in response["days"]:
        # later we can expand this to check contents of day
        assert "day" in day_plan
        # later we can expand this to check contents of items
        assert "items" in day_plan
        assert isinstance(day_plan["items"], list)  

def test_allow_requests():
    from app.utils.rate_limiter import allow_request
    user_key = "test_user"
    # Allow up to 5 requests
    for _ in range(5):
        assert allow_request(user_key) == True
    # 6th request should be blocked
    assert allow_request(user_key) == False







