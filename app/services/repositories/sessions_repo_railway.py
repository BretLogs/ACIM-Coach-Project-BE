from sqlalchemy.orm import Session
from app.models.database import Session as SessionModel
from app.models.session import SessionCreate, SessionUpdate
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class SessionsRepositoryRailway:
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(self, username: str, session_data: SessionCreate) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        session = SessionModel(
            session_id=session_id,
            username=username,
            session_data=json.dumps(session_data.dict())
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session_id
    
    def get_sessions(self, username: str) -> List[SessionModel]:
        """Get all sessions for a user"""
        return self.db.query(SessionModel).filter(SessionModel.username == username).all()
    
    def get_session(self, session_id: str, username: str) -> Optional[SessionModel]:
        """Get a specific session"""
        return self.db.query(SessionModel).filter(
            SessionModel.session_id == session_id,
            SessionModel.username == username
        ).first()
    
    def update_session(self, session_id: str, username: str, updates: SessionUpdate) -> bool:
        """Update a session"""
        session = self.get_session(session_id, username)
        if not session:
            return False
        
        # Update only provided fields
        update_data = updates.dict(exclude_unset=True)
        session.session_data = json.dumps(update_data)
        
        self.db.commit()
        self.db.refresh(session)
        return True
    
    def delete_session(self, session_id: str, username: str) -> bool:
        """Delete a session"""
        session = self.get_session(session_id, username)
        if not session:
            return False
        
        self.db.delete(session)
        self.db.commit()
        return True
    
    def get_today_sessions(self, username: str) -> List[SessionModel]:
        """Get sessions for today"""
        today = date.today().isoformat()
        return self.get_sessions_by_date(username, today)
    
    def get_sessions_by_date(self, username: str, date_str: str) -> List[SessionModel]:
        """Get sessions for a specific date"""
        # This is a simplified implementation
        # In a real app, you might want to store date separately or parse session_data
        all_sessions = self.get_sessions(username)
        today_sessions = []
        
        for session in all_sessions:
            try:
                session_data = json.loads(session.session_data)
                # Check if session has a date field that matches
                if session_data.get('date') == date_str:
                    today_sessions.append(session)
            except (json.JSONDecodeError, KeyError):
                continue
        
        return today_sessions
