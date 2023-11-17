from dataclasses import dataclass
from .frame import Frame


@dataclass
class ArchiveFromHistory:
    title: str
    n_frames: int
    ratio: float
    completed: bool
    type: str
    created_at: int
    _id: str | int
    url: str | None = None
    image: bytes | None = None
