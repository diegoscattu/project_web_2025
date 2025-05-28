from sqlmodel import SQLModel,Field
from datetime import datetime

class Event(SQLModel, table= True):
    title:str
    description:str
    date:datetime
    location: str
    id: int = Field(default=None, primary_key=True)

