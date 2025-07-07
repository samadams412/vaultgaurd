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
    
model_config = {
    "from_attributes": True
}
