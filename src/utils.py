import importlib
import logging
from contextlib import asynccontextmanager

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from .exceptions import ModelNotFound
from .settings import MODELS_DIR

log_handler = logging.StreamHandler()
log_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - [%(levelname)s] - <%(funcName)s> : %(message)s"
    )
)

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)


def get_model(model_name: str) -> DeclarativeBase:
    """Locate database model.
    Attempts relative import from root directory.

    Args:
        `model_name`: The exact name of your db model.

    Raises:
        `ModuleNotFound`
        `ModelNotFound`

    Returns:
        Your model class.
    """
    try:
        module = importlib.import_module(MODELS_DIR, ".")
    except ModuleNotFoundError:
        logger.error(
            "Models module not found! check your `settings.MODELS_DIR`"
        )
        raise

    try:
        model = getattr(module, model_name)
    except AttributeError as e:
        logger.error(
            f"Model `{model_name}` not found in `.{MODELS_DIR}` module."
        )
        raise ModelNotFound(e)
    return model


async def create_tables(
    async_conn: AsyncConnection, base: DeclarativeBase
) -> None:
    """Create database tables.

    Args:
        `async_conn`: instance of  sqlalchemy `AsyncConnection`.
        `base`: subclass of sqlalchemy `DeclarativeBase`.
    """

    try:
        await async_conn.run_sync(base.metadata.create_all)
    except Exception as e:
        logger.error(
            "Error occured during tables creation! "
            f"Check your database connection: {e}"
        )
        await async_conn.aclose()
        await async_conn.engine.dispose()
        raise


async def drop_tables(async_conn: AsyncConnection, base: DeclarativeBase):
    """Drop database tables.

    Args:
        `async_conn`: instance of  sqlalchemy `AsyncConnection`.
        `base`: subclass of sqlalchemy `DeclarativeBase`.
    """

    try:
        await async_conn.run_sync(base.metadata.drop_all)
    except Exception as e:
        logger.error(
            "Error occured during tables dropping! "
            f"Check your database connection: {e}"
        )
        await async_conn.aclose()
        await async_conn.engine.dispose()
        raise


@asynccontextmanager
async def db_session(async_session: async_sessionmaker):
    """Provide async session.

    Args:
        `async_session`: instance of sqlalchemy `async_sessionmaker`.

    Yields:
        `session`: instance of sqlalchemy `AsyncSession`.
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Error occured during session execution: {e}")
            await session.rollback()
        finally:
            await session.aclose()
            logger.info("Async session closed")


async def check_tables_created(async_conn: AsyncConnection) -> bool:
    """Check if database tables were created.

    Args:
        async_conn: instance of sqlalchemy `AsyncConnection`.

    Returns:
        Boolean check result.
    """
    inspected = await async_conn.run_sync(lambda x: inspect(x))
    tables = await async_conn.run_sync(
        lambda _: [table for table in inspected.get_table_names()]
    )
    return tables != []
