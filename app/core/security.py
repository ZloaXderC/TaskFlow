from uuid import UUID
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id:UUID) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload ={
        "sub": str(user_id),
        "type": "access",
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm= settings.JWT_ALGORITHM
    )

    return token

def decode_access_token(token:str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type  = payload.get("type")
        if token_type != "access":
            raise ValueError("Invalid token type")

        return user_id

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def create_refresh_token(user_id:UUID) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm= settings.JWT_ALGORITHM
    )

    return token


def decode_refresh_token(token:str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type  = payload.get("type")
        if token_type != "refresh":
            raise ValueError("Invalid token type")

        return user_id

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    
