from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class RefreshTokenData(BaseModel):
    token: str
    jti: UUID
    expires_at:datetime

class RefreshTokenPayload(BaseModel):
    user_id:UUID
    jti:UUID