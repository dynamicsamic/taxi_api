import random

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.models import Base, Gender, PaymentMethod
from src.repository import (
    CarrierService,
    CityService,
    CustomerService,
    TransactionService,
    TripService,
)
from src.utils import (
    create_random_date,
    create_tables,
    db_session,
    drop_tables,
)

test_engine = create_async_engine("sqlite+aiosqlite://", echo=True)
async_session = async_sessionmaker(test_engine, expire_on_commit=False)

CARRIER_SIZE = 10
CITY_SIZE = 50
CUSTOMER_SIZE = 10000
TRANSACTION_SIZE = 100
TRIP_SIZE = TRANSACTION_SIZE


async def create_carriers(session):
    await CarrierService(session).create_many(
        [{"id": i, "name": f"carrier{i}"} for i in range(1, CARRIER_SIZE + 1)]
    )


async def create_cities(session):
    await CityService(session).create_many(
        [
            {
                "id": i,
                "name": f"city{i}",
                "population": random.randrange(1000, 2000000),
                "users": random.randrange(10, 100000),
            }
            for i in range(1, CITY_SIZE + 1)
        ]
    )


async def create_customers(session):
    await CustomerService(session).create_many(
        [
            {
                "id": i,
                "gender": random.choice((Gender.Female, Gender.Male)),
                "age": random.randrange(18, 100),
                "month_income": random.randrange(10000, 300000),
            }
            for i in range(1, CUSTOMER_SIZE + 1)
        ]
    )


async def create_transactions(session):
    await TransactionService(session).create_many(
        [
            {
                "id": i,
                "payment_method": random.choice(
                    (PaymentMethod.Card, PaymentMethod.Cash)
                ),
                "customer_id": random.randrange(1, CUSTOMER_SIZE),
            }
            for i in range(1, TRANSACTION_SIZE + 1)
        ]
    )


async def create_trips(session):
    await TripService(session).create_many(
        [
            {
                "id": i,
                "date": create_random_date(),
                "distance": random.randrange(100, 10000),
                "price": random.randrange(1000, 100000),
                "cost": random.randrange(1000, 100000),
                "transaction_id": i,
                "carrier_id": random.randrange(1, CARRIER_SIZE + 1),
                "city_id": random.randrange(1, CITY_SIZE + 1),
            }
            for i in range(1, TRIP_SIZE + 1)
        ]
    )


async def create_test_data(session):
    create_functions = (
        create_carriers,
        create_cities,
        create_customers,
        create_transactions,
        create_trips,
    )
    for fun in create_functions:
        await fun(session)


@pytest_asyncio.fixture(scope="module")
async def create_test_tables():
    async with test_engine.begin() as conn:
        await create_tables(conn, Base)
    async with db_session(async_session) as session:
        await create_test_data(session)
        yield session
    async with test_engine.begin() as conn:
        await drop_tables(conn, Base)
