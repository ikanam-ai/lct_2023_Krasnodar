from dataclasses import dataclass
from .rectangle import Rectangle


@dataclass
class Frame:
    rects: list[Rectangle]
    image: bytes
    _id: str | int
    arc_id: str | int
    position: int | None = None
    time: int | None = None
