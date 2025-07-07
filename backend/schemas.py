# 📁 File: backend/schemas.py

from pydantic import BaseModel, EmailStr

# 🎯 Incoming request body for /auth/register
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 🎯 Outgoing response after successful registration
class UserOut(BaseModel):
    id: int
    email: EmailStr

# Used when user sends credentials to login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Used to return token upon successful login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


model_config = {
    "from_attributes": True
}
