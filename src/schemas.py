from uuid import UUID

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    model_config = {"from_attributes": True}


class City(BaseModel):
    id: UUID
    name: str
    population: int
    users: int


class CityCreate(BaseModel):
    name: str
    population: int
    users: int


class CityUpdate(BaseModel):
    name: str
    population: int
    users: int
