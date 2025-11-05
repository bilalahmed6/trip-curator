from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_handler import generate_chat_reply
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()
@router.post("", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    logger
    result = generate_chat_reply(payload.message, payload.user_id)
    return {'reply': result['reply'], 'context': result.get('context')}
