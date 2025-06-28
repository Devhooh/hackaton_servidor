from fastapi import APIRouter, Depends, status
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import create_user, get_user, get_users, get_users_count
from app.core.database import get_db
from app.utils.response import response
from app.schemas.user_schema import UsersPaginatedResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    user_data = UserRead.model_validate(db_user).model_dump()
    return response(
        status_code=201,
        message="Usuario creado exitosamente",
        data=user_data
    )

@router.get("/{user_id}")
async def get_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id)
    if not db_user:
        return response(
            status_code=404,
            message="Usuario no encontrado",
            error=f"No se encontró usuario con id {user_id}"
        )
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
    db: AsyncSession = Depends(get_db),
):
    users = await get_users(db, skip, limit)
    total = await get_users_count(db)

    users_data = [UserRead.model_validate(user).model_dump() for user in users]

    return response(
        status_code=200,
        message="Usuarios obtenidos exitosamente",
        data=users_data,
        count_data=total,
    )

