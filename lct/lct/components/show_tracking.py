import pickle
import streamlit as st
from PIL import Image, ImageDraw
from pymongo.collection import Collection

from models.archive_from_history import ArchiveFromHistory
from models.frame import Frame
from utils.draw_recs_on_img import draw_rectangles_on_image


def get_centres(frames: list[Frame]) -> list[tuple[Frame, float, float]]:
    centers = []
    for frame in frames:
        if not frame['rects']:
            continue
        rect = frame['rects'][-1]
        if rect['conf'] < 0.65:
            continue
        x1, y1 = rect['left']
        x2, y2 = rect['right']

        center = (frame, int((x1 + x2) // 2), int((y1 + y2) // 2))
        centers.append(center)

    return centers


def draw_line(centers: list[tuple[Frame, int, int]]):
    images = []
    max_ = len(centers)
    for i in range(1, max_):
        frame = centers[i][0]
        image = Image.fromarray(pickle.loads(frame['image']), 'RGB')
        image_with_rectangles = draw_rectangles_on_image(image, frame['rects'])
        draw = ImageDraw.Draw(image_with_rectangles)
        for j in range(i):
            x1, y1 = centers[j][1], centers[j][2]
            x2, y2 = centers[j - 1][1], centers[j - 1][2]
            draw.line((x1, y1, x2, y2), fill=(255, 0, 0), width=20)
        images.append(image_with_rectangles)

    return images


def loop(frames: list):
    c = 0
    while True:
        yield frames[c % len(frames)]
        c += 1


def back(id_):
    col: Collection = st.session_state.mongo_db.archives_collection

    def inner():
        st.session_state.__setitem__("arc", ArchiveFromHistory(**col.find_one({"_id": id_})))
        st.session_state.__setitem__("track", None)

    return inner


def show_tracking(id_):
    frames: Collection = st.session_state.mongo_db.frames_collection
    frames = list(frames.find({"arc_id": id_}).limit(50))
    st.button("Назад", on_click=back(id_), key=f"back_TO_FL_{id_}")
    centers = get_centres(frames)
    images = draw_line(centers)
    stframe = st.empty()
    for img in loop(images):
        stframe.image(img)
