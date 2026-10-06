from datetime import datetime, timezone
from uuid import UUID

from app.repositories.refresh_token import RefreshTokenRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshTokenORM
from sqlalchemy import select
from app.core.security import create_refresh_token, decode_refresh_token



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
        payload = decode_refresh_token(refresh_token)
        token = await self.repository.get_by_jti(payload.jti)

        if token is None:
            raise ValueError("Incorrect token")
        
        if token.revoked:
            raise ValueError("Incorrect token")

        if token.expires_at<=datetime.now(timezone.utc):
            raise ValueError("Incorrect token")

        return payload.user_id

    async def revoke(self,refresh_token: str):
        payload = decode_refresh_token(refresh_token)
        token = await self.repository.revoke(payload.jti)

        if token is None:
            raise ValueError("Not found token")

        return payload.user_id
        



