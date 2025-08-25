from sqlalchemy.orm import Session
from app.models.database import SessionLocal, create_tables
from app.core.config import settings
import json
from typing import List, Optional, Dict, Any

class RailwayDatabaseService:
    def __init__(self):
        pass  # Remove global db instance
    
    def get_db(self) -> Session:
        return SessionLocal()
    
    def create_tables_if_not_exist(self):
        """Create database tables if they don't exist"""
        try:
            create_tables()
            print("Database tables initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def close(self):
        """Close database connection"""
        pass  # Sessions are managed by get_db()

# Global instance
db_service = RailwayDatabaseService()

# Helper function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
