# 📁 backend/db_init.py

from db import Base, engine
from models import User, TokenBlacklist  # ✅ Make sure to import both

print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done!")
