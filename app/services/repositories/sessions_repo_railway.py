from sqlalchemy.orm import Session
from app.models.database import Session as SessionModel
import json
import uuid
from typing import List, Optional, Dict, Any

class SessionsRepositoryRailway:
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(self, username: str, session_data: Dict[str, Any]) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        session = SessionModel(
            session_id=session_id,
            username=username,
            session_data=json.dumps(session_data)
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
    
    def update_session(self, session_id: str, username: str, session_data: Dict[str, Any]) -> bool:
        """Update a session"""
        session = self.get_session(session_id, username)
        if not session:
            return False
        
        session.session_data = json.dumps(session_data)
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
