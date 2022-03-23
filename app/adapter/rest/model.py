from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    id: Optional[int]
    device_id: int
    lat: float
    long: float
    date: datetime
