import enum

from advanced_alchemy.base import UUIDBase
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = UUIDBase


class AbstractBase(Base):
    __abstract__ = True

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


class City(AbstractBase):
    __tablename__ = "cities"

    name: Mapped[str]
    population: Mapped[int]
    users: Mapped[int]

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
    )

    def __str__(self) -> str:
        return self._fmt(
            f"{self.gender}, {self.age} years, ${self.month_income}"
        )


class Transaction(AbstractBase):
    __tablename__ = "transactions"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    customer: Mapped[Customer] = relationship(back_populates="transactions")
    payment_method: Mapped[Enum] = mapped_column(
        Enum(PaymentMethod, create_constraint=True, validate_strings=True)
    )

    def __str__(self) -> str:
        return self._fmt(
            f"CustomerId {self.customer_id}, {self.payment_method}"
        )


db_engine = create_async_engine("sqlite+aiosqlite:///test.sqlite", echo=True)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)
