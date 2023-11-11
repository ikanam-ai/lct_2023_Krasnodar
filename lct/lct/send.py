import pickle

from config import Config
from rabbit.connection import RabbitMQConnection
from rabbit.producer.base_producer import RabbitMQProducer
from utils.from_archive import to_queue_models


def send_videos_to_queue(temp_folder: str, files_params: list[tuple[float, float, int]]) -> None:
    config = Config()

    with RabbitMQConnection(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT, username=config.RABBITMQ_USER,
                            password=config.RABBITMQ_PASSWORD) as connection:
        producer = RabbitMQProducer(connection)
        for video in to_queue_models(temp_folder, files_params):
            data = pickle.dumps(video.__dict__)
            producer.publish_message(exchange=config.EXCHANGE_NAME, data=data,
                                     routing_key=config.BINDING_KEY)


def send_urls_to_queue(urls: list[str]) -> None:
    config = Config()

    with RabbitMQConnection(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT, username=config.RABBITMQ_USER,
                            password=config.RABBITMQ_PASSWORD) as connection:
        producer = RabbitMQProducer(connection)
        for url in urls:
            ...
