import json
import uuid
from datetime import datetime

import pika

from config import settings
from event.dao import EventDAO


class BaseProducer:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(
            username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASS
        )
        params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials,
        )
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def connection_close(self):
        """
        Закрытие соединения.

        """
        self.connection.close()


class Producer(BaseProducer):
    """
    Класс отправитель сообщений.

    """

    module = None
    event = None
    event_consumers = None

    def __init__(self) -> None:
        """
        Инициализация отправителя сообщений.

        Параметры
        ---------
        module: str
            наименование модуля
        event_consumers: list[str]
            модули - получатели
        event: str
            наименование события

        """
        super().__init__()
        self.callback_queue = self.channel.queue_declare(
            queue=f"{self.module}/eventAck", durable=True
        )

    async def send_messages(self, message: dict):
        """
        Отправка сообщений.

        Атрибуты
        --------
        message: dict
            сообщение для отправки

        """

        for consumer in self.event_consumers:
            queue = f"{consumer}/{self.event}"
            self.channel.queue_declare(queue=queue, durable=True)
            event = await EventDAO.add(
                data={
                    "status": "created",
                    "queue": queue,
                    "message": str(message),
                    "send_time": datetime.utcnow(),
                }
            )
            message["eventId"] = str(event.id)
            message["ackDestination"] = f"{self.module}/eventAck"
            self.channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=json.dumps(message),
            )
            event = await EventDAO.update(
                filter_by={"id": event.id},
                data={"status": "send", "message": str(message)},
            )


class AckProducer(BaseProducer):
    module = None

    def __init__(self, message) -> None:
        super().__init__()
        self.body = json.loads(message.body)
        self.queue = self.body["ackDestination"]
        self.channel.queue_declare(queue=self.queue, durable=True)

    def send_ack(self):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(
                {"eventId": self.body["eventId"], "ackDestination": self.queue}
            ),
        )
