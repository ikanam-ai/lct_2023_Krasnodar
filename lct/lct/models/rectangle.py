from dataclasses import dataclass


@dataclass
class Rectangle:
    left: tuple[int, int]
    right: tuple[int, int]
    conf: float
    cls: int
