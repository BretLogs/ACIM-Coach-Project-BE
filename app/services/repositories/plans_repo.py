from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from typing import Optional
from app.services.db import db_service
from app.core.config import settings
from app.models.plan import WeekPlan, DayPlan, Workout

class PlansRepository:
    def __init__(self):
        self.table = db_service.get_table(settings.DDB_TABLE_PLANS)
    
    def get_week_start(self, week_offset: int = 0) -> str:
        """Get the start of the week (Monday) for the given offset"""
        today = datetime.utcnow().date()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        target_monday = monday + timedelta(weeks=week_offset)
        return target_monday.isoformat()
    
    def get_week_plan(self, client_id: str, week_offset: int = 0) -> WeekPlan:
        week_start = self.get_week_start(week_offset)
        
        try:
            response = self.table.get_item(
                Key={'client_id': client_id, 'week_start_iso': week_start}
            )
            
            item = response.get('Item')
            if item:
                # Convert DynamoDB item back to WeekPlan
                days = []
                for day_data in item.get('days', []):
                    workouts = []
                    for workout_data in day_data.get('workouts', []):
                        workouts.append(Workout(**workout_data))
                    days.append(DayPlan(day=day_data['day'], workouts=workouts))
                
                return WeekPlan(
                    client_id=item['client_id'],
                    week_start_iso=item['week_start_iso'],
                    days=days
                )
            else:
                # Return empty week plan
                days = []
                for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                    days.append(DayPlan(day=day, workouts=[]))
                
                return WeekPlan(
                    client_id=client_id,
                    week_start_iso=week_start,
                    days=days
                )
                
        except ClientError as e:
            raise Exception(f"Failed to get week plan: {str(e)}")
    
    def save_week_plan(self, plan: WeekPlan) -> bool:
        try:
            # Convert WeekPlan to DynamoDB item
            days_data = []
            for day in plan.days:
                workouts_data = []
                for workout in day.workouts:
                    workouts_data.append(workout.dict())
                days_data.append({
                    'day': day.day,
                    'workouts': workouts_data
                })
            
            item = {
                'client_id': plan.client_id,
                'week_start_iso': plan.week_start_iso,
                'days': days_data,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            raise Exception(f"Failed to save week plan: {str(e)}")

# Global instance
plans_repo = PlansRepository()
