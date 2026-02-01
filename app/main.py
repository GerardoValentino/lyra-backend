from fastapi import FastAPI, HTTPException
from app.api.v1 import api_router
from dotenv import load_dotenv
from app.exceptions import setup_exception_handlers

load_dotenv()

app = FastAPI(title="Lyra App", version="1.0.0")

# --- REGISTRO DE EXCEPTION HANDLERS ---
setup_exception_handlers(app)

# -- Rutas --
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def init():
    return { 'message': "Bienvenido a Lyra App" }