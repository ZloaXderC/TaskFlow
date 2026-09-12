from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserRegister(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str
    
class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str
