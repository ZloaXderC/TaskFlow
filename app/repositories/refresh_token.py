import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshTokenORM
from sqlalchemy import select

class RefreshTokenRepository:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def create_refresh_token(
            self,
            user_id:UUID,
            jti:UUID,
            expires_at:datetime
            ):

        new_token = RefreshTokenORM(
            user_id = user_id,
            jti = jti,
            expires_at = expires_at
            )
        
        self.db.add(new_token)

        try:
            await self.db.commit()

        except Exception:
                await self.db.rollback()
                raise

        await self.db.refresh(new_token)
         
        return new_token
    
    async def get_by_jti(self,jti:UUID):
        stmt = select(RefreshTokenORM).where(RefreshTokenORM.jti==jti)

        result = await self.db.execute(stmt)
        token = result.scalar_one_or_none()

        return token

    async def revoke(self,jti:UUID):
        token = await self.get_by_jti(jti)

        if token == None:
            return None

        token.revoked = True

        try:
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return token
