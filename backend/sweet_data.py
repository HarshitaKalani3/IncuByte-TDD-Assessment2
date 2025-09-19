# seed_data.py
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app import models
import sqlalchemy.exc

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

# Fixed list of sweets
fixed_sweets = [
    {"name": "Gulab Jamun", "description": "Sweet fried dough balls soaked in syrup", "price": 100, "quantity": 20, "category": "Indian"},
    {"name": "Rasgulla", "description": "Soft spongy syrupy balls", "price": 90, "quantity": 15, "category": "Indian"},
    {"name": "Ladoo", "description": "Traditional ball-shaped sweets", "price": 80, "quantity": 30, "category": "Indian"},
    {"name": "Barfi", "description": "Milk-based sweet", "price": 85, "quantity": 25, "category": "Indian"},
    {"name": "Kaju Katli", "description": "Cashew fudge", "price": 120, "quantity": 20, "category": "Indian"},
    {"name": "Halwa", "description": "Flavored Indian dessert", "price": 70, "quantity": 10, "category": "Indian"},
    {"name": "Peda", "description": "Soft, thick milk sweet", "price": 75, "quantity": 20, "category": "Indian"},
    {"name": "Jalebi", "description": "Crispy coil dipped in syrup", "price": 60, "quantity": 15, "category": "Indian"},
    {"name": "Soan Papdi", "description": "Flaky sweet", "price": 50, "quantity": 10, "category": "Indian"},
    {"name": "Cham Cham", "description": "Stuffed cylindrical sweet", "price": 95, "quantity": 12, "category": "Indian"},
]

def seed_fixed_sweets():
    db: Session = SessionLocal()
    try:
        existing = db.query(models.Sweet).count()
        if existing == 0:
            for sweet in fixed_sweets:
                db_sweet = models.Sweet(**sweet, owner_id=1)  # assuming admin user has ID 1
                db.add(db_sweet)
            db.commit()
            print("✅ Fixed menu inserted successfully.")
        else:
            print("⚠️ Sweets table already has data. Delete it first if you want to reseed.")
    except sqlalchemy.exc.SQLAlchemyError as e:
        print("❌ Error inserting data:", str(e))
    finally:
        db.close()

if __name__ == "__main__":
    seed_fixed_sweets()