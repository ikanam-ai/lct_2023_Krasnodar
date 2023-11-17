import os
import zipfile
import cv2
from typing import IO, Iterable
from numpy import ndarray
from models.task import Task


def create_thumbnail(video_path: str) -> ndarray | None:
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()

    return frame if ret else None


def extract_videos(archive_path: IO[bytes], extract_folder: str) -> None:
    os.makedirs(extract_folder, exist_ok=True)
    if archive_path.name.endswith("mp4"):
        with open(os.path.join(extract_folder, archive_path.name), "wb") as f:
            f.write(archive_path.read())
    else:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)


def files_to_queue_models(path: str, settings: list[tuple[float, float, int]]) -> Iterable[Task]:
    for file, s in zip(os.listdir(path), settings):
        video_path = os.path.join(path, file)
        with open(video_path, 'rb') as f:
            threshold, ratio, n_frames = s
            yield Task(title=file, ratio=ratio, data=f.read(), threshold=threshold, n_frames=n_frames, type="video")
        os.remove(video_path)


def urls_to_queue_models(urls: list[str], params: list[tuple[float, float, int]]) -> Iterable[Task]:
    for url, param in zip(urls, params):
        title = url.split("@")[1]
        threshold, ratio, n_frames = param
        yield Task(title=title, ratio=ratio, data=url, threshold=threshold, n_frames=n_frames, type="rtc", url=url)
