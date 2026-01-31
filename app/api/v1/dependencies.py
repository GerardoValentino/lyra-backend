import os
from fastapi import HTTPException, status

def get_api_key() -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_KEY no configurada"
        )
    return api_key
