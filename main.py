from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes, auth  
from app.core.error_handlers import register_error_handlers
from app.core.database import engine
from app.models.user import Base

app = FastAPI(title="Mi App con FastAPI y PostgreSQL")

# Opcional: CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(user_routes.router)
api_router.include_router(auth.router)  

app.include_router(api_router)

register_error_handlers(app)

# Crea tablas automáticamente
Base.metadata.create_all(bind=engine)
