from app.schemas.response import APIResponse

def success_response(
    data=None,
    message: str = "Operación exitosa"
):
    return APIResponse(
        success=True,
        message=message,
        data=data
    )
