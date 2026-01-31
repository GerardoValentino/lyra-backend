from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Annotated
import httpx
from app.schemas import SongRequest, SongAnalyticsRequest
from app.api.v1.services import fetch_song_lyrics
from app.api.v1.services import analyze_song_lyrics
from app.api.v1.dependencies import get_api_key

router = APIRouter(
    prefix="/songs",
    tags=["songs"]
)

@router.get("/lyrics", status_code=status.HTTP_200_OK)
async def get_song_lyrics(params: Annotated[SongRequest, Query()]):
        try:
            return await fetch_song_lyrics(
                artist=params.artist,
                song_name=params.song_name
            )
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la canción"
            )
        except httpx.RequestError:
            return {
                "lyrics": f"Offline: letra para {params.song_name}",
                "source": "mock_data"
            }

@router.post("/analysis", status_code=status.HTTP_202_ACCEPTED)
async def analyze_song(request_data: SongAnalyticsRequest, api_key: str = Depends(get_api_key)):
    try:
        return await analyze_song_lyrics(
            message=request_data.message,
            lyrics=request_data.song_lyrics,
            api_key=api_key
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ocurrio un problema al analizar la canción con IA: {e.response.text}"
        )