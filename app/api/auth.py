from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.auth import LoginRequest, LoginResponse, User
from app.services.repositories.users_repo import users_repo
from app.core.security import create_access_token, verify_token

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    username = verify_token(credentials.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    user = users_repo.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(subject=user["username"])
    return LoginResponse(message="ok", token=access_token, username=user["username"])

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    return User(username=current_user)
