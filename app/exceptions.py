from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.schemas.response import APIResponse

# --- Clases de Excepción ---

class LyricsError(Exception):
    """Clase base para errores de letras"""
    def __init__(self, message: str, error: any):
        self.message = message
        self.error = error

class LyricsNotFoundError(LyricsError):
    pass

class LyricsServiceUnavailable(LyricsError):
    pass


# --- Handlers ---

async def lyrics_error_handler(request: Request, exc: LyricsError):
    print(f"DEBUG: Error original capturado: {type(exc.error)}")

    status_code = (
        status.HTTP_404_NOT_FOUND 
        if isinstance(exc, LyricsNotFoundError) 
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    response = APIResponse(
        success=False,
        message=exc.message,
        data=None
    )

    return JSONResponse(status_code=status_code, content=response.model_dump())

