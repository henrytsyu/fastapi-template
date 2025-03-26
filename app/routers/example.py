from typing import List
from fastapi import APIRouter, Depends

from app.db.unit_of_work import UnitOfWork, get_unit_of_work
from app.schemas.example import ExampleResponse


router = APIRouter()
router.prefix = "/examples"
router.tags = ["examples"]


@router.get("/", response_model=List[ExampleResponse])
async def get_examples(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> List[ExampleResponse]:
    return list(map(lambda x: x.to_response(), uow.examples.all()))
