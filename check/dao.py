import datetime
from typing import Optional

from sqlalchemy import Select, and_, select, true

import position_check.utils as position_utils
from check.models import Check
from check.utils import CheckStatuses, change_format
from dao.base import BaseDAO
from position_check.dao import PositionCheckDAO
from database import async_session_maker


class CheckDAO(BaseDAO):
    model = Check

    @classmethod
    async def get_check_with_positions(
        cls, check, positions: list = None
    ) -> Optional[dict]:
        return (
            change_format(
                {
                    **check.__dict__,
                    "positions": (
                        await PositionCheckDAO.json_get_all({"check_id": check.id})
                    )["positions_check"]
                    if positions is None
                    else positions,
                }
            )
            if check is not None
            else None
        )

    @classmethod
    async def json_find_one(cls, id, filter_by: dict = {}) -> Optional[dict]:
        check = await cls.get_one_or_none({"id": id, **filter_by})

        return await cls.get_check_with_positions(check)

    @classmethod
    async def json_get_all(cls, filter_by: dict = {}) -> dict:
        checks = await cls.get_all(filter_by)

        return (
            {"checks": [await cls.get_check_with_positions(check) for check in checks]}
            if checks is not None
            else None
        )

    @classmethod
    async def json_get_several(cls, filter_by: dict = {}) -> dict:
        time_start = filter_by.pop("time_start", None)
        time_end = filter_by.pop("time_end", None)
        count = filter_by.pop("count", None)

        if count is None:
            count = 100000000

        async with async_session_maker() as session:
            query: Select = (
                select(cls.model)
                .filter_by(
                    **filter_by,
                )
                .where(
                    and_(
                        (
                            cls.model.date
                            > datetime.datetime.strptime(
                                time_start, "%Y-%m-%dT%H:%M:%S"
                            )
                        )
                        if time_start
                        else true()
                    )
                )
                .where(
                    and_(
                        (
                            cls.model.date
                            < datetime.datetime.strptime(time_end, "%Y-%m-%dT%H:%M:%S")
                        )
                        if time_end
                        else true()
                    )
                )
            )

        checks = [row[0] for row in (await session.execute(query)).fetchall()].sort(
            key=lambda check: check.date, reverse=True
        )
        return (
            {"checks": [change_format(check.__dict__) for check in checks[:count]]}
            if checks is not None
            else None
        )

    @classmethod
    async def json_add(cls, data: dict) -> Optional[dict]:
        positions_check = data.pop("positions", [])
        check = await cls.add(data)
        for position_num, position in enumerate(positions_check):
            await PositionCheckDAO.add(
                {
                    **position_utils.change_format(position),
                    "owner_id": check.owner_id,
                    "check_id": check.id,
                    "position": position_num + 1,
                }
            )
        return await cls.get_check_with_positions(check)

    @classmethod
    async def json_remove(cls, id, filter_by: dict = {}) -> Optional[dict]:
        positions = await PositionCheckDAO.json_get_all({"check_id": id})
        checks = await cls.delete({**filter_by, "id": id})

        return (
            await cls.get_check_with_positions(checks[0], positions)
            if checks is not None and len(checks) > 0
            else None
        )

    @classmethod
    async def json_update(
        cls, id, filter_by: dict = {}, data: dict = {}
    ) -> Optional[dict]:
        checks = await cls.update({"id": id, **filter_by}, data)

        return (
            await cls.get_check_with_positions(checks[0])
            if checks is not None and len(checks) > 0
            else None
        )
