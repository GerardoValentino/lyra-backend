from fastapi import (
    APIRouter, 
    Query,
    status, 
    Depends
)

from typing import Annotated
from app.schemas import SongRequest, SongAnalyticsRequest
from app.api.v1.services import fetch_song_lyrics, analyze_song_lyrics
from app.api.v1.dependencies import get_api_key
from app.utils.responses import success_response

router = APIRouter(
    prefix="/songs",
    tags=["songs"]
)

@router.get("/lyrics")
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
    api_key: str = Depends(get_api_key)
):
    response = await analyze_song_lyrics(
        message=request_data.message,
        lyrics=request_data.song_lyrics,
        api_key=api_key
    )

    return success_response(
        data=response, 
        message="Analisis completado con éxito"
    )

