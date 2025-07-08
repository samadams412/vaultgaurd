# 📁 File: backend/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, Cookie, Response
from sqlalchemy.orm import Session
from uuid import uuid4
from db import get_db
from models import User, TokenBlacklist
from schemas import UserCreate, UserOut, UserLogin, Token
from jose import JWTError, jwt
from utils import SECRET_KEY, ALGORITHM
from utils import hash_password, verify_password, create_access_token, create_refresh_token
from dependencies import get_current_user
from security import create_password_reset_token, verify_password_reset_token

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
def login(user_credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    jti = str(uuid4())  # Generate a JTI for access token
    access_token = create_access_token(data={"sub": user.email, "jti": jti})

    # Still generate refresh token separately
    refresh_token, refresh_jti = create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/auth"
    )

    return {"access_token": access_token, "token_type": "bearer"}

# ------------------------------------------------------------
# 🔐 Route: GET /auth/me
# Returns the current user based on JWT token
# ------------------------------------------------------------

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# ------------------------------------------------------------
# 📩 Route: POST /auth/request-password-reset
# Accepts email, returns a secure reset token (dev only)
# ------------------------------------------------------------
@router.post("/request-password-reset", status_code=status.HTTP_200_OK)
def request_password_reset(email: str, db: Session = Depends(get_db)):
    # 🔎 Check if user exists with this email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email not found")

    # 🔐 Generate secure reset token
    reset_token = create_password_reset_token(user.email)

    # ✉️ In production, send via email — for now return it
    return {"reset_token": reset_token}

# ------------------------------------------------------------
# 🔑 Route: POST /auth/reset-password
# Accepts token + new password, updates password securely
# ------------------------------------------------------------
@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    # ✅ Verify the token
    email = verify_password_reset_token(token)
    if email is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # 🔎 Look up user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔒 Hash the new password
    user.hashed_password = hash_password(new_password)

    # 💾 Save changes
    db.commit()

    return {"message": "Password updated successfully"}


@router.post("/logout")
def logout(
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        # ❌ Add to blacklist
        db.add(TokenBlacklist(jti=jti))
        db.commit()

        # 🧼 Clear the refresh_token cookie
        response.delete_cookie("refresh_token", path="/auth")

        return {"message": "Logged out successfully"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    
# 🧠 Refresh access token using HTTP-only cookie
@router.post("/refresh", response_model=Token)
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)  # 🔍 Read refresh_token from HTTP-only cookie
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        email = payload.get("sub")

        # ❌ Check if token is blacklisted
        blacklisted = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()
        if blacklisted:
            raise HTTPException(status_code=401, detail="Token has been revoked")

        # 🔑 Issue new access token
        new_access_token = create_access_token(data={"sub": email})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")