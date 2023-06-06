import os
from sys import modules

from sqlmodel import SQLModel
from app import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

db_connection_str = settings.database_url
if "pytest" in modules:
    db_connection_str = settings.test_database_url


async_engine = create_async_engine(db_connection_str, echo=True, future=True)


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
