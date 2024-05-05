from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import Carrier, City, Customer, Transaction, Trip


class CarrierRepository(SQLAlchemyAsyncRepository[Carrier]):
    model_type = Carrier


class CityRepository(SQLAlchemyAsyncRepository[City]):
    model_type = City


class CustomerRepository(SQLAlchemyAsyncRepository[Customer]):
    model_type = Customer


class TransactionRepository(SQLAlchemyAsyncRepository[Transaction]):
    model_type = Transaction


class TripRepository(SQLAlchemyAsyncRepository[Trip]):
    model_type = Trip


class CarrierService(SQLAlchemyAsyncRepositoryService[Carrier]):
    repository_type = CarrierRepository


class CityService(SQLAlchemyAsyncRepositoryService[City]):
    repository_type = CityRepository


class CustomerService(SQLAlchemyAsyncRepositoryService[Customer]):
    repository_type = CustomerRepository


class TransactionService(SQLAlchemyAsyncRepositoryService[Transaction]):
    repository_type = TransactionRepository


class TripService(SQLAlchemyAsyncRepositoryService[Trip]):
    repository_type = TripRepository
