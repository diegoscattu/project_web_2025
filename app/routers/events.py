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
    """Returns the list of all events"""
    # Restituisco la lista di tutti gli eventi
    statement = select(Event)
    event = session.exec(statement).all()
    return event


@router.post("/")
def create_event(event: EventCreate, session: SessionDep):
    """Creates a new event"""
    # Carico i parametri in ingresso
    new_event = Event(**event.dict())
    # Creo il nuovo evento
    session.add(new_event)
    session.commit()
    return {"messagge": f"Event {new_event.title} created successfully"}


@router.delete("/")
def delete_all_events(session: SessionDep):
    """Deletes all events"""
    # Elimino le registrazioni agli eventi
    session.exec(delete(Registration))
    # Elimino tutti gli eventi
    session.exec(delete(Event))
    session.commit()
    return "All Events successfully deleted"


@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path(description="the id of the event to delete")]):
    """Deletes the event with the given ID"""
    event = session.get(Event, id)
    # Controllo se l'id è valido
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Elimino l'evento
    session.delete(event)
    session.commit()
    return "Event successfully deleted"


@router.get("/{id}")
def get_event_by_id(session: SessionDep,
                    id: Annotated[int, Path(description="the id of the event to delete")]) -> Event:
    """Returns an event with the given ID"""
    # Apro l'evento con l'id dato
    event = session.get(Event, id)
    # Controllo se esiste l'evento
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: Annotated[int, Path(description="the id of the event to update")],
        new_event: EventCreate
):
    """Updates the event with the given ID"""
    event = session.get(Event, id)
    # Controllo se l'evento esiste
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Aggiorno i dati dell'evento
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()
    return "Event successfully update"


@router.post("/{id}/register")
def register_user_to_event(
    id: Annotated[int, Path(description="ID of the event")],
    registration: RegistrationCreate,
    session: SessionDep
):
    """Registers a new user to the event with the given ID"""
    event = session.get(Event, id)
    # Controllo se l'evento esiste
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Controllo se l'utente esiste
    user = session.get(User, registration.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Controllo se l'utente è già registrato
    existing = session.exec(
        select(Registration).where(
            (Registration.event_id == id) & (Registration.username == registration.username)
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")
    # Registro l'utente all'evento
    new_registration = Registration(username=registration.username, event_id=id)
    session.add(new_registration)
    session.commit()
    return f"utente:{user.username} registrato con successo all'evento:{event.id}"
