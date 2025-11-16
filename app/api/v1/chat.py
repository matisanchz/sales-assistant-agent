from fastapi import APIRouter, Depends
from typing import Optional, Dict, Any

from app.schemas.chat_message import ChatMessageResponse, ChatMessageRequest

router = APIRouter()

def get_chat_service():
    return {}

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    payload: ChatMessageRequest,
    chat_service = Depends(get_chat_service),
):
    """
    Main endpoint for the Sales Assistant chatbot.
    """

    return ChatMessageResponse(
        user_id=payload.user_id,
        session_id=payload.session_id,
        response=None
    )