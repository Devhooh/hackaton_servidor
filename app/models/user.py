# ✅ app/models/user.py
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.schemas.enums import UserTypeEnum, GenderEnum
from app.core.database import Base  # 👈 USA EL MISMO Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(SQLAlchemyEnum(GenderEnum), nullable=False)
    user_type = Column(SQLAlchemyEnum(UserTypeEnum), nullable=False)

    organized_meetings = relationship("Meeting", back_populates="organizer")
    meetings = relationship(
        "Meeting",
        secondary="meeting_participants",
        back_populates="participants"
    )

# ✅ CIERRA EL CICLO SOLO SI HACE FALTA
from app.models.meeting import Meeting
