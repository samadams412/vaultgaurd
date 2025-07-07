# 📁 backend/db_init.py

from db import Base, engine
from models import User  # make sure this matches your actual model

# This will create all tables defined in models.py
print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Done!")
