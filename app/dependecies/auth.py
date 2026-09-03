from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme, decode_access_token
from app.db.database import get_db
from app.repositories.user import UserRepository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db : AsyncSession = Depends(get_db)
    ):
    try:
        user_id = decode_access_token(token)
        user_id = UUID(user_id)
        repository = UserRepository(db)
        user = await repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
                )
        
        return user
    
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials"
            )