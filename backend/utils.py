# -----------------------------
# 📁 File: backend/utils.py
# -----------------------------

from jose import jwt  # Used to generate and decode JWT tokens
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Loads environment variables from .env file
from passlib.context import CryptContext  # Secure password hashing/verification

# ✅ Load variables from .env file (e.g., JWT_SECRET)
load_dotenv()

# 🔐 Configure the password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")  # fallback if .env not present
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Default token lifespan

# ------------------------------------------------------------
# 🔒 Hash a password (e.g., before saving to database)
# ------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ------------------------------------------------------------
# 🔍 Verify a plain password against the stored hashed one
# ------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------------------------------------------
# 🧾 Create a JWT token from user data (e.g., user ID/email)
# ------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()  # Never mutate the original
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Add expiry to payload
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
