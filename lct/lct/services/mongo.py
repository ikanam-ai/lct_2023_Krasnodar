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
    def teach_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['teach']

    @property
    def frames_collection(self) -> Collection:
        return self.client[self.config.MONGO_DATABASE]['frames']

    def _clear_all(self):
        for col in (self.archives_collection, self.users_collection, self.rtc_collection, self.teach_collection,
                    self.frames_collection):
            col.delete_many({})
