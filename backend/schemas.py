from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    birth_date: str
    birth_time: Optional[str] = None
    location: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInput(BaseModel):
    name: str
    birth_date: str
    birth_time: Optional[str] = None
    location: str

class ReadingBase(BaseModel):
    name: str
    birth_date: str
    birth_time: Optional[str] = None
    location: str
    advice: str

class ReadingCreate(ReadingBase):
    pass

class Reading(ReadingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    location: Optional[str] = None