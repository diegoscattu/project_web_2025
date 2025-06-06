from fastapi import APIRouter, HTTPException
from app.data.db import SessionDep
from sqlmodel import select
from app.models.registration import Registration
from app.models.event import Event


router = APIRouter(prefix="/registrations")


@router.get("/")
def list_all_registrations(session: SessionDep) -> list[Registration]:
    """Returns the list of all registrations"""
    # Restituisco la lista di tutte le registrazioni agli eventi
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/")
def delete_registration(session: SessionDep,
                        username: str = select(Registration.username),
                        event_id: int = select(Event.id)):
    """Deletes the registration with the given username and event ID"""
    # Apro la registrazione relativa a username e id evento
    registration = session.exec(
        select(Registration).where(
            (Registration.username == username) & (Registration.event_id == event_id)
        )
    ).first()
    # Controllo se la registrazione esiste
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    # Elimino la registrazione
    session.delete(registration)
    session.commit()
    return {"message": f"Registration for user {username} on event {event_id} deleted"}
