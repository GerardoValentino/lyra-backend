from fastapi import FastAPI
from app.api.v1 import api_router
from dotenv import load_dotenv
from app.exceptions import (
    lyrics_error_handler,
    LyricsNotFoundError,
    LyricsServiceUnavailable
)

load_dotenv()

app = FastAPI(title="Lyra App", version="1.0.0")

app.add_exception_handler(LyricsNotFoundError, lyrics_error_handler)
app.add_exception_handler(LyricsServiceUnavailable, lyrics_error_handler)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def init():
    return { 'message': "Bienvenido a Lyra App" }