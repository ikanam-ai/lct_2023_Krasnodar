from dataclasses import dataclass
from .rectangle import Rectangle


@dataclass
class Frame:
    position: int
    rects: list[Rectangle]
    image: bytes
    _id: str | int
    arc_id: str | int
