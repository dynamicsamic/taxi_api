import pytest

from src.repository import CityService, CustomerService

pytestmark = pytest.mark.asyncio

CITY_COUNT = 20
CUSTOMER_COUNT = 49171


async def test_models(test_session):
    cities = CityService(test_session)
    customers = CustomerService(test_session)
    assert await cities.count() == CITY_COUNT
    assert await customers.count() == CUSTOMER_COUNT
