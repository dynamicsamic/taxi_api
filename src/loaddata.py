import csv
import logging

from advanced_alchemy.base import UUIDBase
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from .models import CityService
from .settings import BASE_DIR, DATA_DIR
from .utils import (
    check_tables_created,
    create_tables,
    get_model,
    log_handler,
)

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)


async def load_modeldata(
    file_name: str,
    model_name: str,
    async_session: AsyncSession,
    service: SQLAlchemyAsyncRepositoryService,
) -> None:
    """Populate single database table from a source file.

    Args:
        `file_name`: exact name of a source file.
        `model_name`: exact name of your model.
        `async_session`: instance of sqlalchemy `AsyncSession`.
        `service`: instance of advanced_alchemy
            `SQLAlchemyAsyncRepositoryService`
    """
    with open(BASE_DIR / DATA_DIR / file_name) as file:
        reader = csv.DictReader(file)
        model = get_model(model_name)
        inserted = await service(async_session).create_many(
            [model(**item) for item in reader]
        )
        logger.info(
            f"Inserted {len(inserted)} items for model `{model_name}`."
        )


async def load_city(async_session: AsyncSession) -> None:
    """Populate `City` table.

    Args:
        `async_session`: instance of sqlalchemy `AsyncSession`.
    """
    await load_modeldata(
        async_session=async_session,
        file_name="City.csv",
        model_name="City",
        service=CityService,
    )


async def load_data(
    async_engine: AsyncEngine,
    async_session: AsyncSession,
) -> None:
    """Populate all database tables.

    Args:
        `async_engine`: instance of sqlalchemy `AsyncEngine`.
        `async_session`: instance of sqlalchemy `AsyncSession`.
    """
    async with async_engine.begin() as conn:
        if not await check_tables_created(conn):
            await create_tables(conn, UUIDBase)
        await load_city(async_session)
