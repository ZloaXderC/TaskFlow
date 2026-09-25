from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependecies.auth import get_current_user
from app.repositories.user import UserRepository
from app.service.user import UserService
from app.schemas.user import TokenRefreshRequest, TokenRefreshResponse, UserLogin, UserResponse, TokenResponse
from app.schemas.user import UserRegister
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix= '/auth', tags = ["Auth"])

@router.post('/register', response_model = UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession= Depends(get_db)
    ):

    service = UserService(db)

    try:
        result  = await service.register(user_data)
        return result 
    
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
        
@router.post('/login', response_model = TokenResponse, status_code=status.HTTP_200_OK)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
    ):

    service = UserService(db)
    user_data = UserLogin(
        email = form_data.username,
        password= form_data.password
    )

    try:
        result = await service.login(user_data)
        return result
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))    

@router.get("/me", response_model = UserResponse)
async def get_me(
    current_user = Depends(get_current_user),
    ):
    return current_user

@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    payload: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        result = await service.refresh_token(payload.refresh_token)
        return result
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

@router.post("/logout", status_code = status.HTTP_204_NO_CONTENT)
async def logout(
    payload: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)

    try:
        result = await service.logout(payload.refresh_token)

    except ValueError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

