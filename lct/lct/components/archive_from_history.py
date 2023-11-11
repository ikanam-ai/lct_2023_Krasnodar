import pickle
from datetime import datetime

import streamlit as st
from models.archive_from_history import ArchiveFromHistory
from pymongo.collection import Collection


def archive_from_history(data: ArchiveFromHistory, forward: callable) -> bool:
    key = data._id
    with st.container():
        cols = st.columns(2)
        if data.image:
            cols[0].image(pickle.loads(data.image))
        data_col = cols[1]
        data_col.subheader(data.title)
        data_col.text(f"Распознавание окончено: {'Да' if data.completed else 'Нет'}")
        data_col.text(f"Уровень сжатия: {data.ratio}")
        data_col.text(f"Распознавался каждый: {data.n_frames} кадр")
        data_col.text(f"Дата распознавания: {datetime.fromtimestamp(data.created_at)}")
        more = data_col.button(f"К распознанным кадрам", key=key, on_click=forward)
        st.divider()

    return more
