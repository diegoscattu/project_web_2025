from fastapi import APIRouter, HTTPException, Path
from app.data.db import SessionDep
from sqlmodel import select
from typing import Annotated
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User

router = APIRouter(prefix="/registrations")


@router.get("/")
def list_all_registrations(session: SessionDep) -> list[Registration]:
    registrations = session.exec(select(Registration)).all()
    return registrations


