from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select, delete
from app.models.user import User
from app.models.registration import Registration

router = APIRouter(prefix="/users")


@router.get("/")
#restituisce la lista di tutti gli utenti
def get_all_users(session: SessionDep) -> list[User]:
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.post("/")
#aggiungiamo un utente
def create_user(user: User, session: SessionDep):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    return {"messagge": f"User {new_user.username} created successfully"}


@router.delete("/")
#eliminiamo tutti gli utenti
def delete_all_users(session: SessionDep):
    statement = delete(User)
    session.exec(statement)
    session.commit()
    return "All Users successfully deleted"


@router.delete("/{username}")
#eliminiamo un determinato utente e le sue registrazioni
def delete_user(
        session: SessionDep,
        username: Annotated[str, Path(description="the username of the user to delete")]):
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # elimina tutte le registrazioni dell'utente
    registration = session.exec(
        select(Registration).where(Registration.username == username)).all()
    for reg in registration:
        session.delete(reg)
    #elimina l'utente
    session.delete(user)
    session.commit()
    return "User successfully deleted"


@router.get("/{username}")
#restituisce i dati di un utente dato un determinato username
def get_user_by_username(session: SessionDep,
                         username: Annotated[str, Path(description="the username of the user to delete")]) -> User:
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
