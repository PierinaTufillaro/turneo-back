from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    client = "client"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    role: Optional[str]

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
