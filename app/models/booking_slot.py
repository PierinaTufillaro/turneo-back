from sqlalchemy import Column, Integer, Time, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class BookingSlot(Base):
    __tablename__ = "booking_slot"

    id = Column(Integer, primary_key=True, index=True)
    court_id = Column(Integer, ForeignKey("court.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    status = Column(String, default="available")  # available / reserved / cancelled

    court = relationship("Court", back_populates="booking_slots")
