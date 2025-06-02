from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import os
import random
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.user import User
from app.models.event import Event


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            # TODO: (optional) initialize the database with fake data
            users = []
            events = []
            for i in range(3):
                user = User(
                    username=f.user_name(),
                    name=f.name(),
                    email=f.email()
                )
                session.add(user)
                users.append(user)
            session.commit()
            for i in range(3):
                event = Event(title=f.word(),
                              description=f.text(),
                              date=f.date_time(),
                              location=f.city())
                session.add(event)
                events.append(event)
            session.commit()
            for i in range(1):
                link = Registration(username=random.choice(users).username,
                                    event_id=random.choice(events).id)
                session.add(link)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
