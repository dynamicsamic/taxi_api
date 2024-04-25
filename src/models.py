import enum

from advanced_alchemy.base import UUIDBase
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column

Base = UUIDBase


class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"


class City(Base):
    __tablename__ = "city"

    name: Mapped[str]
    population: Mapped[int]
    users: Mapped[int]

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, "
            f"{self.population} people, {self.users} users)"
        )


class Customer(Base):
    __tablename__ = "customer"

    gender: Mapped[Enum] = mapped_column(
        Enum(Gender, create_constraint=True, validate_strings=True)
    )
    age: Mapped[int]
    month_income: Mapped[int]

    def __str__(self) -> str:
        return f"{self.gender}, {self.age} years, ${self.month_income}"


db_engine = create_async_engine("sqlite+aiosqlite:///test.sqlite", echo=True)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)
