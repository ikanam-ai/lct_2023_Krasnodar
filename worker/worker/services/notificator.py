import requests
from ..config import Config
from ..models.event import Event


class Notificator:
    def __init__(self, config: Config):
        self.config = config
        self._url = config.NOTIF_URL
        self._pswd = config.ADMIN_NOTIF_PSWD

    def notify(self, event: Event) -> None:
        try:
            data = event.__dict__
            requests.post(f"{self._url}/accept", json=data)
        except:
            pass
