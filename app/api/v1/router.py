from fastapi import APIRouter
from app.api.v1.routes import songs
from app.api.v1.routes import jobs

api_router = APIRouter()

api_router.include_router(songs.router)
api_router.include_router(jobs.router)