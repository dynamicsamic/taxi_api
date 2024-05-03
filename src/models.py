import datetime as dt
import enum

from advanced_alchemy.base import UUIDBase
from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = UUIDBase


class AbstractBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def _fmt(self, description: str) -> str:
        """Return nice-looking model instance description.

        Args:
            description: model description

        Returns:
            Formatted description
        """
        return f"{self.__class__.__name__}({description})"


class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"


class PaymentMethod(enum.Enum):
    Card = "Card"
    Cash = "Cash"


class Carrier(AbstractBase):
    __tablename__ = "carriers"

    name: Mapped[str] = mapped_column(String, unique=True)
    trips: Mapped[list["Trip"]] = relationship(
        back_populates="carrier", cascade="save-update, merge", lazy="noload"
    )

    def __str__(self) -> str:
        return self._fmt(self.name)


class City(AbstractBase):
    __tablename__ = "cities"

    name: Mapped[str]
    population: Mapped[int]
    users: Mapped[int]
    trips: Mapped[list["Trip"]] = relationship(
        back_populates="city", cascade="save-update, merge", lazy="noload"
    )

    def __str__(self) -> str:
        return self._fmt(
            f"{self.name}, {self.population} people, {self.users} users"
        )


class Customer(AbstractBase):
    __tablename__ = "customers"

    gender: Mapped[Enum] = mapped_column(
        Enum(Gender, create_constraint=True, validate_strings=True)
    )
    age: Mapped[int]
    month_income: Mapped[int]
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="customer",
        cascade="delete, merge, save-update",
        passive_deletes=True,
        lazy="noload",
    )

    def __str__(self) -> str:
        return self._fmt(
            f"{self.gender.value}, {self.age} years, ${self.month_income}"
        )


class Transaction(AbstractBase):
    __tablename__ = "transactions"

    payment_method: Mapped[Enum] = mapped_column(
        Enum(PaymentMethod, create_constraint=True, validate_strings=True)
    )
    customer: Mapped[Customer] = relationship(back_populates="transactions")
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    trip: Mapped["Trip"] = relationship(back_populates="transaction")

    def __str__(self) -> str:
        return self._fmt(
            f"CustomerId {self.customer_id}, {self.payment_method.value}"
        )


class Trip(AbstractBase):
    __tablename__ = "trips"

    date: Mapped[dt.date] = mapped_column(Date, default=dt.date.today())
    distance: Mapped[int]
    price: Mapped[int]
    cost: Mapped[int]
    transaction: Mapped[Transaction] = relationship(back_populates="trip")
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="RESTRICT")
    )
    carrier: Mapped[Carrier] = relationship(back_populates="trips")
    carrier_id: Mapped[int] = mapped_column(
        ForeignKey("carriers.id", ondelete="RESTRICT")
    )
    city: Mapped[City] = relationship(back_populates="trips")
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="RESTRICT")
    )

    __table_args__ = (UniqueConstraint("transaction_id"),)

    def __str__(self) -> str:
        return self._fmt(
            f"{self.date}, {self.distance} km, $ {self.price}, "
            f"CarrierId {self.carrier_id}, CityId {self.city_id}"
        )


db_engine = create_async_engine("sqlite+aiosqlite:///test.sqlite", echo=True)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)
