# -----------------------------
# 📁 File: backend/utils.py
# -----------------------------

from jose import jwt, JWTError  # Used to generate and decode JWT tokens
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Loads environment variables from .env file
from passlib.context import CryptContext  # Secure password hashing/verification
import uuid


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
# 🔐 Create short-lived access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔁 Create long-lived refresh token with a unique JTI
def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    jti = str(uuid.uuid4())  # Unique token ID for blacklisting
    to_encode.update({"exp": expire, "jti": jti})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), jti