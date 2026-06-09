from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.logistic_system_api.core.database import get_session
from src.logistic_system_api.core.models import User
from src.logistic_system_api.core.schemas import (
    Token,
    UserCreate,
    UserPublic,
)
from src.logistic_system_api.core.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix='/users', tags=['users'])

DBsession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/register', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def register_user(user: UserCreate, session: DBsession):
    db_user = await session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.post('/login', response_model=Token, status_code=HTTPStatus.OK)
async def login_user(
    session: DBsession, form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = await session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid username or password'
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid username or password'
        )

    access_token = create_access_token(subject=str(db_user.id))

    return Token(access_token=access_token, token_type='bearer')


@router.get('/me', status_code=HTTPStatus.OK)
async def read_current_user(current_user: CurrentUser):
    return current_user
