from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="lyra app", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def init():
    return { 'message': "Bienvenido a FatsAPI" }