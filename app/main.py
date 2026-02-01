from fastapi import FastAPI, HTTPException
from app.api.v1 import api_router
from dotenv import load_dotenv
from app.exceptions import http_exception_handler, generic_exception_handler

load_dotenv()

app = FastAPI(title="Lyra App", version="1.0.0")

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def init():
    return { 'message': "Bienvenido a Lyra App" }