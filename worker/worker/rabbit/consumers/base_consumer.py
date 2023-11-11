import logging
from abc import ABC, abstractmethod

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from ..connection import RabbitMQConnection
from ...config import Config


class RabbitMQConsumerBase(ABC):
    def __init__(self, queue_name: str, binding_key: str, host, port: int, username: str, password: str):
        self.queue_name: str = queue_name
        self.binding_key: str = binding_key
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.config: Config = Config()

    @abstractmethod
    def process_message(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties,
                        body: bytes) -> None:
        pass

    def on_message_callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties,
                            body: bytes) -> None:
        self.process_message(channel, method, properties, body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self) -> None:
        with RabbitMQConnection(self.host, self.port, self.username, self.password) as connection:
            channel = connection.get_channel()
            channel.exchange_declare(exchange=self.config.EXCHANGE_NAME, exchange_type="fanout", durable=True)
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.queue_bind(queue=self.queue_name, exchange=self.config.EXCHANGE_NAME,
                               routing_key=self.binding_key)
            channel.basic_consume(
                queue=self.queue_name,
                auto_ack=False,
                on_message_callback=self.on_message_callback,
            )
            logging.info(f"Started consuming messages from queue: {self.queue_name}")

            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()

            logging.info("Consumer stopped")
