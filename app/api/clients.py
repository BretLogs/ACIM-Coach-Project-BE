from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.client import Client, ClientCreate, ClientUpdate, ClientResponse
from app.services.repositories.clients_repo_railway import ClientsRepositoryRailway
from app.services.db_railway import get_db

router = APIRouter()

# Default username for single-user system
DEFAULT_USERNAME = "admin"

@router.post("/", response_model=ClientResponse)
async def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    try:
        print(f"Creating client with data: {client_data}")
        clients_repo = ClientsRepositoryRailway(db)
        client_id = clients_repo.create_client(DEFAULT_USERNAME, client_data)
        print(f"Client created with ID: {client_id}")
        response = ClientResponse(client_id=client_id)
        print(f"Returning response: {response}")
        return response
    except Exception as e:
        print(f"Error creating client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Client])
async def get_clients(db: Session = Depends(get_db)):
    try:
        clients_repo = ClientsRepositoryRailway(db)
        return clients_repo.get_clients(DEFAULT_USERNAME)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: str, db: Session = Depends(get_db)):
    try:
        clients_repo = ClientsRepositoryRailway(db)
        client = clients_repo.get_client(client_id, DEFAULT_USERNAME)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{client_id}")
async def update_client(client_id: str, updates: ClientUpdate, db: Session = Depends(get_db)):
    try:
        clients_repo = ClientsRepositoryRailway(db)
        success = clients_repo.update_client(client_id, DEFAULT_USERNAME, updates)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return {"message": "updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{client_id}")
async def delete_client(client_id: str, db: Session = Depends(get_db)):
    try:
        clients_repo = ClientsRepositoryRailway(db)
        success = clients_repo.delete_client(client_id, DEFAULT_USERNAME)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return {"message": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Test database connectivity"""
    try:
        # Test basic database connection
        result = db.execute("SELECT 1").scalar()
        print(f"Database test result: {result}")
        
        # Test if clients table exists
        try:
            clients_count = db.execute("SELECT COUNT(*) FROM clients").scalar()
            print(f"Clients table count: {clients_count}")
        except Exception as e:
            print(f"Error checking clients table: {e}")
            return {"status": "error", "message": f"Database connected but clients table issue: {e}"}
        
        return {
            "status": "success", 
            "database_connected": True,
            "clients_count": clients_count,
            "test_result": result
        }
    except Exception as e:
        print(f"Database test error: {e}")
        return {"status": "error", "message": str(e)}
