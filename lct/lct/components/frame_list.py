import pickle

import streamlit as st
from PIL import ImageDraw, Image, ImageFont
from models.archive_from_history import ArchiveFromHistory
from models.frame import Frame
from models.rectangle import Rectangle
from pymongo.collection import Collection
import streamlit_antd_components as sac

from utils.draw_recs_on_img import draw_rectangles_on_image


def edit_image(frame: Frame, img: Image):
    st.session_state['frame'] = (frame, img, st.session_state['arc'])
    st.session_state['arc'] = None


def draw_frame(place, frame: Frame):
    image = Image.fromarray(pickle.loads(frame.image), 'RGB')
    image_with_rectangles = draw_rectangles_on_image(image, frame.rects)
    place.image(image_with_rectangles, caption=f"Номер кадра: {frame.position}")
    place.button("Редактировать", use_container_width=True, key=f"edit_{frame.position}",
                 on_click=lambda: edit_image(frame, image))


def show_pages(id_, f_key: str = "arc_id"):
    frames: Collection = st.session_state.mongo_db.frames_collection
    total = frames.count_documents({f_key: id_})
    if total == 0:
        st.subheader("Тут пока ничего нет"),
    else:
        page_size = 50
        page = sac.pagination(total=total, align='center', jump=True, show_total=True, page_size=page_size)
        skip = int((page - 1) * page_size)
        cols_count = 2
        cols = st.columns(cols_count)
        for i, frame in enumerate(frames.find({f_key: id_}).limit(page_size).skip(skip)):
            draw_frame(cols[i % cols_count], Frame(**frame))


def frame_list(id_, title: str, back: callable, f_key: str = "arc_id") -> None:
    with st.container():
        st.button("Назад", on_click=back, key=f"back_{title}")
        st.text(title)

        show_pages(id_, f_key)
