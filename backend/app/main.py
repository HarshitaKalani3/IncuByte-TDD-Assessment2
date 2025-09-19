from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List, Optional

from app import models, schemas, crud
from app.db import engine, get_db
from app.security import create_access_token
from app.dependencies import get_current_user
from app.config import get_settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
def admin_only(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access needed")
    return current_user

@app.post("/api/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Already registered")
    return crud.create_user(db, user)

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/sweets", response_model=schemas.Sweet)
def add_sweet(sweet: schemas.SweetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_sweet(db, sweet, current_user.id)

@app.get("/api/sweets", response_model=List[schemas.Sweet])
def get_sweets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_sweets(db, skip=skip, limit=limit)

@app.get("/api/sweets/search", response_model=List[schemas.Sweet])
def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, alias="priceMin"),
    price_max: Optional[float] = Query(None, alias="priceMax"),
    db: Session = Depends(get_db)
):
    return crud.search_sweets(db, name, category, price_min, price_max)

@app.put("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
    sweet_id: int = Path(...),
    sweet: schemas.SweetUpdate = Depends(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_sweet(db, sweet_id, sweet)

@app.delete("/api/sweets/{sweet_id}", status_code=204)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_only)
):
    crud.delete_sweet(db, sweet_id)
    return

@app.post("/api/sweets/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    crud.purchase_sweet(db, sweet_id)
    return {"detail": "Purchase successful"}

@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    quantity: int = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(admin_only)
):
    crud.restock_sweet(db, sweet_id, quantity)
    return {"detail": "Restock successful"}