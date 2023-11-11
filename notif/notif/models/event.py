from pydantic import BaseModel


class Event(BaseModel):
    message: str
    type: str | None
    url: str | None
