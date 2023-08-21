from check.models import Check
from dao.base import BaseDAO


class CheckDAO(BaseDAO):
    model = Check
