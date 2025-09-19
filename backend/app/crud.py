from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas
from app.security import get_password_hash, verify_password
from fastapi import HTTPException, status

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_sweet(db: Session, sweet: schemas.SweetCreate, user_id: int):
    db_sweet = models.Sweet(**sweet.model_dump(), owner_id=user_id)
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def get_sweets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Sweet).offset(skip).limit(limit).all()

def search_sweets(db: Session, name: str = None, category: str = None, price_min: float = None, price_max: float = None):
    query = db.query(models.Sweet)
    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if price_min is not None:
        query = query.filter(models.Sweet.price >= price_min)
    if price_max is not None:
        query = query.filter(models.Sweet.price <= price_max)
    return query.all()

def update_sweet(db: Session, sweet_id: int, sweet_update: schemas.SweetUpdate):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    update_data = sweet_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sweet, key, value)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def delete_sweet(db: Session, sweet_id: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db.delete(db_sweet)
    db.commit()

def purchase_sweet(db: Session, sweet_id: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if db_sweet.quantity <= 0:
        raise HTTPException(status_code=400, detail="Sweet is out of stock")
    db_sweet.quantity -= 1
    db.commit()
    db.refresh(db_sweet)

def restock_sweet(db: Session, sweet_id: int, quantity: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db_sweet.quantity += quantity
    db.commit()
    db.refresh(db_sweet)