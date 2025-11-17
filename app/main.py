from fastapi import FastAPI

from app.api.v1.brainstorm import router as brainstorm_router
from app.api.v1.chat import router as chat_router
from app.api.v1.health import router as health_router
from app.core.config import get_settings
from app.core.logging import setup_logging

setup_logging()

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Routers
app.include_router(health_router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chatbot"])
app.include_router(brainstorm_router, prefix="/api/v1/brainstorm", tags=["brainstorm"])

@app.get("/")
async def root():
    return {"message": "Sales Assistant Agent API is running"}