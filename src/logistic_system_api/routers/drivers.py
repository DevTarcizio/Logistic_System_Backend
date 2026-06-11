from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.logistic_system_api.core.database import get_session
from src.logistic_system_api.core.models import Driver, User
from src.logistic_system_api.core.schemas import (
    DriverCreate,
    DriverList,
    DriverPublic,
)
from src.logistic_system_api.core.security import get_current_user

router = APIRouter(prefix='/drivers', tags=['drivers'])

DBsession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/register_driver', response_model=DriverPublic, status_code=HTTPStatus.CREATED
)
async def register_driver(
    driver: DriverCreate, session: DBsession, current_user: CurrentUser
):
    db_driver = await session.scalar(select(Driver).where(Driver.name == driver.name))

    if db_driver:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Driver with this name already exists'
        )

    db_driver = Driver(
        name=driver.name,
        telephone_number=driver.telephone_number,
    )

    session.add(db_driver)
    await session.commit()
    await session.refresh(db_driver)

    return db_driver


@router.get('/list', response_model=DriverList, status_code=HTTPStatus.OK)
async def list_drivers(session: DBsession, current_user: CurrentUser):
    result = await session.execute(select(Driver))
    drivers = result.scalars().all()

    return DriverList(drivers=drivers)


@router.delete('/delete/{driver_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_driver(driver_id: int, session: DBsession, current_user: CurrentUser):
    db_driver = await session.get(Driver, driver_id)

    if not db_driver:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Driver not found')

    await session.delete(db_driver)
    await session.commit()
