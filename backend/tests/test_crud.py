import pytest
from app import crud, schemas

def test_create_user(db_session):
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpass")
    user = crud.create_user(db_session, user_in)
    assert user.username == user_in.username
    assert user.email == user_in.email
    assert user.hashed_password != user_in.password

def test_authenticate_user(db_session):
    user_in = schemas.UserCreate(username="authuser", email="auth@example.com", password="secret")
    crud.create_user(db_session, user_in)
    
    user = crud.authenticate_user(db_session, "authuser", "secret")
    assert user is not None
    user_fail = crud.authenticate_user(db_session, "authuser", "wrongpass")
    assert user_fail is False

def test_create_and_get_sweet(db_session):
    owner = crud.create_user(db_session, schemas.UserCreate(username="owner", email="owner@example.com", password="pass"))
    sweet_in = schemas.SweetCreate(
        name="Chocolate",
        description="Tasty",
        price=100,
        category="Dessert",    
        quantity=5
    )
    sweet = crud.create_sweet(db_session, sweet_in, owner.id)
    assert sweet.name == sweet_in.name
    sweets = crud.get_sweets(db_session)
    assert len(sweets) >= 1