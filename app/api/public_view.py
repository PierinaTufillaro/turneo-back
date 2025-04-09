from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.court import Court
from app.models.sports_complex import SportsComplex
from app.models.booking_slot import BookingSlot
from app.schemas.public_view import PublicView
from app.db.session import get_db
from datetime import date

router = APIRouter(prefix="/public", tags=["Public View"])


@router.get("/{complex_slug}", response_model=PublicView)
def view_available_slots(complex_slug: str, db: Session = Depends(get_db)):
    complex = db.query(SportsComplex).filter_by(slug=complex_slug).first()

    if not complex:
        raise HTTPException(status_code=404, detail="Complex not found")

    courts = db.query(Court).filter_by(complex_id=complex.id).all()
    court_ids = [court.id for court in courts]

    today = date.today()
    slots = (
        db.query(BookingSlot)
        .filter(BookingSlot.court_id.in_(court_ids))
        .filter(BookingSlot.date >= today)
        .filter_by(status="available")
        .all()
    )

    return {
        "complex": complex,
        "courts": courts,
        "slots": slots,
    }
