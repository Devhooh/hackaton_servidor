from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# 👇 Importa todos los modelos aquí
from app.models.user import Base, User
from app.models.meeting import Meeting

from app.routes import user_routes, auth, meeting_routes
from app.core.error_handlers import register_error_handlers
from app.core.database import engine

app = FastAPI(title="ACI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
api_router = APIRouter(prefix="/api")
api_router.include_router(user_routes.router)
api_router.include_router(auth.router)  
api_router.include_router(meeting_routes.router)

app.include_router(api_router)

register_error_handlers(app)

# ✅ Esto ahora sí tiene todo el metadata de User, Meeting y la tabla intermedia
Base.metadata.create_all(bind=engine)
