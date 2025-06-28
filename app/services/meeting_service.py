from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, date

from app.models.meeting import Meeting
from app.models.user import User

def get_meeting(db: Session, meeting_id: UUID) -> Meeting | None:
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()

def get_meetings(db: Session, skip: int, limit: int) -> list[Meeting]:
    return db.query(Meeting).offset(skip).limit(limit).all()

def get_meetings_count(db: Session) -> int:
    return db.query(Meeting).count()

def get_meetings_today(db: Session, skip: int, limit: int) -> list[Meeting]:
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    return (
        db.query(Meeting)
        .filter(Meeting.start_time >= start_of_day, Meeting.start_time <= end_of_day)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_meetings_today_count(db: Session) -> int:
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    return (
        db.query(Meeting)
        .filter(Meeting.start_time >= start_of_day, Meeting.start_time <= end_of_day)
        .count()
    )

def create_meeting(db: Session, meeting_data, organizer: User) -> Meeting:
    meeting = Meeting(
        title=meeting_data.title,
        start_time=meeting_data.start_time,
        duration=meeting_data.duration,
        organizer_id=organizer.id,
        organizer=organizer,
    )
    if meeting_data.participants:
        participants = db.query(User).filter(User.email.in_(meeting_data.participants)).all()
        meeting.participants = participants

    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

def update_meeting(db: Session, meeting: Meeting, meeting_data) -> Meeting:
    if meeting_data.title is not None:
        meeting.title = meeting_data.title
    if meeting_data.start_time is not None:
        meeting.start_time = meeting_data.start_time
    if meeting_data.duration is not None:
        meeting.duration = meeting_data.duration
    if meeting_data.participants is not None:
        participants = db.query(User).filter(User.email.in_(meeting_data.participants)).all()
        meeting.participants = participants

    db.commit()
    db.refresh(meeting)
    return meeting

def get_meeting_participants(meeting: Meeting) -> list[User]:
    users = {user.id: user for user in meeting.participants}
    users[meeting.organizer.id] = meeting.organizer
    return list(users.values())

def get_meetings_for_user(db: Session, user: User):
    from app.models.meeting import Meeting

    meetings = db.query(Meeting).join(Meeting.participants).filter(
        (Meeting.participants.any(id=user.id)) | (Meeting.organizer_id == user.id)
    ).distinct().all()

    return meetings
