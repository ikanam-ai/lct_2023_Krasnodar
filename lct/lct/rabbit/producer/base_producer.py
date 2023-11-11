from pika import exceptions as pika_exceptions
from pika.adapters.blocking_connection import BlockingChannel
from abc import ABC

from ..connection import RabbitMQConnection


class RabbitMQProducer(ABC):
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection
        self.channel: BlockingChannel | None = None

    def publish_message(self, exchange: str, routing_key: str, data: bytes):
        if self.channel is None:
            self.channel = self.connection.get_channel()

        if self.channel is not None:
            try:
                self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=data,
                    properties=None,
                )
                print(f"Message sent to exchange: {exchange} with routing_key {routing_key}")
            except pika_exceptions.ConnectionClosedByBroker:
                print("Connection closed by broker. Failed to publish the message")
        else:
            print("Failed to obtain a channel for publishing the message")
