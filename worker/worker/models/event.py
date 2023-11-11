from dataclasses import dataclass


@dataclass
class Event:
    message: str
    type: str | None
    url: str | None
