from typing import List, Literal, Optional
from pydantic import BaseModel

class QuestionResponse(BaseModel):
    question: str
    response: str

class BrainstormRequest(BaseModel):
    user_id: str
    section: Literal["outreach"]
    idea_type: str
    form: Optional[List[QuestionResponse]] = None