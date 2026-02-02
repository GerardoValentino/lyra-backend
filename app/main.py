from fastapi import FastAPI, HTTPException
from app.api.v1 import api_router
from dotenv import load_dotenv
from app.exceptions import setup_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Lyra App", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRO DE EXCEPTION HANDLERS ---
setup_exception_handlers(app)

# -- Rutas --
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def init():
    return { 'message': "Bienvenido a Lyra App" }