import datetime
from uuid import UUID

from app.repositories.refresh_token import RefreshTokenRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshTokenORM
from sqlalchemy import select
from app.core.security import create_refresh_token, decode_refresh_token

8

class RefreshTokenService:
    def __init__(self,db: AsyncSession):
        repository = RefreshTokenRepository(db)
        self.repository = repository

    async def create(self,user_id: UUID):
        refresh_data = create_refresh_token(user_id)
        await self.repository.create_refresh_token(
            user_id=user_id,
            jti= refresh_data.jti,
            expires_at=refresh_data.expires_at
            )

        return refresh_data

    async def validate(self,refresh_token:str):
        decode = decode_refresh_token(refresh_token)
        


