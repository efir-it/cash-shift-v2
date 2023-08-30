from sqlalchemy import select
from position_check.models import PositionCheck
from dao.base import BaseDAO
from database import async_session_maker

class PositionCheckDAO(BaseDAO):
    model = PositionCheck
    