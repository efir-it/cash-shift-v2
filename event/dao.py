from dao.base import BaseDAO
from event.models import Event


class EventDAO(BaseDAO):
    model = Event
