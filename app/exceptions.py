from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.response import APIResponse

async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    response = APIResponse(
        success=False,
        message=exc.detail,
        data=None
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )
