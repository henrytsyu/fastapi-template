from fastapi import APIRouter


router = APIRouter()
router.prefix = "/example"
router.tags = ["example"]
