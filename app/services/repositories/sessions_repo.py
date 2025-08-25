import uuid
from datetime import datetime, date
from botocore.exceptions import ClientError
from typing import List, Optional
from app.services.db import db_service
from app.core.config import settings
from app.models.session import Session, SessionCreate, SessionUpdate
from app.services.repositories.clients_repo import clients_repo

class SessionsRepository:
    def __init__(self):
        self.table = db_service.get_table(settings.DDB_TABLE_SESSIONS)
    
    def create_session(self, username: str, session_data: SessionCreate) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        # Get client name
        client = clients_repo.get_client(session_data.client_id, username)
        if not client:
            raise Exception("Client not found")
        
        item = {
            'session_id': session_id,
            'username': username,
            'client_id': session_data.client_id,
            'client_name': client.name,
            'date': session_data.date,
            'time': session_data.time,
            'status': 'scheduled',
            'notes': session_data.notes or '',
            'created_at': now,
            'updated_at': now
        }
        
        try:
            self.table.put_item(Item=item)
            return session_id
        except ClientError as e:
            raise Exception(f"Failed to create session: {str(e)}")
    
    def get_sessions_by_date(self, username: str, target_date: str) -> List[Session]:
        """Get all sessions for a specific date"""
        try:
            response = self.table.scan(
                FilterExpression='username = :username AND #date = :date',
                ExpressionAttributeNames={'#date': 'date'},
                ExpressionAttributeValues={
                    ':username': username,
                    ':date': target_date
                }
            )
            
            sessions = []
            for item in response.get('Items', []):
                sessions.append(Session(
                    session_id=item['session_id'],
                    client_id=item['client_id'],
                    client_name=item['client_name'],
                    date=item['date'],
                    time=item['time'],
                    status=item['status'],
                    notes=item.get('notes', ''),
                    created_at=item['created_at'],
                    updated_at=item['updated_at']
                ))
            
            # Sort by time
            sessions.sort(key=lambda x: x.time)
            return sessions
        except ClientError as e:
            raise Exception(f"Failed to get sessions: {str(e)}")
    
    def get_today_sessions(self, username: str) -> List[Session]:
        """Get all sessions for today"""
        today = date.today().isoformat()
        return self.get_sessions_by_date(username, today)
    
    def get_session(self, session_id: str, username: str) -> Optional[Session]:
        """Get a specific session"""
        try:
            response = self.table.get_item(
                Key={
                    'session_id': session_id,
                    'username': username
                }
            )
            
            if 'Item' not in response:
                return None
            
            item = response['Item']
            return Session(
                session_id=item['session_id'],
                client_id=item['client_id'],
                client_name=item['client_name'],
                date=item['date'],
                time=item['time'],
                status=item['status'],
                notes=item.get('notes', ''),
                created_at=item['created_at'],
                updated_at=item['updated_at']
            )
        except ClientError as e:
            raise Exception(f"Failed to get session: {str(e)}")
    
    def update_session(self, session_id: str, username: str, updates: SessionUpdate) -> bool:
        """Update a session"""
        try:
            update_expr = "SET updated_at = :updated_at"
            expr_values = {
                ':updated_at': datetime.utcnow().isoformat()
            }
            
            for key, value in updates.dict(exclude_unset=True).items():
                if value is not None:
                    update_expr += f", {key} = :{key}"
                    expr_values[f":{key}"] = value
            
            self.table.update_item(
                Key={
                    'session_id': session_id,
                    'username': username
                },
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to update session: {str(e)}")
    
    def delete_session(self, session_id: str, username: str) -> bool:
        """Delete a session"""
        try:
            self.table.delete_item(
                Key={
                    'session_id': session_id,
                    'username': username
                }
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete session: {str(e)}")

# Global instance
sessions_repo = SessionsRepository()
