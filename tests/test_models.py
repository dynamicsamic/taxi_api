import pytest
import pytest_asyncio

from src.repository import CarrierService, CityService, TripService

pytestmark = pytest.mark.asyncio


CITY_MODELFIELDS = {"name": str, "population": int, "users": int, "id": int}
CARIER_MODELFIELDS = {"name": str, "id": int}


@pytest_asyncio.fixture(scope="module")
async def cityservice(create_test_tables):
    return CityService(create_test_tables)


@pytest_asyncio.fixture(scope="module")
async def carierservice(create_test_tables):
    return CarrierService(create_test_tables)


@pytest_asyncio.fixture(scope="module")
async def tripservice(create_test_tables):
    return TripService(create_test_tables)


async def test_carier_modelfields(carierservice):
    carier = await carierservice.get_one_or_none(id=1)
    carier_dict = carier.to_dict()

    assert all(
        [
            type(carier_dict[fieldname]) is fieldtype
            for fieldname, fieldtype in CARIER_MODELFIELDS.items()
        ]
    )


async def test_carier_noloads_trips(carierservice):
    carier = await carierservice.get_one_or_none(id=1)
    assert carier.trips == []


async def test_city_modelfields(cityservice):
    city = await cityservice.get_one_or_none(id=1)
    city_dict = city.to_dict()

    assert all(
        [
            type(city_dict[fieldname]) is fieldtype
            for fieldname, fieldtype in CITY_MODELFIELDS.items()
        ]
    )


async def test_city_noloads_trips(cityservice):
    city = await cityservice.get_one_or_none(id=1)
    assert city.trips == []
