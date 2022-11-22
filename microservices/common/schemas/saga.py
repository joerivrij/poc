from pydantic import BaseModel
from enum import Enum


class SagaBase(BaseModel):
    type: str
    status: str
    uuid: str
    reason: str


class SagaCreate(SagaBase):
    pass
