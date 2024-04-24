import pytest_asyncio
from advanced_alchemy.base import UUIDBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.loaddata import load_data
from src.models import CityService
from src.utils import db_session, drop_tables

test_engine = create_async_engine("sqlite+aiosqlite://", echo=True)
async_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def test_session():
    async with db_session(async_session) as session:
        await load_data(test_engine, session)
        yield session
    async with test_engine.begin() as conn:
        await drop_tables(conn, UUIDBase)


@pytest_asyncio.fixture
async def cityservice(test_session):
    return CityService(test_session)
