import httpx
from app.exceptions import (
    AnalysisServiceError,
    AnalysisTimeoutError
)

async def analyze_song_lyrics(
    message: str,
    lyrics: str,
    api_key: str
) -> dict:
    url = "https://apifreellm.com/api/v1/chat"

    prompt = f"{message}\n\nLyrics:\n{lyrics}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {"message": prompt}

    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            # Capturamos fallos de la API (401, 429, 500, etc.)
            raise AnalysisServiceError(
                "No se pudo completar el análisis de IA en este momento", 
                e
            )
        except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
            # Capturamos específicamente el timeout
            raise AnalysisTimeoutError(
                "La IA tardó demasiado en responder. Intenta con un texto más corto.", 
                e
            )
        except httpx.RequestError as e:
            # Cualquier otro error de red
            raise AnalysisServiceError(
                "Error de conexión con el servicio de análisis", 
                e
            )