from sqlalchemy.orm import Session
from app.models.database import SessionLocal, create_tables
from app.core.config import settings
import json
from typing import List, Optional, Dict, Any

class RailwayDatabaseService:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_db(self) -> Session:
        return self.db
    
    def create_tables_if_not_exist(self):
        """Create database tables if they don't exist"""
        try:
            create_tables()
            print("Database tables initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()

# Global instance
db_service = RailwayDatabaseService()

# Helper function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
