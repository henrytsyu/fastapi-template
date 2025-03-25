from typing import Iterator
from fastapi import FastAPI
from sqladmin import Admin
from sqlmodel import Session, create_engine

from .admin import AdminAuth, views
from app import get_settings


engine = create_engine(get_settings().DATABASE_URL)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def create_admin(app: FastAPI) -> None:
    admin = Admin(app, engine, authentication_backend=AdminAuth())
    for view in views:
        admin.add_view(view)
