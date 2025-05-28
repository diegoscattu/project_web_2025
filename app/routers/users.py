from fastapi import APIRouter
from sqlmodel import select
from data.db import SessionDep
from app.models.user import User


router= APIRouter(prefix="/users")

@router.get("/users")
def get_all_users(session: SessionDep)-> list[User]:
    """" returns all users """
    statement= select(User)
    users = session.exec(statement).all()
    return users



