from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, hash_password, verify_password
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

        token= create_access_token(user.id)

        return {
            "access_token": token,
            "token_type":"bearer"
        }

        




