from fastapi import APIRouter, HTTPException, status
from app.models.chat import ChatRequest, ChatResponse
from app.services.groq_client import groq_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    try:
        if not request.user_input.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User input cannot be empty"
            )
        
        response = groq_service.send_message(request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {str(e)}"
        )
