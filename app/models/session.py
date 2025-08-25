from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Session(BaseModel):
    session_id: str
    client_id: str
    client_name: str
    date: str  # ISO date string
    time: str  # HH:MM format
    status: str  # "scheduled", "completed", "cancelled"
    notes: Optional[str] = None
    created_at: str
    updated_at: str

class SessionCreate(BaseModel):
    client_id: str
    date: str
    time: str
    notes: Optional[str] = None

class SessionUpdate(BaseModel):
    time: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
