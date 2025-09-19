from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, crud, models
from app.db import get_db
from app.dependencies import get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/sweets", tags=["sweets"])

def admin_only(user: models.User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/", response_model=schemas.Sweet)
def add_sweet(sweet: schemas.SweetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_sweet(db, sweet, current_user.id)

@router.get("/", response_model=List[schemas.Sweet])
def get_sweets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_sweets(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[schemas.Sweet])
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return crud.search_sweets(db, name, category, price_min, price_max)

@router.put("/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(sweet_id: int, sweet: schemas.SweetUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.update_sweet(db, sweet_id, sweet)

@router.delete("/{sweet_id}", status_code=204)
def delete_sweet(sweet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(admin_only)):
    crud.delete_sweet(db, sweet_id)
    return

@router.post("/{sweet_id}/purchase")
def purchase_sweet(sweet_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.purchase_sweet(db, sweet_id)
    return {"detail": "Purchase successful"}

@router.post("/{sweet_id}/restock")
def restock_sweet(sweet_id: int, quantity: int, db: Session = Depends(get_db), current_user: models.User = Depends(admin_only)):
    crud.restock_sweet(db, sweet_id, quantity)
    return {"detail": "Restock successful"}