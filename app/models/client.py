from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    age: int
    sex: str  # "male" or "female"
    height_cm: float
    weight_kg: float
    activity_level: str  # "sedentary", "light", "moderate", "very_active", "athlete"
    goals: str
    bmr: int
    tdee: int
    calorie_maintenance: int
    notes: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    goals: Optional[str] = None
    bmr: Optional[int] = None
    tdee: Optional[int] = None
    calorie_maintenance: Optional[int] = None
    notes: Optional[str] = None

class Client(ClientBase):
    client_id: str
    created_at: datetime
    updated_at: datetime

class ClientResponse(BaseModel):
    client_id: str
