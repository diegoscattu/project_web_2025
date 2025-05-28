from fastapi import APIRouter
from app.data.db import SessionDep
from sqlmodel import select
from app.models.user import User

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session:SessionDep)->list[User]:
    statement= select(User)
    users=session.exec(statement).all()
    return users

@router.post("/")
def create_user(user:User,session:SessionDep):
    new_user= User(**user.dict())
    session.add(new_user)
    session.commit()
    return {"messagge": f"User {new_user.username} created successfully"}