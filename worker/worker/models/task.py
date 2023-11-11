from typing import Literal
from dataclasses import dataclass


@dataclass
class Task:
    title: str
    data: bytes
    n_frames: int
    threshold: float
    type: Literal["video", "rtc"]
    ratio: float = 0.5
