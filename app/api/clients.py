from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.client import Client, ClientCreate, ClientUpdate, ClientResponse
from app.services.repositories.clients_repo import clients_repo

router = APIRouter()

# Default username for single-user system
DEFAULT_USERNAME = "admin"

@router.post("/", response_model=ClientResponse)
async def create_client(client_data: ClientCreate):
    try:
        client_id = clients_repo.create_client(DEFAULT_USERNAME, client_data)
        return ClientResponse(client_id=client_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Client])
async def get_clients():
    try:
        return clients_repo.get_clients(DEFAULT_USERNAME)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: str):
    try:
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
async def update_client(client_id: str, updates: ClientUpdate):
    try:
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
async def delete_client(client_id: str):
    try:
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
