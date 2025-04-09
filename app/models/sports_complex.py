from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class SportsComplex(Base):
    __tablename__ = "sports_complex"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)  # Para URLs públicas
    address = Column(String)
    city = Column(String)
    province = Column(String)
    phone = Column(String)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    owner = relationship("User", back_populates="complexes")
    courts = relationship("Court", back_populates="complex", cascade="all, delete")
