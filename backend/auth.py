# 📁 File: backend/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import UserCreate, UserOut, UserLogin, Token
from utils import hash_password, verify_password, create_access_token

router = APIRouter()


# ------------------------------------------------------------
# 🔐 Route: POST /auth/register
# Registers a new user with email + password
# ------------------------------------------------------------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 🔎 Check if email already exists in database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔒 Hash the user's password before storing it
    hashed_pw = hash_password(user.password)

    # 🧱 Create a new User object
    new_user = User(email=user.email, hashed_password=hashed_pw)

    # 💾 Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Return the created user (excluding password)
    return new_user


# ------------------------------------------------------------
# 🔐 Route: POST /auth/login
# Authenticates user and returns JWT token
# ------------------------------------------------------------
@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # 🔎 Check if user with this email exists
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 🔑 Generate JWT token with user's email
    access_token = create_access_token(data={"sub": user.email})

    # 🪪 Return token payload
    return {"access_token": access_token, "token_type": "bearer"}
