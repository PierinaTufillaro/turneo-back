from pydantic import BaseModel
from datetime import time


class CourtAvailabilityBase(BaseModel):
    court_id: int
    weekday: int  # 0 = Sunday, ..., 6 = Saturday
    start_time: time
    end_time: time


class CourtAvailabilityCreate(CourtAvailabilityBase):
    pass


class CourtAvailabilityOut(CourtAvailabilityBase):
    id: int

    class Config:
        orm_mode = True
