from pydantic import BaseModel
from typing import List

class Workout(BaseModel):
    exercise: str
    sets: int
    reps: int
    rest_sec: int
    notes: str

class DayPlan(BaseModel):
    day: str  # "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    workouts: List[Workout]

class WeekPlan(BaseModel):
    client_id: str
    week_start_iso: str
    days: List[DayPlan]
