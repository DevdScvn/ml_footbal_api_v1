import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)

class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession):
        stmt = select(cls.model).order_by(cls.model.id)
        result = await session.scalars(stmt)
        return result.all()


    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()


    @classmethod
    async def create(cls, data, session: AsyncSession) -> model:
        query = cls.model(**data.model_dump())
        session.add(query)
        await session.commit()
        await session.refresh(query)
        return query