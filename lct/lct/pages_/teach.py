import pickle

import streamlit as st
import streamlit_antd_components as sac
from PIL import Image

from models.frame import Frame
from components.edit_img import edit_img
from pymongo.collection import Collection

from utils.draw_recs_on_img import draw_rectangles_on_image
from utils.frames_to_arc import frames_to_arc


def back():
    st.session_state.__setitem__('edit', None)


def delete_frame(frame):
    frames: Collection = st.session_state.mongo_db.teach_collection
    frames.delete_one({"_id": frame._id})
    st.toast("Кадр удален")


def fake_frame(place, frame: Frame):
    img = draw_rectangles_on_image(Image.fromarray(pickle.loads(frame.image), 'RGB'), frame.rects)
    place.image(img)
    place.button("Редактировать", use_container_width=True,
                 on_click=lambda: st.session_state.__setitem__('edit', frame),
                 key=f"edit_btn_{frame._id}")
    place.button("Удалить", on_click=lambda: delete_frame(frame), use_container_width=True, key=f"del_btn_{frame._id}")

    place.divider()


def download(frames: list[Frame]):
    arc_path = frames_to_arc(frames, st.session_state.username)
    if not arc_path:
        return
    return open(arc_path, "rb")


def show_list():
    st.title("Датасет для дообучения")
    teach: Collection = st.session_state.mongo_db.teach_collection
    total = teach.count_documents({})
    if total == 0:
        st.subheader("Тут пока ничего нет"),
    else:
        st.subheader("Кадры можно отредактировать, а затем экспортировать в формате для обучения yolo v8")
        cols = st.columns(2)
        frames = []
        btn_place = cols[0]
        cols[1].text(f"Изображений на странице: {total}")
        cols = st.columns(2)
        page_size = 30
        page = sac.pagination(total=total, align='center', jump=True, show_total=True, page_size=page_size)
        skip = int((page - 1) * page_size)
        cols_count = 2
        cols = st.columns(cols_count)

        for i, frame in enumerate(teach.find({}).limit(page_size).skip(skip)):
            frames.append(frame)
            fake_frame(cols[i % cols_count], Frame(**frame))
        btn_place.download_button("Скачать сохраненные данные", download(frames), file_name="data.zip",
                                  use_container_width=True)


def save(rects):
    frame: Frame = st.session_state.get('edit')
    frames: Collection = st.session_state.mongo_db.teach_collection
    frames.update_one({"_id": frame._id}, {"$set": {"rects": rects}})
    st.toast("Изменения сохранены")
    back()


def edit():
    frame: Frame = st.session_state.get('edit')
    edit_img((frame, Image.fromarray(pickle.loads(frame.image), 'RGB'), None), back, save)


def main() -> None:
    if st.session_state.get('edit'):
        edit()
    else:
        show_list()
