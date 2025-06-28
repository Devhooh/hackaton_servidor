# ✅ app/models/meeting.py
from sqlalchemy import Column, String, DateTime, Interval, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base  # 👈 USA EL MISMO Base
import uuid

# Usa el mismo Base
meeting_participants = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", UUID(as_uuid=True), ForeignKey("meetings.id"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)

    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organizer = relationship("User", back_populates="organized_meetings")

    participants = relationship(
        "User",
        secondary=meeting_participants,
        back_populates="meetings"
    )
