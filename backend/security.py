# -----------------------------
# 📁 File: backend/security.py
# -----------------------------
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# 🔑 Secret + Config
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 15  # ⏳ 15-minute expiration

# -------------------------------------------------------
# 🔐 Create a short-lived password reset token
# -------------------------------------------------------
def create_password_reset_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------------------------------------------
# ✅ Verify token + extract email if valid
# -------------------------------------------------------
def verify_password_reset_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # 📧 the email we encoded
    except JWTError:
        return None
