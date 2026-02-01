import httpx
from app.exceptions import LyricsNotFoundError, LyricsServiceUnavailable

async def fetch_song_lyrics(artist: str, song_name: str) -> dict:
    url = f"https://lrclib.net/api/get?artist_name={artist}&track_name={song_name}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise LyricsNotFoundError("No se encontró la letra de esta canción", e)
            # Para otros errores de estado (400, 500, etc.)
            raise LyricsServiceUnavailable("El servicio de letras externo falló", e)

        except httpx.RequestError as e:
            # Errores de conexión, DNS o timeouts
            raise LyricsServiceUnavailable("No se pudo conectar con el servicio de letras", e)