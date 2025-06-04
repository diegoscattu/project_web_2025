from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select, delete
from app.models.user import User, UserCreate
from app.models.registration import Registration

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(session: SessionDep) -> list[User]:
    """Returns the list of all users"""
    # Restituisco la lista di tutti gli utenti
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.post("/")
def create_user(user: UserCreate, session: SessionDep):
    """Create a new user"""
    existing_user = session.get(User, user.username)
    # Controllo se l'username non è già presente
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Passo i parametri in ingresso alla funzione
    new_user = User(**user.dict())
    # Creo il nuovo utente
    session.add(new_user)
    session.commit()
    return {"messagge": f"User {new_user.username} created successfully"}


@router.delete("/")
def delete_all_users(session: SessionDep):
    """Delete all users and all their registrations"""
    # Elimino tutte le registrazioni
    session.exec(delete(Registration))
    # Elimino tutti gli utenti
    session.exec(delete(User))
    session.commit()
    return "All Users successfully deleted"


@router.delete("/{username}")
def delete_user(
        session: SessionDep,
        username: Annotated[str, Path(description="the username of the user to delete")]):
    """Delete a user and his registrations"""
    user = session.get(User, username)
    # Controllo se l'utente esiste
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Apro le registrazioni relative all'username dato
    registration = session.exec(
        select(Registration).where(Registration.username == username)).all()
    # Elimino le registrazioni
    for reg in registration:
        session.delete(reg)
    # Elimino l'utente con l'username dato
    session.delete(user)
    session.commit()
    return "User successfully deleted"


@router.get("/{username}")
def get_user_by_username(session: SessionDep,
                         username: Annotated[str, Path(description="the username of the user to delete")]) -> User:
    """Returns a user with the given username"""
    user = session.get(User, username)
    # Controllo se l'user esiste
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
