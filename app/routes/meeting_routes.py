from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.meeting_schema import MeetingCreate, MeetingUpdate, MeetingOut, MeetingsPaginatedResponse
from app.schemas.user_schema import UserRead
from app.services.meeting_service import (
    get_meeting,
    get_meetings,
    get_meetings_count,
    get_meetings_today_for_user,
    get_meetings_today_for_user_count,
    get_meetings_for_user_paginated,
    get_meetings_for_user_count,
    create_meeting,
    update_meeting,
    get_meeting_participants,
    get_meetings_for_user_paginated,
    get_meetings_for_user_count
)
from app.utils.response import response

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_meeting_route(
    meeting_data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meeting = create_meeting(db, meeting_data, current_user)
    meeting_out = MeetingOut.model_validate(meeting).model_dump()
    return response(
        status_code=201,
        message="Reunión creada exitosamente",
        data=meeting_out
    )

@router.get("/", response_model=MeetingsPaginatedResponse)
async def get_meetings_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meetings = get_meetings(db, skip, limit)
    total = get_meetings_count(db)

    meetings_data = [MeetingOut.model_validate(m).model_dump() for m in meetings]

    return response(
        status_code=200,
        message="Reuniones obtenidas exitosamente",
        data=meetings_data,
        count_data=total,
    )

@router.get("/today", response_model=MeetingsPaginatedResponse)
async def get_meetings_today_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meetings = get_meetings_today_for_user(db, current_user, skip, limit)
    total = get_meetings_today_for_user_count(db, current_user)

    meetings_data = [MeetingOut.model_validate(m).model_dump() for m in meetings]

    return response(
        status_code=200,
        message="Reuniones de hoy del usuario obtenidas exitosamente",
        data=meetings_data,
        count_data=total,
    )

@router.get("/{meeting_id}/participants")
async def get_meeting_participants_route(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    users = get_meeting_participants(meeting)
    if meeting.organizer not in users:
        users.append(meeting.organizer)
    users_data = [UserRead.model_validate(u).model_dump() for u in users]

    return response(
        status_code=200,
        message=f"Participantes de la reunión {meeting_id} obtenidos",
        data=users_data
    )

@router.put("/{meeting_id}", status_code=status.HTTP_200_OK)
async def update_meeting_route(
    meeting_id: UUID,
    meeting_data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    if meeting.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para editar esta reunión")

    meeting = update_meeting(db, meeting, meeting_data)
    meeting_out = MeetingOut.model_validate(meeting).model_dump()
    return response(
        status_code=200,
        message="Reunión actualizada exitosamente",
        data=meeting_out
    )

@router.get("/my", response_model=MeetingsPaginatedResponse)
async def get_my_meetings_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meetings = get_meetings_for_user_paginated(db, current_user, skip, limit)
    total = get_meetings_for_user_count(db, current_user)

    meetings_data = []
    for m in meetings:
        rol = "organizador" if m.organizer_id == current_user.id else "participante"
        meeting_dict = MeetingOut.model_validate(m).model_dump()
        meeting_dict["rol_en_reunion"] = rol
        meetings_data.append(meeting_dict)

    return response(
        status_code=200,
        message="Reuniones del usuario obtenidas correctamente",
        data=meetings_data,
        count_data=total
    )
