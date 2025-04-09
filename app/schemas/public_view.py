from pydantic import BaseModel
from datetime import time, date


class CourtOut(BaseModel):
    id: int
    name: str
    sport: str
    type: str
    hourly_price: float

    class Config:
        orm_mode = True


class SlotOut(BaseModel):
    id: int
    court_id: int
    date: date
    start_time: time
    end_time: time
    status: str

    class Config:
        orm_mode = True


class ComplexOut(BaseModel):
    id: int
    name: str
    slug: str
    address: str
    city: str
    province: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class PublicView(BaseModel):
    complex: ComplexOut
    courts: list[CourtOut]
    slots: list[SlotOut]
