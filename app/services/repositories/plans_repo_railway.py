from sqlalchemy.orm import Session
from app.models.database import Plan
from app.models.plan import WeekPlan, DayPlan, Workout
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

class PlansRepositoryRailway:
    def __init__(self, db: Session):
        self.db = db
    
    def create_plan(self, client_id: str, week_start_iso: str, plan_data: Dict[str, Any]) -> int:
        """Create a new plan"""
        plan = Plan(
            client_id=client_id,
            week_start_iso=week_start_iso,
            plan_data=json.dumps(plan_data)
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan.id
    
    def get_plans(self, client_id: str) -> List[Plan]:
        """Get all plans for a client"""
        return self.db.query(Plan).filter(Plan.client_id == client_id).all()
    
    def get_plan(self, plan_id: int) -> Optional[Plan]:
        """Get a specific plan"""
        return self.db.query(Plan).filter(Plan.id == plan_id).first()
    
    def get_plan_by_week(self, client_id: str, week_start_iso: str) -> Optional[Plan]:
        """Get a plan by client and week"""
        return self.db.query(Plan).filter(
            Plan.client_id == client_id,
            Plan.week_start_iso == week_start_iso
        ).first()
    
    def update_plan(self, plan_id: int, plan_data: Dict[str, Any]) -> bool:
        """Update a plan"""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        
        plan.plan_data = json.dumps(plan_data)
        self.db.commit()
        self.db.refresh(plan)
        return True
    
    def delete_plan(self, plan_id: int) -> bool:
        """Delete a plan"""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        
        self.db.delete(plan)
        self.db.commit()
        return True
    
    def get_week_plan(self, client_id: str, weekOffset: int) -> WeekPlan:
        """Get week plan for a client with offset"""
        # Calculate the target week start date
        today = datetime.now()
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)
        target_week_start = current_week_start + timedelta(weeks=weekOffset)
        week_start_iso = target_week_start.strftime("%Y-%m-%d")
        
        # Try to get existing plan
        plan = self.get_plan_by_week(client_id, week_start_iso)
        
        if plan:
            # Return existing plan
            plan_data = json.loads(plan.plan_data)
            return WeekPlan(
                client_id=client_id,
                week_start_iso=week_start_iso,
                days=plan_data.get('days', [])
            )
        else:
            # Return empty plan structure
            return WeekPlan(
                client_id=client_id,
                week_start_iso=week_start_iso,
                days=[]
            )
    
    def save_week_plan(self, plan: WeekPlan) -> bool:
        """Save or update a week plan"""
        try:
            # Check if plan already exists
            existing_plan = self.get_plan_by_week(plan.client_id, plan.week_start_iso)
            
            if existing_plan:
                # Update existing plan
                existing_plan.plan_data = json.dumps({'days': [day.dict() for day in plan.days]})
                self.db.commit()
                self.db.refresh(existing_plan)
            else:
                # Create new plan
                new_plan = Plan(
                    client_id=plan.client_id,
                    week_start_iso=plan.week_start_iso,
                    plan_data=json.dumps({'days': [day.dict() for day in plan.days]})
                )
                self.db.add(new_plan)
                self.db.commit()
                self.db.refresh(new_plan)
            
            return True
        except Exception as e:
            print(f"Error saving week plan: {e}")
            return False
