import pickle
import tempfile

import streamlit as st
from PIL import Image
from numpy import ndarray
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager
from models.frame import Frame


def to_temp_file(img: Image):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img.save(temp_file)
    temp_file_path = temp_file.name
    temp_file.close()

    return temp_file_path


def convert_rects(frame: Frame):
    return [{
        "left": rect['left'][0],
        "top": rect['left'][1],
        "width": rect['right'][0] - rect['left'][0],
        "height": rect['right'][1] - rect['left'][1],
        "label": rect['cls'],
        "conf": rect['conf']
    } for rect in frame.rects]


def convert_to_rects(rects: list[dict], orig: Frame):
    return [{
        "cls": or_rec['cls'],
        "conf": or_rec['conf'],
        "left": [rect["left"], rect["top"]],
        "right": [rect["width"] + rect['left'], rect["height"] + rect["top"]]
    } for rect, or_rec in zip(rects, orig.rects)]


def edit_img(frame_: tuple[Frame, Image, dict], back: callable, save: callable, fake: callable) -> None:
    frame, img, _ = frame_
    st.button("Назад", on_click=back, key=f"back_edit_{frame.position}")
    st.title("Редактирование распознавания")

    im = ImageManager(to_temp_file(img))
    im._rects = convert_rects(frame)
    resized_img = im.resizing_img()
    resized_rects = im.get_resized_rects()
    rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

    if not rects:
        return
    try:
        preview_imgs = im.init_annotation(rects)
        btn_cols = st.columns(2)
        btn_cols[0].button(label="Сохранить", on_click=lambda: save(convert_to_rects(im._current_rects, frame)),
                           use_container_width=True)
        btn_cols[1].button(label="Ложное срабатывание", on_click=fake, use_container_width=True)
        for i, prev_img in enumerate(preview_imgs):
            prev_img[0].thumbnail((200, 200))
            cols = st.columns(2)
            with cols[0]:
                cols[0].image(prev_img[0])
            with cols[1]:
                val = prev_img[1] or ''
                new_val = cols[1].text_input("Класс", value=val, key=f"class_{val}_{i}")
                im.set_annotation(i, new_val)
    except ValueError:
        st.error("Неверные границы выделения объектов")
