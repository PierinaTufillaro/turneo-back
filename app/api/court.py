from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.court import Court
from app.models.user import User
from app.models.sports_complex import SportsComplex
from app.schemas.court import CourtCreate, CourtOut
from app.db.session import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/courts", tags=["Courts"])


@router.post("/", response_model=CourtOut)
def create_court(
    court: CourtCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    # if not complex or complex.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to add court to this complex")

    new_court = Court(**court.dict())
    db.add(new_court)
    db.commit()
    db.refresh(new_court)
    return new_court


@router.get("/{complex_id}", response_model=list[CourtOut])
def get_courts_by_complex(
    complex_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    complex = db.query(SportsComplex).filter_by(id=complex_id).first()
    # if not complex or complex.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to view these courts")

    return db.query(Court).filter_by(complex_id=complex_id).all()


@router.put("/{court_id}", response_model=CourtOut)
def update_court(
    court_id: int,
    court_update: CourtCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    court = db.query(Court).filter_by(id=court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this court")

    for field, value in court_update.dict().items():
        setattr(court, field, value)

    db.commit()
    db.refresh(court)
    return court


@router.delete("/{court_id}")
def delete_court(
    court_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    court = db.query(Court).filter_by(id=court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if not complex or complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this court")

    db.delete(court)
    db.commit()
    return {"detail": "Court deleted successfully"}
