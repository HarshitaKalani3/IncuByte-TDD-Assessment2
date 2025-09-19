from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: Optional[str] = "user"
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SweetBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: Optional[int] = 0
    category: Optional[str] = None

class SweetCreate(SweetBase):
    pass

class Sweet(SweetBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)