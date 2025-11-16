from pydantic import BaseModel

class ChatMessageRequest(BaseModel):
    user_id: str
    session_id: str
    user_input: str

class ChatMessageResponse(BaseModel):
    user_id: str
    session_id: str
    response: str
