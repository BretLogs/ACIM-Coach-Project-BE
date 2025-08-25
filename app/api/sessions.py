from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.session import Session, SessionCreate, SessionUpdate, SessionResponse
from app.services.repositories.sessions_repo_railway import SessionsRepositoryRailway
from app.services.db_railway import get_db

router = APIRouter()

# Default username for single-user system
DEFAULT_USERNAME = "admin"

@router.post("/", response_model=SessionResponse)
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        session_id = sessions_repo.create_session(DEFAULT_USERNAME, session_data)
        return SessionResponse(session_id=session_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/today", response_model=List[Session])
async def get_today_sessions(db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        return sessions_repo.get_today_sessions(DEFAULT_USERNAME)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/date/{date}", response_model=List[Session])
async def get_sessions_by_date(date: str, db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        return sessions_repo.get_sessions_by_date(DEFAULT_USERNAME, date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        session = sessions_repo.get_session(session_id, DEFAULT_USERNAME)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{session_id}")
async def update_session(session_id: str, updates: SessionUpdate, db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        success = sessions_repo.update_session(session_id, DEFAULT_USERNAME, updates)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return {"message": "updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    try:
        sessions_repo = SessionsRepositoryRailway(db)
        success = sessions_repo.delete_session(session_id, DEFAULT_USERNAME)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return {"message": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
