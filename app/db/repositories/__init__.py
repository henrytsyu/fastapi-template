from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from sqlmodel import Session, col, select
from sqlalchemy.exc import NoResultFound

from app.db.models import GenericModel


T = TypeVar("T", bound=GenericModel)


class GenericRepository(Generic[T]):
    """Base class for CRUD operations on a GenericModel."""

    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        """Provide the model class to operated on. This should duplicate the generic class type."""

        self._session = session
        self._model_cls = model_cls

    def get_by_id(self, id: int) -> T:
        """Return a single record by id. Raise 404 if not found."""

        try:
            return self._session.get_one(self._model_cls, id)
        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"{self._model_cls.__name__} with id {id} not found",
            )

    def find_by_id(self, id: int) -> Optional[T]:
        """Return a single record by id, or None if not found."""

        return self._session.get(self._model_cls, id)

    def find_by_ids(self, ids: List[int]) -> List[T]:
        """Return a list of records ordered by id."""

        stmt = (
            select(self._model_cls)
            .where(col(self._model_cls.id).in_(ids))
            .order_by(col(self._model_cls.id))
        )
        return list(self._session.exec(stmt).all())

    def all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        """Return all records of the model ordered by id. Use limit and offset for pagination."""

        stmt = (
            select(self._model_cls)
            .order_by(col(self._model_cls.id))
            .limit(limit)
            .offset(offset)
        )
        return list(self._session.exec(stmt).all())

    def all_created_after(
        self,
        created_after: datetime,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[T]:
        """Return all records created after a given datetime from newest to oldest."""

        created_at = col(self._model_cls.created_at)
        stmt = (
            select(self._model_cls)
            .where(created_at > created_after)
            .order_by(created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self._session.exec(stmt).all())

    def all_created_before(
        self,
        created_before: datetime,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[T]:
        """Return all records created before a given datetime from newest to oldest."""

        created_at = col(self._model_cls.created_at)
        stmt = (
            select(self._model_cls)
            .where(created_at < created_before)
            .order_by(created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self._session.exec(stmt).all())

    def all_created_between(
        self,
        created_after: datetime,
        created_before: datetime,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[T]:
        """Return all records created within a timeframe from newest to oldest."""

        created_at = col(self._model_cls.created_at)
        stmt = (
            select(self._model_cls)
            .where(created_at < created_before)
            .where(created_at > created_after)
            .order_by(created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self._session.exec(stmt).all())

    def upsert(self, record: T) -> T:
        """Insert or update a record. Return the record with the id and created_at set."""

        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def upsert_all(self, records: List[T]) -> List[T]:
        """Insert or update a list of records."""

        self._session.add_all(records)
        self._session.flush()
        for record in records:
            self._session.refresh(record)
        return records

    def delete(self, id: int) -> None:
        """Delete a record by id."""

        record = self.find_by_id(id)
        if record:
            self._session.delete(record)
            self._session.flush()
