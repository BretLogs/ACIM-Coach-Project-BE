from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str
    username: str

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
