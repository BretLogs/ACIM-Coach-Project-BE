import uuid
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
from typing import List, Optional
from app.services.db import db_service
from app.core.config import settings
from app.models.client import Client, ClientCreate, ClientUpdate

class ClientsRepository:
    def __init__(self):
        self.table = db_service.get_table(settings.DDB_TABLE_CLIENTS)
    
    def create_client(self, username: str, client_data: ClientCreate) -> str:
        client_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        item = {
            'client_id': client_id,
            'username': username,
            'name': client_data.name,
            'age': client_data.age,
            'sex': client_data.sex,
            'height_cm': Decimal(str(client_data.height_cm)),
            'weight_kg': Decimal(str(client_data.weight_kg)),
            'activity_level': client_data.activity_level,
            'goals': client_data.goals,
            'bmr': client_data.bmr,
            'tdee': client_data.tdee,
            'calorie_maintenance': client_data.calorie_maintenance,
            'notes': client_data.notes,
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        
        try:
            self.table.put_item(Item=item)
            return client_id
        except ClientError as e:
            raise Exception(f"Failed to create client: {str(e)}")
    
    def get_clients(self, username: str) -> List[Client]:
        try:
            # Query by GSI or scan with filter (for MVP, we'll scan)
            response = self.table.scan(
                FilterExpression='username = :username',
                ExpressionAttributeValues={':username': username}
            )
            
            clients = []
            for item in response.get('Items', []):
                clients.append(Client(
                    client_id=item['client_id'],
                    name=item['name'],
                    age=item['age'],
                    sex=item['sex'],
                    height_cm=float(item['height_cm']),
                    weight_kg=float(item['weight_kg']),
                    activity_level=item['activity_level'],
                    goals=item['goals'],
                    bmr=item['bmr'],
                    tdee=item['tdee'],
                    calorie_maintenance=item['calorie_maintenance'],
                    notes=item['notes'],
                    created_at=datetime.fromisoformat(item['created_at']),
                    updated_at=datetime.fromisoformat(item['updated_at'])
                ))
            
            return clients
        except ClientError as e:
            raise Exception(f"Failed to get clients: {str(e)}")
    
    def get_client(self, client_id: str, username: str) -> Optional[Client]:
        try:
            response = self.table.get_item(
                Key={'client_id': client_id, 'username': username}
            )
            
            item = response.get('Item')
            if not item:
                return None
            
            return Client(
                client_id=item['client_id'],
                name=item['name'],
                age=item['age'],
                sex=item['sex'],
                height_cm=float(item['height_cm']),
                weight_kg=float(item['weight_kg']),
                activity_level=item['activity_level'],
                goals=item['goals'],
                bmr=item['bmr'],
                tdee=item['tdee'],
                calorie_maintenance=item['calorie_maintenance'],
                notes=item['notes'],
                created_at=datetime.fromisoformat(item['created_at']),
                updated_at=datetime.fromisoformat(item['updated_at'])
            )
        except ClientError as e:
            raise Exception(f"Failed to get client: {str(e)}")
    
    def update_client(self, client_id: str, username: str, updates: ClientUpdate) -> bool:
        try:
            # Build update expression
            update_expr = "SET updated_at = :updated_at"
            expr_values = {':updated_at': datetime.utcnow().isoformat()}
            
            update_data = updates.dict(exclude_unset=True)
            for key, value in update_data.items():
                update_expr += f", {key} = :{key}"
                # Convert float values to Decimal for DynamoDB
                if key in ['height_cm', 'weight_kg'] and isinstance(value, float):
                    expr_values[f":{key}"] = Decimal(str(value))
                else:
                    expr_values[f":{key}"] = value
            
            self.table.update_item(
                Key={'client_id': client_id, 'username': username},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to update client: {str(e)}")
    
    def delete_client(self, client_id: str, username: str) -> bool:
        try:
            self.table.delete_item(
                Key={'client_id': client_id, 'username': username}
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete client: {str(e)}")

# Global instance
clients_repo = ClientsRepository()
