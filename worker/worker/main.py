import concurrent

from .ai_models.yolo_model import YoloModel
from .config import Config
from .rabbit.consumers.video_consumer import TaskConsumer
from .services.mongo import Mongo
from .services.notificator import Notificator

config = Config(override=True)

mongo = Mongo(config)


def prcs():
    try:
        yolo = YoloModel(config.MODEL_PATH)
        notificator = Notificator(config)
        TaskConsumer(
            queue_name=config.EXCHANGE_NAME,
            binding_key=config.BINDING_KEY,
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            username=config.RABBITMQ_USER,
            password=config.RABBITMQ_PASSWORD,
            mongo=mongo,
            yolo=yolo,
            notificator=notificator
        ).consume()
    except Exception as e:
        print(e)
        prcs()



def main() -> None:
    prcs()
    # with concurrent.futures.ProcessPoolExecutor(config.PROCESSES) as executor:
    #     futures = {executor.submit(prcs): arg for arg in range(config.PROCESSES)}
    #     for future in concurrent.futures.as_completed(futures):
    #         pass
