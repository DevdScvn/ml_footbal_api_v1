from fastapi import APIRouter


router = APIRouter(prefix="/prediction", tags=["football"])


@router.get("")
async def get_all():
    return {"msg": "ok"}


