from fastapi import APIRouter
from app.data.db import SessionDep
from sqlmodel import select,delete
from app.models.registration import Registration

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_registrations(session: SessionDep)->list[Registration]:
    statement= select(Registration)
    event=session.exec(statement).all()
    return event