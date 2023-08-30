import json

from event.dao import EventDAO

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
       #return await RmkDAO.delete_by_storeId(body["storeId"])
       
    # @staticmethod
    # async def process_incoming_remove_store(message):
    #     await message.ack()
    #     print(message.info())
    #     body = json.loads(message.body)
    #     return await RmkDAO.delete_by_storeId(body["storeId"])
