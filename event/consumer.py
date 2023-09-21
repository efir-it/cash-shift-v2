import json
import uuid

from cash_shift.dao import CheckoutShiftDAO
from event.dao import EventDAO


class ConsumerMethods:
    @staticmethod
    async def process_incoming_ack(message):
        await message.ack()
        body = json.loads(message.body)
        await EventDAO.update(
            filter_by={"id": uuid.UUID(body["eventId"])},
            data={"status": "response_received"},
        )

    @staticmethod
    async def process_incomig_remove_workplace(message):
        await message.ack()
        body = json.loads(message.body)
        await CheckoutShiftDAO.hide_by({"workplace_id": uuid.UUID(body["workplaceId"])})

    @staticmethod
    async def process_incoming_remove_store(message):
        await message.ack()
        body = json.loads(message.body)
        await CheckoutShiftDAO.hide_by({"store_id": uuid.UUID(body["storeId"])})

    @staticmethod
    async def process_incoming_remove_organization(message):
        await message.ack()
        body = json.loads(message.body)
        await CheckoutShiftDAO.hide_by(
            {"organization_id": uuid.UUID(body["organizationId"])}
        )
