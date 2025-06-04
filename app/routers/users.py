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
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.post("/")
def create_user(user: UserCreate, session: SessionDep):
    """Create a new user"""
    existing_user = session.get(User, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    return {"messagge": f"User {new_user.username} created successfully"}


@router.delete("/")
def delete_all_users(session: SessionDep):
    """Delete all users and all their registrations"""
    session.exec(delete(Registration))
    session.exec(delete(User))
    session.commit()
    return "All Users successfully deleted"


@router.delete("/{username}")
def delete_user(
        session: SessionDep,
        username: Annotated[str, Path(description="the username of the user to delete")]):
    """Delete a user and his registrations"""
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    registration = session.exec(
        select(Registration).where(Registration.username == username)).all()
    for reg in registration:
        session.delete(reg)
    session.delete(user)
    session.commit()
    return "User successfully deleted"


@router.get("/{username}")
def get_user_by_username(session: SessionDep,
                         username: Annotated[str, Path(description="the username of the user to delete")]) -> User:
    """Returns a user with the given username"""
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
