from app.schemas.example import ExampleResponse
from . import GenericModel


class Example(GenericModel, table=True):
    name: str

    def to_response(self) -> ExampleResponse:
        return ExampleResponse(id=self.id, name=self.name)
