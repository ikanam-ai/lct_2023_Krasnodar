import tempfile
import cv2
from typing import Iterable
from numpy import ndarray

from ..models.task import Task
from ..models.rectangle import Rectangle


def open_video(task: Task) -> cv2.VideoCapture:
    if task.type == "video":
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(task.data)
        temp_file_path = temp_file.name
        temp_file.close()
        return cv2.VideoCapture(temp_file_path)

    return cv2.VideoCapture(task.data)


def convert_video(video: cv2.VideoCapture, n_frames: int, ratio: float) -> Iterable[ndarray]:
    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if frame_count % n_frames != 0:
            continue
        if ratio != 1:
            size = (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio))
            frame = cv2.resize(frame, size)
        frame_count += 1
        yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    video.release()


def rects_to_dict(lst: list[Rectangle]) -> list[dict]:
    return [i.__dict__ for i in lst]
