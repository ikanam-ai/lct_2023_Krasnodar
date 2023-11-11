from pydantic import BaseModel
from .event import Event


class Message(BaseModel):
    pswd: str
    event: Event
