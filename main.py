from fastapi import FastAPI, APIRouter
from app.routes import user_routes
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status
from app.core.error_handlers import register_error_handlers

app = FastAPI(title="Mi App con FastAPI y PostgreSQL")

api_router = APIRouter(prefix="/api")

api_router.include_router(user_routes.router)

app.include_router(api_router)

register_error_handlers(app)

# Optional: manejador para errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )
