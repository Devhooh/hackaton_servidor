from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID
from app.schemas.user_schema import UserOut

class MeetingCreate(BaseModel):
    title: str
    start_time: datetime
    duration_minutes: int
    participant_emails: List[EmailStr]

class MeetingOut(BaseModel):
    id: UUID
    title: str
    start_time: datetime
    duration: timedelta
    organizer: UserOut
    participants: List[UserOut]

    @computed_field
    @property
    def duration_minutes(self) -> int:
        return int(self.duration.total_seconds() // 60)

    @computed_field
    @property
    def organizer_email(self) -> EmailStr:
        return self.organizer.email

    @computed_field
    @property
    def participant_emails(self) -> List[EmailStr]:
        return [p.email for p in self.participants]

    class Config:
        from_attributes = True

class MeetingUpdate(BaseModel):
    title: Optional[str]
    start_time: Optional[datetime]
    duration_minutes: Optional[int]
    participant_ids: Optional[List[str]]

class MeetingsPaginatedResponse(BaseModel):
    data: List[MeetingOut]
    count_data: int

    class Config:
        from_attributes = True
