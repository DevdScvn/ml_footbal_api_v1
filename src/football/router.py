from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from football.fb_dao import MatchDAO

router = APIRouter(prefix="/prediction", tags=["football"])


@router.get("")
async def get_all(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    """
    pass
    """
    return await MatchDAO.find_all(session)


