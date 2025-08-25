from sqlalchemy.orm import Session
from app.models.database import Plan
from app.models.plan import PlanCreate, PlanUpdate
import json
from typing import List, Optional, Dict, Any

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
    
    def update_plan(self, plan_id: int, updates: PlanUpdate) -> bool:
        """Update a plan"""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        
        # Update only provided fields
        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "plan_data" and isinstance(value, dict):
                setattr(plan, field, json.dumps(value))
            else:
                setattr(plan, field, value)
        
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
