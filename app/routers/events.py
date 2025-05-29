from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select, delete
from app.models.event import Event, EventCreate
from app.models.user import User
from app.models.registration import Registration, RegistrationCreate


router = APIRouter(prefix="/events")


@router.get("/")
def get_all_events(session: SessionDep) -> list[Event]:
    statement = select(Event)
    event = session.exec(statement).all()
    return event


@router.post("/")
def create_event(event: EventCreate, session: SessionDep):
    new_event = Event(**event.dict())
    session.add(new_event)
    session.commit()
    return {"messagge": f"Event {new_event.title} created successfully"}


@router.delete("/")
def delete_all_events(session: SessionDep):
    statement = delete(Event)
    session.exec(statement)
    session.commit()
    return "All Events successfully deleted"


@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path(description="the id of the event to delete")]):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return "Event successfully deleted"


@router.get("/{id}")
def get_event_by_id(session: SessionDep,
                    id: Annotated[int, Path(description="the id of the event to delete")]) -> Event:
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: Annotated[int, Path(description="the id of the event to update")],
        new_event: EventCreate
):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()
    return "event successfully update"


@router.post("/{id}/register")
def register_user_to_event(
    id: Annotated[int, Path(description="ID of the event")],
    registration: RegistrationCreate,
    session: SessionDep
):
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # Verifica utente esistente
    user = session.get(User, registration.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica registrazione duplicata
    existing = session.exec(
        select(Registration).where(
            (Registration.event_id == id) & (Registration.username == registration.username)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    new_registration = Registration(username=registration.username, event_id=id)
    session.add(new_registration)
    session.commit()
    session.refresh(new_registration)
    return new_registration
