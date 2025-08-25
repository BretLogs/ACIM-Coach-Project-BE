import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

class DynamoDBService:
    def __init__(self):
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        else:
            # For local development with AWS CLI configured
            self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
    
    def get_table(self, table_name: str):
        return self.dynamodb.Table(table_name)
    
    def create_tables_if_not_exist(self):
        """Create DynamoDB tables if they don't exist (for local development)"""
        try:
            # Users table
            self.dynamodb.create_table(
                TableName=settings.DDB_TABLE_USERS,
                KeySchema=[
                    {'AttributeName': 'username', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'username', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Clients table
            self.dynamodb.create_table(
                TableName=settings.DDB_TABLE_CLIENTS,
                KeySchema=[
                    {'AttributeName': 'client_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'username', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'client_id', 'AttributeType': 'S'},
                    {'AttributeName': 'username', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Plans table
            self.dynamodb.create_table(
                TableName=settings.DDB_TABLE_PLANS,
                KeySchema=[
                    {'AttributeName': 'client_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'week_start_iso', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'client_id', 'AttributeType': 'S'},
                    {'AttributeName': 'week_start_iso', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Sessions table
            self.dynamodb.create_table(
                TableName=settings.DDB_TABLE_SESSIONS,
                KeySchema=[
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'username', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'session_id', 'AttributeType': 'S'},
                    {'AttributeName': 'username', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceInUseException':
                print(f"Error creating tables: {e}")

# Global instance
db_service = DynamoDBService()
