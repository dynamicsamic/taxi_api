from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import City, Customer


class CityRepository(SQLAlchemyAsyncRepository[City]):
    model_type = City


class CustomerRepository(SQLAlchemyAsyncRepository[Customer]):
    model_type = Customer


class CityService(SQLAlchemyAsyncRepositoryService[City]):
    repository_type = CityRepository


class CustomerService(SQLAlchemyAsyncRepositoryService[Customer]):
    repository_type = CustomerRepository
