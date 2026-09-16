from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token, hash_password, verify_password
from app.schemas.user import UserRegister, UserLogin
from app.repositories.user import UserRepository

class UserService:
    def __init__(self, db: AsyncSession):
        repository = UserRepository(db)
        self.repository = repository

    async def register(self, user_data: UserRegister):
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("user is difened")
        
        hashed_password = hash_password(user_data.password)
        created_user = await self.repository.create(
            user_data.email,
            hashed_password
            )
        
        return created_user

    async def login(self, user_data: UserLogin):
        user = await self.repository.get_by_email(user_data.email)
        if not user:
            raise ValueError("Invalid email or password")
        
        is_password_valid = verify_password(
            user_data.password,
            user.hashed_password
        )

        if not is_password_valid:
            raise ValueError("Invalid email or password")

        access_token= create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type":"bearer"
            
        }

    async def refresh_token(self, refresh_token: str):
        user_id  = UUID(decode_refresh_token(refresh_token))

        user = await self.repository.get_by_id(user_id)
        
        if not user:
            raise ValueError("User not found")

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        




        




