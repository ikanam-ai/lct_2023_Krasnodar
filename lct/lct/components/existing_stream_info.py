from datetime import datetime

import streamlit as st
from dataclasses import dataclass
from numpy import ndarray


@dataclass
class ExistingStreamInfo:
    name: str
    detection_count: int
    description: None | str
    added_at: int
    resolution: tuple[int, int]
    threshold: float
    n_frame: int
    id_: str | int


def to_edit(img: ndarray) -> None:
    st.session_state['img'] = img


def existing_steam_info(img: ndarray, data: ExistingStreamInfo) -> None | bool:
    cols = st.columns(2)

    cols[0].image(img)
    cols[1].subheader(data.name)
    cols[1].text_input(label="Количество распознований", value=data.detection_count, disabled=True)
    cols[1].date_input(label="Добавлено", value=datetime.fromtimestamp(data.added_at), disabled=True)
    cols[1].text_input(label="Разрешение", value=f"{data.resolution[0]} x {data.resolution[1]}", disabled=True)
    cols[1].text_input(label="Threshold", value=data.threshold, disabled=True)
    cols[1].text_input(label="Распознается каждый n кадр", value=str(data.n_frame), disabled=True)
    btn = cols[1].button("Подробнее", use_container_width=True, on_click=lambda: to_edit(img))
    st.divider()

    return btn
