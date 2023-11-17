import streamlit as st
import streamlit_antd_components as sac
from components.archive_from_history import archive_from_history
from components.frame_list import frame_list
from components.edit_img import edit_img
from components.show_tracking import show_tracking
from components.watch import watch
from models.archive_from_history import ArchiveFromHistory
from pymongo.collection import Collection


def to_watch(arc: ArchiveFromHistory):
    return lambda: st.session_state.__setitem__('watch', arc)


def show_list(collection: Collection, title: str, show_watch: bool = False):
    st.title(title)
    total = collection.count_documents({})
    if total == 0:
        st.subheader("Тут пока ничего нет"),
        st.text("Можно отправить архив в специальном разделе"),
    else:
        page_size = 10
        page = sac.pagination(total=total, align='center', jump=True, show_total=True, page_size=page_size)
        skip = int((page - 1) * page_size)
        for arc in collection.find({}).limit(page_size).skip(skip):
            arc = ArchiveFromHistory(**arc)
            watch_ = to_watch(arc)
            archive_from_history(arc, forward=lambda a=arc: st.session_state.__setitem__("arc", a),
                                 watch=watch_ if show_watch else None)


def save(rects):
    frame, img, arc = st.session_state.get('frame')
    frames: Collection = st.session_state.mongo_db.frames_collection
    frames.update_one({"_id": frame._id}, {"$set": {"rects": rects}})
    st.toast("Изменения сохранены")
    back("frame")()


def mark_fake():
    frame, img, arc = st.session_state.get('frame')
    teaches: Collection = st.session_state.mongo_db.teach_collection
    frames: Collection = st.session_state.mongo_db.frames_collection
    frames.delete_one({"_id": frame._id})
    teaches.insert_one(frame.__dict__)

    st.toast("Кадр отправлен в раздел 'Обучение'")
    back("frame")()


def back(path: str) -> callable:
    return lambda: st.session_state.__setitem__(path, None)


def history(collection: Collection, title: str, show_watch: bool = False):
    if st.session_state.get('frame'):
        edit_img(st.session_state.get('frame'), back("frame"), save, mark_fake)
    elif st.session_state.get('track'):
        show_tracking(st.session_state.get('track'))
    elif st.session_state.get('arc'):
        arc = st.session_state.get('arc')
        frame_list(arc._id, arc.title, back("arc"))
    elif st.session_state.get('watch'):
        watch(st.session_state.get('watch'), back("watch"))
    else:
        show_list(collection, title, show_watch)


def main() -> None:
    res = sac.tabs([
        sac.TabsItem(label='Архивы'),
        sac.TabsItem(label='Трансляции'),
    ], format_func='title', key="history_type", align='center')
    if res == "Архивы":
        history(st.session_state.mongo_db.archives_collection, "История распознаваний из архива")
    else:
        history(st.session_state.mongo_db.rtc_collection, "Распознаваемые трансляции", True)
