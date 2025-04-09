from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Court(Base):
    __tablename__ = "court"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sport = Column(String)
    type = Column(String)
    hourly_price = Column(Integer)
    complex_id = Column(Integer, ForeignKey("sports_complex.id"), nullable=False)

    complex = relationship("SportsComplex", back_populates="courts")
    availabilities = relationship("CourtAvailability", back_populates="court")
    booking_slots = relationship("BookingSlot", back_populates="court", cascade="all, delete-orphan")
