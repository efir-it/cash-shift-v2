from ast import List

import pytest
from aio_pika import IncomingMessage, Message
from fastapi.testowner import TestClient

from cash_shift.dao import CheckoutShiftDAO
from cash_shift.schemas import CashShiftSchemas
from config import settings
from event.consumer import ConsumerMethods
from event.dao import EventDAO
from event.schemas import EventSchemas
from main import app

owner = TestClient(app)


# @pytest.mark.rabbit
# async def test_ack():
#     message_body = {
#         "eventId": "a1835b00-3c35-49af-988d-1257bbd251c3",
#         "ackDestination": "checkoutShift/eventAck",
#     }
#     message = Message(body=str.encode(str(message_body)), app_id=1)
#     await ConsumerMethods.process_incoming_ack(IncomingMessage(message))
#     event: EventSchemas = EventDAO.find_by_id(message_body["eventId"])

#     assert event.id == message["eventId"]
#     assert event.status == "response_received"


# @pytest.mark.rabbit
# async def test_remove_organization():
#     message_body = {
#         "eventId": "a1835b00-3c35-49af-988d-1257bbd251c3",
#         "ackDestination": "checkoutShift/eventAck",
#         "ownerId": "8a88ebd2-6432-41d4-9936-3249c22283e3",
#         "organizationId": "fa71b782-156d-436c-aa20-392954227029",
#     }
#     await ConsumerMethods.process_incoming_remove_organization(message)

#     cashshifts = CheckoutShiftDAO.get_all(
#         **{"organization_id": message["organizationId"]}
#     )
#     for cashshift in cashshifts:
#         assert cashshift.hide == True


# @pytest.mark.rabbit
# async def test_remove_store():
#     message_body = {
#         "eventId": "a1835b00-3c35-49af-988d-1257bbd251c3",
#         "ackDestination": "checkoutShift/eventAck",
#         "ownerId": "8a88ebd2-6432-41d4-9936-3249c22283e3",
#         "organizationId": "fa71b782-156d-436c-aa20-392954227029",
#         "storeId": "61a919d8-6084-4d51-a643-1ab711ef6c2b",
#     }
#     await ConsumerMethods.process_incoming_remove_organization(message)

#     cashshifts = CheckoutShiftDAO.get_all(
#         **{"store_id": message["storeId"], "organizationId": message["organizationId"]}
#     )
#     for cashshift in cashshifts:
#         assert cashshift.hide == True
