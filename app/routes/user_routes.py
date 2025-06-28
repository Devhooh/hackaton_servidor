from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import create_user, get_user
from app.core.database import get_db
from app.utils.response import response

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    user_data = UserRead.model_validate(db_user).model_dump()
    return response(
        status_code=201,
        message="User created successfully",
        data=user_data
    )

@router.get("/{user_id}")
async def get_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id)
    if not db_user:
        return response(
            status_code=404,
            message="User not found",
            error=f"No user found with id {user_id}"
        )
    user_data = UserRead.model_validate(db_user).model_dump()
    return response(
        status_code=200,
        message="User retrieved successfully",
        data=user_data
    )
