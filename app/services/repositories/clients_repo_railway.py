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
        client_id = str(uuid.uuid4())
        
        client = Client(
            client_id=client_id,
            username=username,
            name=client_data.name,
            email=client_data.email,
            phone=client_data.phone,
            age=client_data.age,
            gender=client_data.gender,
            weight=client_data.weight,
            height=client_data.height,
            fitness_level=client_data.fitness_level,
            goals=client_data.goals,
            medical_conditions=client_data.medical_conditions
        )
        
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        
        return client_id
    
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
