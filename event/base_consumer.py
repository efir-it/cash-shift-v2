from aio_pika import connect_robust

from config import settings
from event.base_producer import AckProducer
from event.consumer import ConsumerMethods


class Consumer:
    """
    Класс получатель сообщений.

    Атрибуты
    --------
    event_consumers: List[str]
        список прослушиваемых очередей RabbitMQ
    process_incoming_message: dict
        словарь для сопоставления очередь: функция обработки сообщений

    """

    process_incoming_message_methods = {
        "checkoutShift/eventAck": ConsumerMethods.process_incoming_ack,
        "checkoutShift/removeWorkplace": ConsumerMethods.process_incomig_remove_workplace,
        "checkoutShift/removeStore": ConsumerMethods.process_incoming_remove_store,
        "checkoutShift/removeOrganization": ConsumerMethods.process_incoming_remove_organization,
    }
    events_consumer = process_incoming_message_methods.keys()

    async def process_incoming_message(self, message):
        await self.process_incoming_message_methods[message.routing_key](message)
        if message.routing_key != "checkoutShift/eventAck":
            ack_producer = AckProducer(message=message)
            ack_producer.send_ack()
            ack_producer.connection_close()

    async def consume(self, loop):
        """
        Инициализация получателя сообщений.

        Параметры
        ---------
        loop: asyncio.loop

        """
        connection = await connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASS,
            loop=loop,
        )
        channel = await connection.channel()

        for event in self.events_consumer:
            queue = await channel.declare_queue(event, durable=True)
            await queue.consume(self.process_incoming_message, no_ack=False)

        return connection
