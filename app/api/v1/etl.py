from fastapi import APIRouter, Depends, HTTPException, status
from functools import lru_cache

from app.services.etl_service import EtlService

router = APIRouter()

@lru_cache
def get_etl_service():
    return EtlService()

@router.post("/users")
async def load_users_data(
    etl_service: EtlService = Depends(get_etl_service),
):
    """
    ETL Users Process.
    """
    try:
        await etl_service.load_users_data()

        return {"status": "success", "message": "User data loaded successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ETL failed: {str(e)}"
        )
    
@router.post("/documents")
async def load_documents(
    etl_service: EtlService = Depends(get_etl_service),
):
    """
    ETL Documents Process - RAG System.
    """
    try:
        #await etl_service.load_documents()

        return {"status": "success", "message": "Coming soon"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ETL failed: {str(e)}"
        )