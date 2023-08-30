import json

from event.dao import EventDAO
from cash_shift.dao import CashShiftDAO

class ConsumerMethods:
    @staticmethod
    async def process_incoming_ack(message):
        await message.ack()
        body = json.loads(message.body)
        return await EventDAO.update(body["id"], {"status": body["status"]})

    @staticmethod
    async def process_incomig_remove_rmk(message):
        await message.ack()
        body = json.loads(message.body)
        return await CashShiftDAO.hide_by_rmk_id(body["workplaceId"])
       
    @staticmethod
    async def process_incoming_remove_store(message):
        await message.ack()
        body = json.loads(message.body)
        return await CashShiftDAO.hide_by_store_id(body["storeId"])
        
    @staticmethod
    async def process_incoming_remove_organization(message):
        await message.ack()
        body = json.loads(message.body)
        return await CashShiftDAO.hide_by_organization_id(body["organizationId"])