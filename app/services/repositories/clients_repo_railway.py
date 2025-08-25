from sqlalchemy.orm import Session
from app.models.database import Client
from app.models.client import ClientCreate, ClientUpdate
import uuid
from typing import List, Optional

class ClientsRepositoryRailway:
    def __init__(self, db: Session):
        self.db = db
    
    def create_client(self, username: str, client_data: ClientCreate) -> str:
        """Create a new client"""
        try:
            print(f"Repository: Creating client for username: {username}")
            print(f"Repository: Client data: {client_data}")
            
            client_id = str(uuid.uuid4())
            
            client = Client(
                client_id=client_id,
                username=username,
                name=client_data.name,
                age=client_data.age,
                sex=client_data.sex,
                height_cm=client_data.height_cm,
                weight_kg=client_data.weight_kg,
                activity_level=client_data.activity_level,
                goals=client_data.goals,
                bmr=client_data.bmr,
                tdee=client_data.tdee,
                calorie_maintenance=client_data.calorie_maintenance,
                notes=client_data.notes
            )
            
            print(f"Repository: Adding client to database: {client}")
            self.db.add(client)
            self.db.commit()
            self.db.refresh(client)
            
            print(f"Repository: Client created successfully with ID: {client_id}")
            return client_id
        except Exception as e:
            print(f"Repository: Error creating client: {e}")
            self.db.rollback()
            raise e
    
    def get_clients(self, username: str) -> List[Client]:
        """Get all clients for a user"""
        return self.db.query(Client).filter(Client.username == username).all()
    
    def get_client(self, client_id: str, username: str) -> Optional[Client]:
        """Get a specific client"""
        return self.db.query(Client).filter(
            Client.client_id == client_id,
            Client.username == username
        ).first()
    
    def update_client(self, client_id: str, username: str, updates: ClientUpdate) -> bool:
        """Update a client"""
        client = self.get_client(client_id, username)
        if not client:
            return False
        
        # Update only provided fields
        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)
        
        self.db.commit()
        self.db.refresh(client)
        return True
    
    def delete_client(self, client_id: str, username: str) -> bool:
        """Delete a client"""
        client = self.get_client(client_id, username)
        if not client:
            return False
        
        self.db.delete(client)
        self.db.commit()
        return True
