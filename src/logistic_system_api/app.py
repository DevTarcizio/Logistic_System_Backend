from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.logistic_system_api.core.database import get_session
from src.logistic_system_api.routers import drivers, users

DBsession = Annotated[AsyncSession, Depends(get_session)]

app = FastAPI(title='Logistic System API')
app.include_router(users.router)
app.include_router(drivers.router)


@app.get('/')
def read_root():
    return {'msg': 'Hello World!'}
