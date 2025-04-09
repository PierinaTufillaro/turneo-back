from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.booking_slot import BookingSlot
from app.models.user import User
from app.models.court import Court
from app.models.sports_complex import SportsComplex
from app.schemas.booking_slot import BookingSlotCreate, BookingSlotOut
from app.db.session import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/booking-slots", tags=["Booking Slots"])


@router.post("/", response_model=BookingSlotOut)
def create_slot(
    slot: BookingSlotCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    court = db.query(Court).filter_by(id=slot.court_id).first()
    if not court:
        raise HTTPException(status_code=404, detail="Court not found")

    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    # if complex.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    new_slot = BookingSlot(**slot.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot


@router.get("/court/{court_id}", response_model=list[BookingSlotOut])
def get_slots_by_court(court_id: int, db: Session = Depends(get_db)):
    return db.query(BookingSlot).filter_by(court_id=court_id).all()


@router.get("/complex/{complex_id}", response_model=list[BookingSlotOut])
def get_slots_by_complex(
    complex_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    courts = db.query(Court).filter_by(complex_id=complex_id).all()
    court_ids = [court.id for court in courts]
    return db.query(BookingSlot).filter(BookingSlot.court_id.in_(court_ids)).all()


@router.put("/{slot_id}", response_model=BookingSlotOut)
def update_slot(
    slot_id: int,
    slot_update: BookingSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slot = db.query(BookingSlot).filter_by(id=slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    court = db.query(Court).filter_by(id=slot.court_id).first()
    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in slot_update.dict().items():
        setattr(slot, key, value)

    db.commit()
    db.refresh(slot)
    return slot


@router.delete("/{slot_id}")
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slot = db.query(BookingSlot).filter_by(id=slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    court = db.query(Court).filter_by(id=slot.court_id).first()
    complex = db.query(SportsComplex).filter_by(id=court.complex_id).first()
    if complex.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(slot)
    db.commit()
    return {"detail": "Slot deleted"}
