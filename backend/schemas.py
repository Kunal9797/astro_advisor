from pydantic import BaseModel, EmailStr
from typing import Optional, List
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

class PhilosophyBase(BaseModel):
    name: str
    description: str
    origin: str
    key_principles: List[str]

class Philosophy(PhilosophyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReligionBase(BaseModel):
    name: str
    description: str
    sacred_texts: List[str]
    practices: List[str]

class Religion(ReligionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AstrologicalSystemBase(BaseModel):
    name: str
    origin: str
    description: str
    key_concepts: List[str]
    zodiac_signs: List[str]

class AstrologicalSystem(AstrologicalSystemBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True