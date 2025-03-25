from types import TracebackType
from typing import Iterator, Self
from fastapi import Depends
from sqlmodel import Session

from . import get_session
from .repositories.example import ExampleRepository


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        self.examples = ExampleRepository(self._session)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()


def get_unit_of_work(session: Session = Depends(get_session)) -> Iterator[UnitOfWork]:
    with UnitOfWork(session) as uow:
        yield uow
