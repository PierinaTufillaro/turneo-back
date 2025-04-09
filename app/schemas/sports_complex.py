from pydantic import BaseModel
from typing import Optional

class SportsComplexBase(BaseModel):
    name: str
    slug: str
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class SportsComplexCreate(SportsComplexBase):
    pass

class SportsComplexUpdate(SportsComplexBase):
    pass

class SportsComplexOut(SportsComplexBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
