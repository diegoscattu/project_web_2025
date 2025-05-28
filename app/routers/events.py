from fastapi import APIRouter
from app.data.db import SessionDep
from sqlmodel import select
from app.models.event import Event

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_events(session: SessionDep)->list[Event]:
    statement= select(Event)
    event=session.exec(statement).all()
    return event