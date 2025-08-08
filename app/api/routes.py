from fastapi import APIRouter

from app.api.endpoints import auth,manage_game,manage_collab,manage_player,manage_team

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")