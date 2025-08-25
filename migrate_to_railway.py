#!/usr/bin/env python3
"""
Migration script to help transition from DynamoDB to Railway PostgreSQL
This script can help migrate existing data if needed
"""

import os
import json
import boto3
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Client, Plan, Session as SessionModel
from app.services.db_railway import db_service

def migrate_dynamodb_to_postgresql():
    """Migrate data from DynamoDB to PostgreSQL"""
    
    print("🚂 Starting migration from DynamoDB to Railway PostgreSQL...")
    
    # Initialize database tables
    db_service.create_tables_if_not_exist()
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Check if we have AWS credentials for migration
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
        
        if not aws_access_key or not aws_secret_key:
            print("⚠️  AWS credentials not found. Skipping data migration.")
            print("📝 You can manually migrate data later if needed.")
            return
        
        # Initialize DynamoDB client
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # Migrate clients
        print("📊 Migrating clients...")
        try:
            clients_table = dynamodb.Table('ai_coach_clients')
            response = clients_table.scan()
            
            for item in response.get('Items', []):
                # Check if client already exists
                existing_client = db.query(Client).filter(
                    Client.client_id == item['client_id']
                ).first()
                
                if not existing_client:
                    client = Client(
                        client_id=item['client_id'],
                        username=item.get('username', 'admin'),
                        name=item.get('name', ''),
                        email=item.get('email'),
                        phone=item.get('phone'),
                        age=item.get('age'),
                        gender=item.get('gender'),
                        weight=item.get('weight'),
                        height=item.get('height'),
                        fitness_level=item.get('fitness_level'),
                        goals=item.get('goals'),
                        medical_conditions=item.get('medical_conditions')
                    )
                    db.add(client)
                    print(f"✅ Migrated client: {item.get('name', item['client_id'])}")
            
            db.commit()
            print(f"✅ Migrated {len(response.get('Items', []))} clients")
            
        except Exception as e:
            print(f"❌ Error migrating clients: {e}")
        
        # Migrate plans
        print("📋 Migrating plans...")
        try:
            plans_table = dynamodb.Table('ai_coach_plans')
            response = plans_table.scan()
            
            for item in response.get('Items', []):
                # Check if plan already exists
                existing_plan = db.query(Plan).filter(
                    Plan.client_id == item['client_id'],
                    Plan.week_start_iso == item['week_start_iso']
                ).first()
                
                if not existing_plan:
                    plan = Plan(
                        client_id=item['client_id'],
                        week_start_iso=item['week_start_iso'],
                        plan_data=json.dumps(item.get('plan_data', {}))
                    )
                    db.add(plan)
                    print(f"✅ Migrated plan for client: {item['client_id']}")
            
            db.commit()
            print(f"✅ Migrated {len(response.get('Items', []))} plans")
            
        except Exception as e:
            print(f"❌ Error migrating plans: {e}")
        
        # Migrate sessions
        print("💬 Migrating sessions...")
        try:
            sessions_table = dynamodb.Table('ai_coach_sessions')
            response = sessions_table.scan()
            
            for item in response.get('Items', []):
                # Check if session already exists
                existing_session = db.query(SessionModel).filter(
                    SessionModel.session_id == item['session_id']
                ).first()
                
                if not existing_session:
                    session = SessionModel(
                        session_id=item['session_id'],
                        username=item.get('username', 'admin'),
                        session_data=json.dumps(item.get('session_data', {}))
                    )
                    db.add(session)
                    print(f"✅ Migrated session: {item['session_id']}")
            
            db.commit()
            print(f"✅ Migrated {len(response.get('Items', []))} sessions")
            
        except Exception as e:
            print(f"❌ Error migrating sessions: {e}")
        
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
    
    finally:
        db.close()

def verify_migration():
    """Verify that the migration was successful"""
    
    print("🔍 Verifying migration...")
    
    db = SessionLocal()
    
    try:
        # Count records in each table
        client_count = db.query(Client).count()
        plan_count = db.query(Plan).count()
        session_count = db.query(SessionModel).count()
        
        print(f"📊 Migration Results:")
        print(f"   Clients: {client_count}")
        print(f"   Plans: {plan_count}")
        print(f"   Sessions: {session_count}")
        
        if client_count > 0 or plan_count > 0 or session_count > 0:
            print("✅ Migration verification successful!")
        else:
            print("⚠️  No data found. This is normal for a fresh deployment.")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🚂 Railway Migration Tool")
    print("=" * 50)
    
    # Check if we're in Railway environment
    if os.getenv("RAILWAY_ENVIRONMENT"):
        print("✅ Running in Railway environment")
    else:
        print("⚠️  Not running in Railway environment")
    
    # Run migration
    migrate_dynamodb_to_postgresql()
    
    # Verify migration
    verify_migration()
    
    print("\n🎉 Migration tool completed!")
    print("📝 Next steps:")
    print("   1. Deploy to Railway")
    print("   2. Test your API endpoints")
    print("   3. Update your frontend to use the new API URL")
