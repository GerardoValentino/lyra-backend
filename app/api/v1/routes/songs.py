from fastapi import (
    APIRouter, 
    Query,
    status, 
    BackgroundTasks,
    Depends
)

from typing import Annotated
from app.utils.responses import success_response
from app.schemas import SongRequest, SongAnalyticsRequest
from app.api.v1.services import fetch_song_lyrics
from app.api.v1.dependencies import get_api_key
from app.api.v1.services import create_song_analysis_job

router = APIRouter(
    prefix="/songs",
    tags=["songs"]
)

@router.get("/lyrics", status_code=status.HTTP_200_OK)
async def get_song_lyrics(params: Annotated[SongRequest, Query()]):
    lyrics = await fetch_song_lyrics(
        artist=params.artist,
        song_name=params.song_name
    )

    return success_response(
        data=lyrics,
        message="Letra obtenida correctamente"
    )

@router.post("/analysis", status_code=status.HTTP_202_ACCEPTED)
async def analyze_song(
    request_data: SongAnalyticsRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    return create_song_analysis_job(
        request_data=request_data,
        api_key=api_key,
        background_tasks=background_tasks
    )

