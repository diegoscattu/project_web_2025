from fastapi import APIRouter,HTTPException,Path
from app.data.db import SessionDep
from sqlmodel import select
from typing import Annotated
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User

router = APIRouter(prefix="/events")

@router.get("/")
def get_all_registrations(session: SessionDep)->list[Registration]:
    statement= select(Registration)
    event=session.exec(statement).all()
    return event

@router.post("/{id}/register", response_model=User)
def register_user_to_event(
    id: Annotated[int, Path(description="ID of the event")],
    user: User,
    session: SessionDep
) -> User:
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    new_user = User(**user.dict(), event_id=id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

