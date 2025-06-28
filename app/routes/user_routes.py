from fastapi import APIRouter, Depends, status, Query, HTTPException  # 👈 Importa HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserRead, UsersPaginatedResponse
from app.services.user_service import create_user, get_user, get_users, get_users_count
from app.core.database import get_db
from app.utils.response import response

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    user_data = UserRead.model_validate(db_user).model_dump()
    return response(
        status_code=201,
        message="Usuario creado exitosamente",
        data=user_data
    )

@router.get("/{user_id}")
async def get_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")
    user_data = UserRead.model_validate(db_user).model_dump()
    return response(
        status_code=200,
        message="Usuario obtenido exitosamente",
        data=user_data
    )

@router.get("/", response_model=UsersPaginatedResponse)
async def get_users_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
):
    users = get_users(db, skip, limit)
    total = get_users_count(db)

    users_data = [UserRead.model_validate(user).model_dump() for user in users]

    return response(
        status_code=200,
        message="Usuarios obtenidos exitosamente",
        data=users_data,
        count_data=total,
    )
