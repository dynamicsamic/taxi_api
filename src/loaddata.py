import csv
import logging

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from .models import Base
from .repository import CityService, CustomerService
from .settings import BASE_DIR, DATA_DIR
from .utils import (
    check_tables_created,
    create_tables,
    log_handler,
)

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)

SERVICE_TO_SOURCE = {CityService: "City.csv", CustomerService: "Customer.csv"}


async def load_modeldata(
    file_name: str,
    service: SQLAlchemyAsyncRepositoryService,
    async_session: AsyncSession,
) -> None:
    """Populate single database table from a source file.

    Args:
        `file_name`: exact name of a source file.
        `service`: instance of advanced_alchemy
            `SQLAlchemyAsyncRepositoryService`
        `async_session`: instance of sqlalchemy `AsyncSession`.
    """
    model = service.repository_type.model_type
    with open(BASE_DIR / DATA_DIR / file_name) as file:
        reader = csv.DictReader(file)
        inserted = await service(async_session).create_many(reader)
        logger.info(
            f"Inserted {len(inserted)} items for model "
            f"`{model.__tablename__.capitalize()}`."
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
            await create_tables(conn, Base)
        for service, file in SERVICE_TO_SOURCE.items():
            await load_modeldata(
                file_name=file, service=service, async_session=async_session
            )
