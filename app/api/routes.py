from fastapi import APIRouter

from app.api.endpoints import chat,langgraph_chat

api_router = APIRouter()

# api_router.include_router(auth.router, prefix="/auth")

api_router.include_router(chat.router, prefix="/ai")
api_router.include_router(langgraph_chat.router, prefix="/graph", tags=["LangGraph Agent"])





