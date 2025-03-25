from datetime import datetime
from sqlmodel import Field, SQLModel


class GenericModel(SQLModel):
    """SQLModel base class with common fields."""

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
