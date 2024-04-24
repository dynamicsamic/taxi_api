from advanced_alchemy.base import UUIDBase
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped


class City(UUIDBase):
    __tablename__ = "city"

    name: Mapped[str]
    population: Mapped[int]
    users: Mapped[int]

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, "
            f"{self.population} people, {self.users} users)"
        )


class CityRepository(SQLAlchemyAsyncRepository[City]):
    model_type = City


class CityService(SQLAlchemyAsyncRepositoryService[City]):
    repository_type = CityRepository


db_engine = create_async_engine("sqlite+aiosqlite:///test.sqlite", echo=True)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)
