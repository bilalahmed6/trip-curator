# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.config import ORIGINS
from app.routers.chat import router as chat_router
from app.routers.plan import router as plan_router
# from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Trip Curator Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(plan_router, prefix="/plan", tags=["plan"])



from .storage import init_db, save_itinerary
try:
    init_db()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

@app.post("/save")
async def save_itinerary_endpoint(payload: dict):
    title = payload.get("title", "untitled")
    import json
    save_itinerary(title, json.dumps(payload))
    return {"status":"saved"}


