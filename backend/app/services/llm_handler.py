def generate_chat_reply(message: str, user_id: str | None = None) -> dict:
    return {"reply": f"Echo (stub): {message}", "context": {"source": "stub"}}

def generate_plan(query: str, days: int = 3, preferences: dict | None = None) -> dict:
    days_list = [{"day": d, "items":[{"time":"09:00","place":"Sample","notes":"Sample"}]} for d in range(1, days+1)]
    return {"title": f"Plan for: {query}", "days": days_list}
