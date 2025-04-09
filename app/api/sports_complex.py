from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import sports_complex as models
from app.schemas.court import CourtOut
from app.db.session import get_db
from app.oauth2 import get_current_user 
from app.models.user import User
from app.schemas.sports_complex import SportsComplexCreate,SportsComplexOut, SportsComplexUpdate


router = APIRouter(prefix="/complexes", tags=["Sports Complexes"])

@router.post("/", response_model=SportsComplexOut)
# def create_complex(complex_data: schemas.SportsComplexCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
def create_complex(complex_data: SportsComplexCreate, db: Session = Depends(get_db)):
    # db_complex = models.SportsComplex(**complex_data.dict(), user_id=current_user.id)
    db_complex = models.SportsComplex(**complex_data.dict(),user_id=1)
    db.add(db_complex)
    db.commit()
    db.refresh(db_complex)
    return db_complex

@router.get("/", response_model=list[SportsComplexOut])
# def get_my_complexes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
def get_my_complexes(db: Session = Depends(get_db)):
    return db.query(models.SportsComplex).filter(models.SportsComplex.user_id == 1).all()

@router.get("/{complex_id}", response_model=SportsComplexOut)
def get_complex(complex_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_complex = db.query(models.SportsComplex).filter(models.SportsComplex.id == complex_id, models.SportsComplex.user_id == current_user.id).first()
    if not db_complex:
        raise HTTPException(status_code=404, detail="Complex not found")
    return db_complex

@router.get("/{complex_id}/courts", response_model=list[CourtOut])
def get_courts_of_my_complex(complex_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar que el complejo pertenece al usuario
    complex = db.query(models.SportsComplex).filter_by(id=complex_id, user_id=current_user.id).first()
    if not complex:
        raise HTTPException(status_code=404, detail="Complex not found or not yours")

    return complex.courts  # gracias a la relación en SQLAlchemy

@router.put("/{complex_id}", response_model=SportsComplexOut)
def update_complex(complex_id: int, complex_data: SportsComplexUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_complex = db.query(models.SportsComplex).filter(models.SportsComplex.id == complex_id, models.SportsComplex.user_id == current_user.id).first()
    if not db_complex:
        raise HTTPException(status_code=404, detail="Complex not found")
    for key, value in complex_data.dict(exclude_unset=True).items():
        setattr(db_complex, key, value)
    db.commit()
    db.refresh(db_complex)
    return db_complex

@router.delete("/{complex_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complex(complex_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_complex = db.query(models.SportsComplex).filter(models.SportsComplex.id == complex_id, models.SportsComplex.user_id == current_user.id).first()
    if not db_complex:
        raise HTTPException(status_code=404, detail="Complex not found")
    db.delete(db_complex)
    db.commit()
    

