from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os

# Database URL from environment variable (Railway will provide this)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_coach.db")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(Base):
    __tablename__ = "users"
    
    username = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Client model
class Client(Base):
    __tablename__ = "clients"
    
    client_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    sex = Column(String(10))  # "male" or "female"
    height_cm = Column(Integer)  # in cm
    weight_kg = Column(Integer)  # in kg
    activity_level = Column(String(20))  # "sedentary", "light", "moderate", "very_active", "athlete"
    goals = Column(Text)
    bmr = Column(Integer)
    tdee = Column(Integer)
    calorie_maintenance = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Plan model
class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), nullable=False, index=True)
    week_start_iso = Column(String(10), nullable=False, index=True)
    plan_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Session model
class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    session_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
