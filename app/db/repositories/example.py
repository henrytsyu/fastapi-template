from typing import List
from sqlmodel import Session, select
from . import GenericRepository
from app.db.models.base.example import Example


class ExampleRepository(GenericRepository[Example]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Example)

    def find_by_name(self, name: str) -> List[Example]:
        stmt = select(Example).where(Example.name == name)
        return list(self._session.exec(stmt).all())
