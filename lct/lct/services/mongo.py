from config import Config
from pymongo import MongoClient
from pymongo.collection import Collection


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
    def archives_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['archives']

    @property
    def users_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['users']

    @property
    def rtc_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['rtc']

    @property
    def fake_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['fake']

    @property
    def frames_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['frames']
