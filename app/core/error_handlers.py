from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import response
import traceback

def register_error_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return response(
            status_code=exc.status_code,
            message=str(exc.detail),
            error=exc.__class__.__name__
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return response(
            status_code=422,
            message="Error de validación en los datos enviados",
            error=exc.errors()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        traceback.print_exc()  # Log para debug
        return response(
            status_code=500,
            message="Error interno del servidor",
            error=str(exc)
        )
