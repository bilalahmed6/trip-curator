# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Trip Curator Backend (placeholder)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(payload: dict):
    # placeholder logic for Day 1
    user = payload.get("message", "")
    return {"reply": f"Echo (placeholder): {user}"}
