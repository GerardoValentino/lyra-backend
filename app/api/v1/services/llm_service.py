import httpx
from app.exceptions import (
    AnalysisServiceError,
    AnalysisTimeoutError
)

async def analyze_song_lyrics(
    lyrics: str,
    api_key: str
) -> dict:
    url = "https://apifreellm.com/api/v1/chat"

    message = """
    Analiza la siguiente canción y haz el siguiente análisis:
    Clasificala en una de las siguientes categorias:
        1. Amor
        2. Desamor
        3. Muerte
        4. Crítica social
        5. Crítica política
        6. Religión
        7. Experiencia personal
        8. Otro

    Redacta un breve resumen del contenido de la canción.
    Haz interpretación del significado de la canción, especialmente en los casos en los que:
        1. Existan metáforas
        2. El mensaje no sea literal
        3. El significado requiera un análisis más profundo

    Indica si la canción es cantada desde la perspectiva de:
        Una persona de género masculino
        Una persona de género femenino
        Indeterminado (No es posible inferirlo claramente)

    Si existe, extrae una lista de:
        Nombres de empresas
        Marcas
        Productos comerciales
    
    RESPONDE ÚNICAMENTE EN FORMATO JSON. No incluyas introducciones ni notas al pie. 
    Sigue esta estructura:
    {
    "categoria": "...",
    "resumen": "...",
    "interpretacion": "...",
    "perspectiva": "...",
    "entidades": []
    }
    """

    prompt = f"{message}\n\Aquí esta la letra:\n{lyrics}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {"message": prompt }

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