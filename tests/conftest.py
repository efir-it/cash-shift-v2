import asyncio
import datetime
import json

import pytest
from httpx import AsyncClient
from jose import jwt
from sqlalchemy import insert

from cash_shift.models import CashShift
from check.models import Receipt
from config import settings
from database import Base, async_session_maker, engine
from event.models import Event
from main import app as fastapi_app
from position_check.models import PositionCheck


# custom Decoder
def DecodeDateTime(empDict):
    format = "%Y-%m-%dT%H:%M:%S"
    if "date" in empDict:
        empDict["date"] = datetime.datetime.strptime(empDict["date"], format)
    if "send_time" in empDict:
        empDict["send_time"] = datetime.datetime.strptime(empDict["send_time"], format)
    return empDict


@pytest.fixture(scope="session", autouse=True)
async def set_user_variables():
    assert settings.MODE == "TEST"

    permissions = [
        f"/checkoutShift/getCheckoutShifts",
        f"/checkoutShift/getCheckoutShift",
        f"/checkoutShift/openCheckoutShift",
        f"/checkoutShift/closeCheckoutShift",
        f"/checkoutShift/getCashReceipt",
        f"/checkoutShift/createCashReceipt",
        f"/checkoutShift/returnCashReceipt",
        f"/checkoutShift/closeCashReceipt",
        f"/checkoutShift/removeCashReceipt",
    ]
    timedelta = datetime.timedelta(settings.TEST_TIMEDELTA)
    owner_jwt_data = {
        "ownerId": settings.TEST_OWNER_ID,
        "exp": datetime.datetime.utcnow() + timedelta,
        "iss": settings.TOKEN_ISSUER,
        "aud": settings.TOKEN_OWNER_AUDIENCE,
    }
    worker_jwt_data = {
        "ownerId": settings.TEST_OWNER_ID,
        "organizationId": settings.TEST_ORGANIZATION_ID,
        "workerId": settings.TEST_WORKER_ID,
        "exp": datetime.datetime.utcnow() + timedelta,
        "iss": settings.TOKEN_ISSUER,
        "aud": settings.TOKEN_WORKER_AUDIENCE,
        "api_permission": permissions,
    }
    owner_token = jwt.encode(
        owner_jwt_data,
        settings.TOKEN_OWNER_KEY,
        algorithm=settings.ALGORITHM,
    )
    worker_token = jwt.encode(
        worker_jwt_data,
        settings.TOKEN_WORKER_KEY,
        algorithm=settings.ALGORITHM,
    )
    settings.TEST_WORKER_TOKEN = worker_token
    settings.TEST_OWNER_TOKEN = owner_token


@pytest.fixture(scope="function", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"./tests/mock_{model}.json", encoding="utf-8") as file:
            return json.loads(file.read(), object_hook=DecodeDateTime)

    cash_shift = open_mock_json("cash_shift")
    check = open_mock_json("check")
    rabbit_event = open_mock_json("rabbit_event")

    async with async_session_maker() as session:
        add_cash_shift = insert(CashShift).values(cash_shift)
        add_check = insert(Receipt).values(check)
        add_rabbit_event = insert(Event).values(rabbit_event)
        await session.execute(add_cash_shift)
        await session.execute(add_check)
        await session.execute(add_rabbit_event)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
