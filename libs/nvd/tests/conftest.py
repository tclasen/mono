import os
from collections.abc import AsyncGenerator

import pytest
from nvd import Nvd
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture(params=[pytest.param("", marks=pytest.mark.integration)])
def engine() -> AsyncEngine:
    return create_async_engine("sqlite+aiosqlite:///", echo=True)


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session_:
        yield session_


@pytest.fixture(params=[pytest.param("", marks=pytest.mark.integration)])
def nvd_api_key() -> str | None:
    return os.environ.get("NVD_API_KEY")


@pytest.fixture
def nvd(session: AsyncSession, nvd_api_key: str | None) -> Nvd:
    return Nvd(session, nvd_api_key)
