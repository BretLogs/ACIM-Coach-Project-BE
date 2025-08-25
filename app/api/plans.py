from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from app.models.plan import WeekPlan
from app.services.repositories.plans_repo_railway import PlansRepositoryRailway
from app.services.db_railway import get_db

router = APIRouter()

@router.get("/weeks/{client_id}", response_model=WeekPlan)
async def get_week_plan(
    client_id: str,
    weekOffset: int = Query(0, description="Week offset: 0 for current week, 1 for next week"),
    db: Session = Depends(get_db)
):
    try:
        # Validate week offset
        if weekOffset not in [0, 1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Week offset must be 0 (current week) or 1 (next week)"
            )
        
        plans_repo = PlansRepositoryRailway(db)
        return plans_repo.get_week_plan(client_id, weekOffset)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/weeks/{client_id}")
async def save_week_plan(
    client_id: str,
    plan: WeekPlan,
    db: Session = Depends(get_db)
):
    try:
        # Ensure the client_id in the URL matches the plan
        if plan.client_id != client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client ID in URL must match client ID in plan"
            )
        
        plans_repo = PlansRepositoryRailway(db)
        success = plans_repo.save_week_plan(plan)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save week plan"
            )
        
        return {"message": "saved"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
