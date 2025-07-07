# 📁 File: backend/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import UserCreate, UserOut
from utils import hash_password

router = APIRouter()

# ------------------------------------------------------------
# 🔐 Route: POST /auth/register
# Registers a new user with email + password
# ------------------------------------------------------------
@router.post("/auth/register", response_model=UserOut)
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
