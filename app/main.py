from fastapi import FastAPI
from app.api.v1.chat import router as chat_router
from app.api.v1.health import router as health_router

app = FastAPI(
    title="Sales Assistant Agent API",
    version="0.1.0",
    description="API backend for the sales-assistant-agent project."
)

# Routers
app.include_router(health_router, prefix="/api/v1/health", tags=["health"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Sales Assistant Agent API is running"}