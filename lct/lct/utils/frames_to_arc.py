import os
import pickle
import zipfile
import shutil
from PIL import Image

from models.frame import Frame
from models.rectangle import Rectangle

yml = """train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1
names: ['market']"""


def load_cls():
    return {
        "market": 0
    }


def rec_to_yolo(frame: Frame, rec: Rectangle) -> str:
    if rec:
        cls = load_cls()
        h, w, _ = pickle.loads(frame.image).shape
        x1, y1 = rec['left']
        x2, y2 = rec['right']
        x_ = (x1 + x2) / 2 / w
        y_ = (y1 + y2) / 2 / h
        w_ = (x2 - x1) / w
        h_ = (y2 - y1) / h
        return f"{cls[rec['cls']]} {x_} {y_} {w_} {h_}"
    return ""


def frames_to_arc(frames: list[Frame], user: str) -> str:
    # Создаем временную папку для сохранения изображений и файлов
    temp_folder = os.path.join("temp_zip_folder", user)
    train_folder = os.path.join(temp_folder, "train")
    output_zip_path = os.path.join(temp_folder, "teach_data.zip")
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(train_folder, exist_ok=True)
    images_folder = labels_path = temp_folder
    yml_file = os.path.join(temp_folder, 'data.yaml')
    try:
        with open(yml_file, "w", encoding="utf-8") as t_yaml:
            t_yaml.write(yml)
        for frame in frames:
            frame = Frame(**frame)
            images_folder = os.path.join(train_folder, "images")
            os.makedirs(images_folder, exist_ok=True)
            image_path = os.path.join(images_folder, f"{frame._id}.jpg")
            image = Image.fromarray(pickle.loads(frame.image), 'RGB')
            with open(image_path, "wb") as image_file:
                image.save(image_file)

            labels_path = os.path.join(train_folder, "labels")
            os.makedirs(labels_path, exist_ok=True)
            label_path = os.path.join(labels_path, f"{frame._id}.txt")
            with open(label_path, "w", encoding="utf-8") as labels_file:
                for rect in frame.rects:
                    labels_file.write(rec_to_yolo(frame, rect))

        with zipfile.ZipFile(output_zip_path, "w") as zip_file:
            for foldername, subfolders, filenames in os.walk(temp_folder):
                for filename in filenames:
                    if filename in output_zip_path:
                        continue
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, temp_folder)
                    zip_file.write(filepath, arcname)

    finally:
        shutil.rmtree(train_folder)
        os.remove(yml_file)

    return output_zip_path
