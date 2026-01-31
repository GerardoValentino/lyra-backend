from fastapi import APIRouter, Query, HTTPException, status
from starlette import status
from typing import Annotated
from app.schemas import SongRequest, SongAnalyticsRequest
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

router = APIRouter(
    prefix="/song",
    tags=["song"]
)

API_KEY = os.getenv("API_KEY")

@router.get("/lyrics", status_code=status.HTTP_200_OK)
async def get_song_lyrics(params: Annotated[SongRequest, Query()]):
    url = f"https://lrclib.net/api/get?artist_name={params.artist}&track_name={params.song_name}"
    
    async with httpx.AsyncClient() as client:
        try:
            # Esperamos 10 segundos por si tarda mucho en responder
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail="No se encontró la canción"
            )
        except (httpx.RequestError, httpx.TimeoutException):
            return {
                "lyrics": f"Cargando offline: Esta es una letra de prueba para {params.song_name}...",
                "source": "mock_data"
            }

@router.post("/analysis", status_code=status.HTTP_202_ACCEPTED)
async def analyze_song(request_data: SongAnalyticsRequest):
    if not API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="La API_KEY no está configurada en el servidor."
        )

    url = "https://apifreellm.com/api/v1/chat"

    prompt = f"{request_data.message}\n\nLyrics:\n{request_data.song_lyrics}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "message": prompt
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"Algo salio mal: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Ocurrio un problema analizando la canción: {str(e)}"
            )