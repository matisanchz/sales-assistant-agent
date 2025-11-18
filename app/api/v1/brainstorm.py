from fastapi import APIRouter, Depends, HTTPException, status
from functools import lru_cache

from app.schemas.brainstorm import BrainstormRequest
from app.services.brainstorm_service import BrainstormService

router = APIRouter()

@lru_cache
def get_brainstorm_service():
    return BrainstormService()

@router.post("/ideas")
async def generate_idea(
    payload: BrainstormRequest,
    brainstorm_service: BrainstormService = Depends(get_brainstorm_service),
):
    """
    This endpoint generates brainstorm ideas based on the selected section and subsection.
    """
    try:
        return await brainstorm_service.generate_idea(
            user_id=payload.user_id,
            section=payload.section,
            idea_type=payload.idea_type,
            form=payload.form
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Your request couldn't be processed: {str(e)}"
        )