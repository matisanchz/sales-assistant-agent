from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Optional, Dict, Any

from app.schemas.chat_message import ChatMessageResponse, ChatMessageRequest
from app.services.chat_service import ChatService

router = APIRouter()

@lru_cache
def get_chat_service():
    return ChatService()

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    payload: ChatMessageRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Main endpoint for the Sales Assistant chatbot.
    """
    try:
        result = await chat_service.process_message(
            user_id=payload.user_id,
            session_id=payload.session_id,
            user_input=payload.user_input
        )

        return ChatMessageResponse(
            user_id=result["user_id"],
            session_id=result["session_id"],
            response=result["response"]
        )
    except Exception as e:
        raise