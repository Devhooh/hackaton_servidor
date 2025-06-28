from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.enums import UserTypeEnum, GenderEnum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(SQLAlchemyEnum(GenderEnum), nullable=True)
    user_type = Column(SQLAlchemyEnum(UserTypeEnum), nullable=True)