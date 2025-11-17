from pydantic import BaseModel
from typing import Optional

class ChatMessageRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    user_input: str

class ChatMessageResponse(BaseModel):
    user_id: str
    session_id: str
    response: str
