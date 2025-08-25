from botocore.exceptions import ClientError
from app.services.db import db_service
from app.core.config import settings
from app.core.security import get_password_hash, verify_password

class UsersRepository:
    def __init__(self):
        self.table = db_service.get_table(settings.DDB_TABLE_USERS)
    
    def get_user(self, username: str):
        try:
            response = self.table.get_item(Key={'username': username})
            return response.get('Item')
        except ClientError:
            return None
    
    def create_user(self, username: str, password: str):
        try:
            hashed_password = get_password_hash(password)
            self.table.put_item(
                Item={
                    'username': username,
                    'hashed_password': hashed_password
                }
            )
            return True
        except ClientError:
            return False
    
    def authenticate_user(self, username: str, password: str):
        # For MVP, use hardcoded credentials
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            return {'username': username}
        
        # Also check database for future extensibility
        user = self.get_user(username)
        if user and verify_password(password, user.get('hashed_password', '')):
            return user
        
        return None

# Global instance
users_repo = UsersRepository()
