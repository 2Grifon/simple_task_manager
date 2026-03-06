from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
)

sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
