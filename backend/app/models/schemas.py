# backend/app/models/schemas.py (summary)
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    context: Optional[Dict[str, Any]] = None

class PlanRequest(BaseModel):
    query: str
    days: int = 3
    preferences: Dict[str, Any] = {}

class DayPlan(BaseModel):
    day: int
    items: List[Dict[str, Any]]

class PlanResponse(BaseModel):
    title: str
    days: List[DayPlan]
