from fastapi import APIRouter

from position_check.dao import PositionCheckDAO
from position_check.schemas import PositionCheckSchema

router = APIRouter(prefix="/positions_check", tags=["Позиции чека"])
