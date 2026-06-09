from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.logistic_system_api.core.database import get_session
from src.logistic_system_api.core.models import User
from src.logistic_system_api.core.settings import Settings

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str):
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {'sub': str(subject), 'exp': expires}

    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except Exception as e:
        print(f'Erro: {type(e).__name__}')
        print(f'Mensagem: {e}')
        raise


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    payload = decode_access_token(token)
    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')

    user = await session.scalar(select(User).where(User.id == int(user_id)))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='User not found')

    return user
