from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.court_availability import CourtAvailabilityCreate, CourtAvailabilityOut
from app.models.user import User
from app.models.court import Court
from app.models.sports_complex import SportsComplex
from app.models.court_availability import CourtAvailability
from app.db.session import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/availability", tags=["Court Availability"])


@router.post("/", response_model=CourtAvailabilityOut)
def create_availability(
    availability: CourtAvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    court = db.query(Court).filter_by(id=availability.court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_avail = CourtAvailability(**availability.dict())
    db.add(new_avail)
    db.commit()
    db.refresh(new_avail)
    return new_avail


@router.get("/{court_id}", response_model=list[CourtAvailabilityOut])
def get_availabilities(
    court_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    court = db.query(Court).filter_by(id=court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(CourtAvailability).filter_by(court_id=court_id).all()


@router.put("/{availability_id}", response_model=CourtAvailabilityOut)
def update_availability(
    availability_id: int,
    update_data: CourtAvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    availability = db.query(CourtAvailability).filter_by(id=availability_id).first()
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    court = db.query(Court).filter_by(id=availability.court_id).first()
    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for field, value in update_data.dict().items():
        setattr(availability, field, value)

    db.commit()
    db.refresh(availability)
    return availability


@router.delete("/{availability_id}")
def delete_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    availability = db.query(CourtAvailability).filter_by(id=availability_id).first()
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    court = db.query(Court).filter_by(id=availability.court_id).first()
    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(availability)
    db.commit()
    return {"detail": "Availability deleted"}
