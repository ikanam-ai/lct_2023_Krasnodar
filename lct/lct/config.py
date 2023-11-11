from __future__ import annotations

import os


class Config:
    _instance: Config = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self, override: bool = False):
        if self.__initialized and not override:
            return

        self.RABBITMQ_HOST: str = os.environ.get("RABBITMQ_HOST")
        self.RABBITMQ_PORT: int = int(os.environ.get("RABBITMQ_PORT"))
        self.RABBITMQ_USER: str = os.environ.get("RABBITMQ_USER")
        self.RABBITMQ_PASSWORD: str = os.environ.get("RABBITMQ_PASSWORD")
        self.RABBITMQ_VHOST: str = os.environ.get("RABBITMQ_VHOST", "/")
        self.EXCHANGE_NAME: str = os.environ.get("EXCHANGE_NAME")
        self.DEQUE_NAME: str = os.environ.get("DEQUE_NAME")
        self.BINDING_KEY: str = os.environ.get("BINDING_KEY")
        self.MODEL_PATH: str = os.environ.get("MODEL_PATH")
        self.MONGO_HOST: str = os.environ.get("MONGO_HOST")
        self.MONGO_PORT: str = os.environ.get("MONGO_PORT")
        self.MONGO_DATABASE: str = os.environ.get("MONGO_DATABASE")
        self.MONGO_USERNAME: str = os.environ.get("MONGO_USERNAME")
        self.MONGO_PASSWORD: str = os.environ.get("MONGO_PASSWORD")
        self.NOTIF_PSWD: str = os.environ.get("NOTIF_PSWD")
        self.NOTIF_URL: str = os.environ.get("NOTIF_URL")
        self.USER_LOGIN: str = os.environ.get("USER_LOGIN")
        self.USER_PASSWORD: str = os.environ.get("USER_PASSWORD")

        self.__initialized: bool = True

    def waiting_factor(self):
        return 2
