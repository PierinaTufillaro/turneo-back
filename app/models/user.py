from sqlalchemy import Column, Integer, String, Enum
from app.db.session import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    client = "client"
    admin = "admin"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), nullable=False)

    complexes = relationship("SportsComplex", back_populates="owner")