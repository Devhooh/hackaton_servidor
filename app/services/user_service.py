from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.user import User
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("El correo ya está registrado")

def get_user(db: Session, user_id: int) -> User | None:
    result = db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    result = db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

def get_users_count(db: Session):
    result = db.execute(select(func.count(User.id)))
    return result.scalar_one()
