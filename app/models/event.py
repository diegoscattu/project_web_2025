from sqlmodel import SQLModel, Field
from datetime import datetime

# Creo le classi per gli eventi e la creazione degli eventi
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str


class EventCreate(SQLModel):
    title: str
    description: str
    date: datetime
    location: str
