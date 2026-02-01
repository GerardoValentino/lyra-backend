from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.response import APIResponse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# --- Clases de Excepción para letras ---
class LyricsError(Exception):
    """Clase base para errores de letras"""
    def __init__(self, message: str, error: any):
        self.message = message
        self.error = error

class LyricsNotFoundError(LyricsError):
    pass

class LyricsServiceUnavailable(LyricsError):
    pass

# --- Clases de Excepción para IA ---
class AnalysisError(Exception):
    """Clase base para errores de análisis de IA"""
    def __init__(self, message: str, error: any = None):
        self.message = message
        self.error = error
        super().__init__(self.message)

class AnalysisServiceError(AnalysisError):
    """Cuando la API de IA falla o devuelve error de cuota/estado"""
    pass

class AnalysisTimeoutError(AnalysisError):
    """Cuando la IA tarda demasiado en responder (Timeout)"""
    pass


# --- Handlers ---

async def lyrics_error_handler(request: Request, exc: LyricsError):
    print(f"DEBUG: Error original capturado: {type(exc.error)}")
    logger.error(f"LYRICS ERROR: {exc.error}")

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

async def analysis_error_handler(request: Request, exc: AnalysisError):
    print(f"DEBUG: Error original capturado: {type(exc.error)}")
    logger.error(f"IA Analysis Error: {exc.error}")

    status_code = (
        status.HTTP_504_GATEWAY_TIMEOUT 
        if isinstance(exc, AnalysisTimeoutError) 
        else status.HTTP_502_BAD_GATEWAY
    )

    response = APIResponse(
        success=False,
        message=exc.message,
        data=None
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Maneja errores lanzados explícitamente a través de HTTPException.
    """

    response_content = APIResponse(
        success=False,
        message=exc.detail,
        data=None
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content.model_dump()
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
        Captura cualquier error de Python (KeyError, ValueError, etc.)
        que no haya sido manejado por otros handlers.
    """
    
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)

    response_content = APIResponse(
        success=False,
        message="Ocurrió un error interno inesperado en el servidor",
        data=None
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_content.model_dump()
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos los manejadores de excepciones en la aplicación.
    """
    # Errores estándar
    app.add_exception_handler(HTTPException, http_exception_handler)
    
    # Errores de Letras
    app.add_exception_handler(LyricsNotFoundError, lyrics_error_handler)
    app.add_exception_handler(LyricsServiceUnavailable, lyrics_error_handler)
    
    # Errores de Análisis (IA)
    app.add_exception_handler(AnalysisServiceError, analysis_error_handler)
    app.add_exception_handler(AnalysisTimeoutError, analysis_error_handler)
    
    # Error genérico (Catch-all)
    app.add_exception_handler(Exception, generic_exception_handler)