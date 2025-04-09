from pydantic import BaseModel
from datetime import date, time


class BookingSlotBase(BaseModel):
    court_id: int
    date: date
    start_time: time
    end_time: time
    status: str = "available"


class BookingSlotCreate(BookingSlotBase):
    pass


class BookingSlotOut(BookingSlotBase):
    id: int

    class Config:
        orm_mode = True
