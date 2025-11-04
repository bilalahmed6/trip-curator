# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Trip Curator Backend (placeholder)")

# Allow common dev origins (adjust for prod)
origins = [
    "http://localhost:7860",
    "http://127.0.0.1:7860",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(payload: ChatRequest):
    logger.info("Received chat: %s", payload.message)
    # Placeholder: later replace with LLM + retrieval.
    user = payload.message.strip()
    return {"reply": f"Echo (placeholder): {user}"}



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

@app.post("/plan", response_model=PlanResponse)
async def plan(req: PlanRequest):
    logger.info("Generated plan for query: %s", req.query)
    # Simple stub — returns structure; replace with real logic later
    days = []
    for d in range(1, max(1, req.days)+1):
        days.append(DayPlan(day=d, items=[{"time":"09:00","place":"Sample Place","notes":"Sample note"}]))
    return PlanResponse(title=f"Plan for: {req.query}", days=days)

from .storage import init_db, save_itinerary
init_db()

@app.post("/save")
async def save_itinerary_endpoint(payload: dict):
    title = payload.get("title", "untitled")
    import json
    save_itinerary(title, json.dumps(payload))
    return {"status":"saved"}


