from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta

class MeetingCreate(BaseModel):
    title: str
    start_time: datetime
    duration_minutes: int
    participant_emails: List[EmailStr]

class MeetingOut(BaseModel):
    id: str
    title: str
    start_time: datetime
    duration_minutes: int
    organizer_email: EmailStr
    participant_emails: List[EmailStr]

    class Config:
        from_attributes = True  # Pydantic v2

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
