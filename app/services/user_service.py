from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserCreate
from sqlalchemy import func

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("El correo ya está registrado") 

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def get_users_count(db: AsyncSession):
    result = await db.execute(select(func.count(User.id)))
    return result.scalar_one()