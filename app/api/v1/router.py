from fastapi import APIRouter
from app.api.v1.routes import songs

api_router = APIRouter()

api_router.include_router(songs.router)