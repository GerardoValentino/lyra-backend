from fastapi import FastAPI
from app.api.v1 import api_router
from dotenv import load_dotenv
from app.socket import socket_app

load_dotenv()

app = FastAPI(title="Lyra App", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

app.mount("/ws", socket_app)

@app.get("/")
def init():
    return { 'message': "Bienvenido a FastAPI" }