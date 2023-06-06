from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from .repository import UrlRepository


async def get_bityl_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UrlRepository:
    return UrlRepository(session=session)
