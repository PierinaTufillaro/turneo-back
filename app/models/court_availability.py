from sqlalchemy import Column, Integer, Time, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship


class CourtAvailability(Base):
    __tablename__ = "court_availability"

    id = Column(Integer, primary_key=True, index=True)
    court_id = Column(Integer, ForeignKey("court.id"))
    weekday = Column(Integer)  # 0 = Sunday, 6 = Saturday
    start_time = Column(Time)
    end_time = Column(Time)

    court = relationship("Court", back_populates="availabilities")