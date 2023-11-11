from pymongo import MongoClient
from pymongo.collection import Collection

from ..config import Config


class Mongo:
    def __init__(self, config: Config):
        self.config = config
        self.client: MongoClient = MongoClient(
            host=[f"{config.MONGO_HOST}:{config.MONGO_PORT}"],
            serverSelectionTimeoutMS=3000,
            username=config.MONGO_USERNAME,
            password=config.MONGO_PASSWORD,
        )

    @property
    def archives(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['archives']

    @property
    def frames(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['frames']

    @property
    def rtc(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['rtc']