from numpy import ndarray
from ultralytics import YOLO
from ultralytics.engine.results import Results

from ..models.rectangle import Rectangle


class YoloModel(YOLO):
    def __init__(self, model_path: str):
        super().__init__(model_path)

    def predict_(self, frame: ndarray) -> list[Rectangle]:
        rectangles = []
        results: Results = self.predict(frame)
        for result in results:
            name = ", ".join(result.names.values())
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                borders = box.xyxy[0].tolist()
                left, right = tuple(borders[:2]), tuple(borders[2:])
                conf, cls = box.conf.tolist()[0], name
                rectangles.append(Rectangle(left=left, right=right, conf=conf, cls=cls))

        return rectangles
