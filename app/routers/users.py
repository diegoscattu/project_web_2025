from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select, delete
from app.models.user import User

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(session: SessionDep) -> list[User]:
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.post("/")
def create_user(user: User, session: SessionDep):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    return {"messagge": f"User {new_user.username} created successfully"}


@router.delete("/")
def delete_all_users(session: SessionDep):
    statement = delete(User)
    session.exec(statement)
    session.commit()
    return "All Users successfully deleted"


@router.delete("/{username}")
def delete_user(
        session: SessionDep,
        username: Annotated[str, Path(description="the username of the user to delete")]):
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return "User successfully deleted"


@router.get("/{username}")
def get_user_by_username(session: SessionDep,
                         username: Annotated[str, Path(description="the username of the user to delete")]) -> User:
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
