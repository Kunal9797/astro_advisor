from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
import os
from dotenv import load_dotenv
from openai import OpenAI

from . import models, schemas, auth
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def read_root():
    return {"message": "Welcome to Astro Advisor API"}

@app.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=models.User.hash_password(user.password),
        birth_date=user.birth_date,
        birth_time=user.birth_time,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.verify_token)):
    return current_user

@app.post("/get-advice", response_model=schemas.Reading)
async def get_advice(
    user_input: schemas.UserInput, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.verify_token)
):
    try:
        prompt = f"""
        Provide brief astrological and spiritual advice for:
        Name: {user_input.name}
        Birth Date: {user_input.birth_date}
        Birth Time: {user_input.birth_time or 'Not provided'}
        Location: {user_input.location}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable advisor combining astrological and spiritual wisdom."},
                {"role": "user", "content": prompt}
            ]
        )

        advice = response.choices[0].message.content

        # Create database entry with user_id
        db_reading = models.Reading(
            name=user_input.name,
            birth_date=user_input.birth_date,
            birth_time=user_input.birth_time,
            location=user_input.location,
            advice=advice,
            user_id=current_user.id
        )
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)

        return db_reading

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/readings/", response_model=List[schemas.Reading])
async def get_readings(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.verify_token)
):
    readings = db.query(models.Reading).filter(models.Reading.user_id == current_user.id).offset(skip).limit(limit).all()
    return readings

@app.get("/readings/{reading_id}", response_model=schemas.Reading)
async def get_reading(
    reading_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.verify_token)
):
    reading = db.query(models.Reading).filter(
        models.Reading.id == reading_id,
        models.Reading.user_id == current_user.id
    ).first()
    if reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading

@app.put("/users/me", response_model=schemas.User)
async def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/users/me/readings", response_model=List[schemas.Reading])
async def get_user_readings(
    current_user: models.User = Depends(auth.verify_token),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    readings = db.query(models.Reading)\
        .filter(models.Reading.user_id == current_user.id)\
        .order_by(models.Reading.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return readings

@app.delete("/users/me")
async def delete_user(
    current_user: models.User = Depends(auth.verify_token),
    db: Session = Depends(get_db)
):
    # Delete all user's readings first
    db.query(models.Reading).filter(models.Reading.user_id == current_user.id).delete()
    # Delete the user
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/quick-advice", response_model=schemas.Reading)
async def get_quick_advice(user_input: schemas.UserInput, db: Session = Depends(get_db)):
    try:
        prompt = f"""
        Provide brief astrological and spiritual advice for:
        Name: {user_input.name}
        Birth Date: {user_input.birth_date}
        Birth Time: {user_input.birth_time or 'Not provided'}
        Location: {user_input.location}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable advisor combining astrological and spiritual wisdom."},
                {"role": "user", "content": prompt}
            ]
        )

        advice = response.choices[0].message.content

        # Create database entry without user_id
        db_reading = models.Reading(
            name=user_input.name,
            birth_date=user_input.birth_date,
            birth_time=user_input.birth_time,
            location=user_input.location,
            advice=advice
        )
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)

        return db_reading

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))