import pickle

import streamlit as st
import streamlit_antd_components as sac
from models.frame import Frame
from pymongo.collection import Collection


def fake_frame(place, frame: Frame, arc: Collection):
    place.image(pickle.loads(frame.image))
    place.text(f"{frame.position} кадр")
    arc = arc.find_one({"_id": frame.arc_id})
    if arc:
        place.text(f"Файл: {arc['title']}")
    place.divider()


def main() -> None:
    fakes: Collection = st.session_state.mongo_db.fake_collection
    arc: Collection = st.session_state.mongo_db.archives_collection
    total = fakes.count_documents({})
    if total == 0:
        st.subheader("Тут пока ничего нет"),
    else:
        page_size = 30
        page = sac.pagination(total=total, align='center', jump=True, show_total=True, page_size=page_size)
        skip = int((page - 1) * page_size)
        cols_count = 2
        cols = st.columns(cols_count)
        for i, fake in enumerate(fakes.find({}).limit(page_size).skip(skip)):
            fake_frame(cols[i % cols_count], Frame(**fake), arc)