from datetime import datetime, timedelta, timezone

from jwt import encode
from pwdlib import PasswordHash

from src.logistic_system_api.core.settings import Settings

settings = Settings()


pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str):
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {'sub': subject, 'exp': expires}

    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
