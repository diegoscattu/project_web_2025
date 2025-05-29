from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from sqlmodel import select
from typing import Annotated
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User

router = APIRouter(prefix="/registrations")


@router.get("/")
def list_all_registrations(session: SessionDep) -> list[Registration]:
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/")
def delete_registration(session: SessionDep,
    username: str = select(Registration.username),
    event_id: int = select(Event.id)

):
    registration = session.exec(
        select(Registration).where(
            (Registration.username == username) & (Registration.event_id == event_id)
        )
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()
    return {"message": f"Registration for user {username} on event {event_id} deleted"}

