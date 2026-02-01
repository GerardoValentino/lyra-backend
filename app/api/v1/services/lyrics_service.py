import httpx
from fastapi import HTTPException

async def fetch_song_lyrics(artist: str, song_name: str) -> dict:
    url = (
        "https://lrclib.net/api/get"
        f"?artist_name={artist}&track_name={song_name}"
    )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            # Error esperado (404, 400, etc.)
            raise HTTPException(
                status_code=404,
                detail="No se encontró la letra de la canción"
            )

        except httpx.RequestError:
            # Error de red / timeout
            raise HTTPException(
                status_code=503,
                detail="Servicio de letras no disponible"
            )
