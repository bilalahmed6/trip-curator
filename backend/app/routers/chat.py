from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_handler import generate_chat_reply
from app.utils.rate_limiter import allow_request
from fastapi import HTTPException, Request  
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()
@router.post("", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest,request: Request):
    user_key = request.headers.get('X-User-ID', request.client.host)
    logger.info(f"User key: {user_key}")
    if not allow_request(user_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    result = generate_chat_reply(payload.message, payload.user_id)
    return {'reply': result['reply'], 'context': result.get('context')}
