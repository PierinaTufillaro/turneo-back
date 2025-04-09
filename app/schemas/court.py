from pydantic import BaseModel
from typing import Optional


class CourtBase(BaseModel):
    name: str
    sport: str
    type: str
    hourly_price: float
    complex_id: int


class CourtCreate(CourtBase):
    pass


class CourtOut(CourtBase):
    id: int

    class Config:
        orm_mode = True
