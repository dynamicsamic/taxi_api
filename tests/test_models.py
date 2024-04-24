import pytest

pytestmark = pytest.mark.asyncio

CITY_COUNT = 20


async def test_foo(cityservice):
    assert await cityservice.count() == CITY_COUNT
