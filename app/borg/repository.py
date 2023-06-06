from __future__ import annotations

from uuid import UUID
from typing import List

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Url
from .schemas import UrlBase, UrlPatch


class UrlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Url]:
        statement = select(Url)
        results = await self.session.execute(statement=statement)
        urls = results.scalars().all()  # type: list[Url]
        return urls

    async def create(self, data: UrlBase) -> Url:
        values = data.dict()

        hero = Url(**values)
        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)

        return hero

    async def get(self, id: str | UUID) -> Url:
        statement = select(Url).where(Url.id == id)
        results = await self.session.execute(statement=statement)
        url = results.scalar_one_or_none()  # type: Url | None
        return url

    async def get_by_code(self, code: str) -> Url:
        statement = select(Url).where(Url.code == code)
        results = await self.session.execute(statement=statement)
        url = results.scalar_one_or_none()
        return url

    async def get_by_short_url(self, short_url: str) -> Url:
        statement = select(Url).where(Url.short_url == short_url)
        results = await self.session.execute(statement=statement)
        url = results.scalar_one_or_none()
        return url

    async def get_by_original_url(self, original_url: str) -> Url:
        statement = select(Url).where(Url.original_url == original_url)
        results = await self.session.execute(statement=statement)
        url = results.scalar_one_or_none()
        return url

    async def patch(self, id: str | UUID, data: UrlPatch) -> Url:
        url = await self.get(id=id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(url, k, v)

        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url

    async def delete(self, id: str | UUID) -> bool:
        statement = delete(Url).where(Url.id == id)

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
