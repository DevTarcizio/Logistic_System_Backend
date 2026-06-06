from typing import Annotated

from src.logistic_system_api.core.database import get_session
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

DBsession = Annotated[AsyncSession, Depends(get_session)]

app = FastAPI()


@app.get('/')
def read_root():
    return {'msg': 'Hello World!'}


@app.get('/db')
async def db_test(session: DBsession):
    result = await session.execute(text('SELECT 1'))

    return {'status': 'ok', 'Result': result.scalar()}
