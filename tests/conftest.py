import asyncio
import datetime
import json
import dateutil.parser

import pytest
from sqlalchemy import insert

from config import settings
from database import Base, async_session_maker, engine

from check.models import Check
from check_status.models import CheckStatus
from position_check.models import PositionCheck
from type_operation.models import TypeOperation
from type_payment.models import TypePayment
from type_taxation.models import TypeTaxation
from cash_shift.models import CashShift

from httpx import AsyncClient

from main import app as fastapi_app


# custom Decoder
def DecodeDateTime(empDict):
    format = "%Y-%m-%dT%H:%M:%S"
    if "date" in empDict:
        empDict["date"] = datetime.datetime.strptime(empDict["date"], format)
    return empDict


@pytest.fixture(scope="session", autouse=True)
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
    check_status = open_mock_json("check_status")
    position_check = open_mock_json("position_check")
    type_operation = open_mock_json("type_operation")
    type_payment = open_mock_json("type_payment")
    type_taxation = open_mock_json("type_taxation")

    async with async_session_maker() as session:
        add_cash_shift = insert(CashShift).values(cash_shift)
        add_check = insert(Check).values(check)
        add_check_status = insert(CheckStatus).values(check_status)
        add_position_check = insert(PositionCheck).values(position_check)
        add_type_operation = insert(TypeOperation).values(type_operation)
        add_type_payment = insert(TypePayment).values(type_payment)
        add_type_taxation = insert(TypeTaxation).values(type_taxation)

        await session.execute(add_type_operation)
        await session.execute(add_type_payment)
        await session.execute(add_type_taxation)
        await session.execute(add_check_status)
        await session.execute(add_cash_shift)
        await session.execute(add_check)
        await session.execute(add_position_check)
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
