import streamlit as st
import streamlit_antd_components as sac
from components.archive_from_history import archive_from_history
from components.frame_list import frame_list
from components.edit_img import edit_img
from models.archive_from_history import ArchiveFromHistory
from pymongo.collection import Collection


def show_list(archive: Collection) -> bool:
    st.title("История распознаваний из архива")
    total = archive.count_documents({})
    if total == 0:
        st.subheader("Тут пока ничего нет"),
        st.text("Можно отправить архив в специальном разделе"),
    else:
        page_size = 10
        page = sac.pagination(total=total, align='center', jump=True, show_total=True, page_size=page_size)
        skip = int((page - 1) * page_size)
        for arc in archive.find({}).limit(page_size).skip(skip):
            arc = ArchiveFromHistory(**arc)
            archive_from_history(arc, forward=lambda a=arc: st.session_state.__setitem__("arc", a))


def save(rects):
    frame, img, arc = st.session_state.get('frame')
    frames: Collection = st.session_state.mongo_db.frames_collection
    frames.update_one({"_id": frame._id}, {"$set": {"rects": rects}})
    st.toast("Изменения сохранены")
    back("frame")()


def mark_fake():
    frame, img, arc = st.session_state.get('frame')
    fakes: Collection = st.session_state.mongo_db.fake_collection
    frames: Collection = st.session_state.mongo_db.frames_collection
    frames.delete_one({"_id": frame._id})
    fakes.insert_one(frame.__dict__)

    st.toast("Кадр плмечен как ложный")
    back("frame")()


def back(path: str) -> callable:
    return lambda: st.session_state.__setitem__(path, None)


def main() -> None:
    archive: Collection = st.session_state.mongo_db.archives_collection
    if st.session_state.get('frame'):
        edit_img(st.session_state.get('frame'), back("frame"), save, mark_fake)
    elif st.session_state.get('arc'):
        arc = st.session_state.get('arc')
        frame_list(arc._id, arc.title, back("arc"))
    else:
        show_list(archive)
