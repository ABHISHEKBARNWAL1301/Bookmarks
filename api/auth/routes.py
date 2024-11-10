from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime
from models import UserCreate, User
from connection import get_db
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .utils import  create_access_token



# Password hashing setup



AuthRoute = APIRouter(tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create a user endpoint
@AuthRoute.post("/signup")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken. Please choose another one.")
    
    # Create new user
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": f"User {new_user.username} created successfully"}




# Login endpoint to authenticate and get the token
@AuthRoute.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}






