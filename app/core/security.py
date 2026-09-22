from uuid import UUID, uuid4
from app.schemas.refresh_token import RefreshTokenData, RefreshTokenPayload
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

def create_refresh_token(user_id:UUID) -> RefreshTokenData:
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    jti = uuid4()
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expires_at,
        "jti": str(jti)
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm= settings.JWT_ALGORITHM
    )

    return RefreshTokenData(token = token, jti = jti , expires_at = expires_at)


def decode_refresh_token(token:str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        

        user_id = payload.get("sub")
        token_type  = payload.get("type")
        jti = payload.get("jti")
        if token_type != "refresh":
            raise ValueError("Invalid token type")
        if not jti:
            raise ValueError("Invalid jti")

        return RefreshTokenPayload(user_id=user_id,jti=jti)

    except (jwt.InvalidTokenError, ValueError):
        raise ValueError("Invalid token")
    
