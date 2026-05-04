import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from utils.errors import InvalidTokenError, TokenExpiredError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_DUMMY_HASH = "$2b$12$KIXnHu7sBJLFQJbMq1ZhFOqHY4X3m8vVjWz6Y0p9QlNpRoSmTuUwG"


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password_safe(plain: str, hashed: str | None) -> bool:
    target = hashed if hashed is not None else _DUMMY_HASH
    result = pwd_context.verify(plain, target)
    return result and hashed is not None


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()


def generate_opaque_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError:
        raise TokenExpiredError("Access token has expired.")
    except JWTError:
        raise InvalidTokenError("Access token is invalid or malformed.")

    if payload.get("type") != "access":
        raise InvalidTokenError("Token is not an access token.")

    return payload