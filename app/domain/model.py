from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    id: Optional[int]
    device_id: int
    lat: float
    long: float
    date: datetime


class User(BaseModel):
    id: int
    nome: str


class Device(BaseModel):
    id: int
    user_id: int
