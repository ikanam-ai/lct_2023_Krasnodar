from __future__ import annotations

import logging
import time

from pika import PlainCredentials, ConnectionParameters, BlockingConnection, exceptions
from pika.adapters.blocking_connection import BlockingChannel
from config import Config

class RabbitMQConnection:
    _instance: RabbitMQConnection | None = None

    def __new__(cls, host: str, port: int, username: str, password: str):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, host: str, port: int, username: str, password: str):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.connection: BlockingConnection | None = None

    def __enter__(self) -> RabbitMQConnection:
        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def connect(self):
        retries = 0
        while retries < 10:
            try:
                credentials = PlainCredentials(self.username, self.password)
                parameters = ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
                self.connection: BlockingConnection = BlockingConnection(parameters)
                logging.info("Connected to RabbitMQ")

                return
            except exceptions.AMQPConnectionError as e:
                logging.error(f"Failed to connect to RabbitMQ: {e}")
                retries += 1
                wait_time = Config().waiting_factor() ** retries
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        logging.info("Exceeded maximum number of connection retries. Stopping the code.")

    def is_connected(self) -> bool:
        return self.connection is not None and self.connection.is_open

    def close(self) -> None:
        if self.is_connected():
            self.connection.close()
            self.connection = None
            logging.info("Closed RabbitMQ connection")

    def get_channel(self) -> BlockingChannel | None:
        if self.is_connected():
            return self.connection.channel()

        return None
