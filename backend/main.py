# -----------------------------
# 📁 File: backend/main.py
# -----------------------------
from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI(title="VaultGuard API")

# Root route
@app.get("/")
def root():
    return {"message": "VaultGuard API is running"}

# Mount the auth routes
app.include_router(auth_router, prefix="/auth")