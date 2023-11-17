import pickle
from datetime import datetime

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from .base_consumer import RabbitMQConsumerBase
from ...ai_models.yolo_model import YoloModel
from ...models.task import Task
from ...models.event import Event
from ...models.rectangle import Rectangle
from ...services.mongo import Mongo
from ...services.notificator import Notificator
from ...utils.video_converter import open_video, convert_video, rects_to_dict


class TaskConsumer(RabbitMQConsumerBase):
    def __init__(self, queue_name: str, binding_key: str, host: str, port: int, username: str, password: str,
                 mongo: Mongo, yolo: YoloModel, notificator: Notificator):
        super().__init__(queue_name, binding_key, host, port, username, password)
        self.mongo = mongo
        self.yolo = yolo
        self.notificator = notificator
        self._entity_id = None

    def process_message(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties,
                        body: bytes) -> None:
        task: Task = Task(**pickle.loads(body))
        frames = convert_video(open_video(task), task.n_frames, task.ratio)
        if task.type == "video":
            self._process_video(task, frames)
        else:
            self._process_rtc(task, frames)

    def _process_video(self, task: Task, frames):
        self._entity_id = self.mongo.archives.insert_one(
            {"title": task.title, "n_frames": task.n_frames, "ratio": task.ratio,
             'completed': False, "type": task.type,
             "created_at": datetime.now().timestamp()}).inserted_id
        has_image = False
        for i, frame in enumerate(frames):
            position = i * task.n_frames
            rects = self.yolo.predict_(frame)
            if not has_image:
                self.mongo.archives.update_one({"_id": self._entity_id},
                                               {"$set": {"image": pickle.dumps(frame)}})
            if not rects:
                continue
            frame = {"position": position, "rects": rects_to_dict(rects), "image": pickle.dumps(frame),
                     "arc_id": self._entity_id}
            self.mongo.frames.insert_one(frame)
            has_image = True
        self.mongo.archives.update_one({"_id": self._entity_id},
                                       {"$set": {"completed": True}})

    def _process_rtc(self, task: Task, frames):
        self._entity_id = self.mongo.rtc.insert_one(
            {"title": task.title, "n_frames": task.n_frames, "ratio": task.ratio, "url": task.url,
             'completed': False, "type": task.type, "created_at": datetime.now().timestamp()}).inserted_id
        has_image = False
        for i, frame in enumerate(frames):
            if not has_image:
                self.mongo.rtc.update_one({"_id": self._entity_id},
                                          {"$set": {"image": pickle.dumps(frame)}})
            rects = self.yolo.predict_(frame)
            time = datetime.now().timestamp()
            if not rects:
                continue
            frame = {"time": time, "rects": rects_to_dict(rects), "arc_id": self._entity_id,
                     "image": pickle.dumps(frame)}
            self.mongo.frames.insert_one(frame)
            has_image = True
        self.mongo.archives.update_one({"_id": self._entity_id},
                                       {"$set": {"completed": True}})

    def notify(self, rects: list[Rectangle]):
        url = str(self._entity_id)
        founded = ", ".join([str(rect.cls) for rect in rects])
        message = f"В трансляции {self._entity_id} найдены: {founded}"
        self.notificator.notify(Event(message=message, url=url, type="live"))
