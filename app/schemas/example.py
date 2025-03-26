from pydantic import BaseModel


class ExampleResponse(BaseModel):
    id: int
    name: str
