from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from src.logistic_system_api.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from http import HTTPStatus
from src.logistic_system_api.core.models import User
from src.logistic_system_api.core.schemas import UserCreate, UserPublic

router = APIRouter(
    prefix="/users", tags=["users"]
)

DBsession = Annotated[AsyncSession, Depends(get_session)]

@router.post('/register', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def register_user(user: UserCreate, session: DBsession):
    db_user = await session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))    
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')
        
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    await session.commit() 
    await session.refresh(db_user)

    return db_user