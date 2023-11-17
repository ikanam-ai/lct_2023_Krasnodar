import cv2
import streamlit as st
import streamlit_antd_components as sac
from streamlit.runtime.uploaded_file_manager import UploadedFile
from send import send_urls_to_queue
from components.archive_video_params import archive_video_params


def get_urls_from_file() -> list[str]:
    uploaded_file: UploadedFile | None = st.file_uploader("Загрузите zip архив с видео", type=["txt", "csv"])
    urls = uploaded_file.readlines() if uploaded_file else []

    return [url.decode('utf-8').strip() for url in urls]


def get_urls_from_text() -> list[str]:
    rtmp_urls = st.text_area("RTMP-адреса")

    return rtmp_urls.split("\n") if rtmp_urls else []


def check_urls(urls: list[str]) -> list[tuple[str, cv2.typing.MatLike]]:
    res = []
    for url in urls:
        try:
            cap = cv2.VideoCapture(url)
            r, frame = cap.read()
            if cap.isOpened():
                res.append((url, frame))
            cap.release()
        except:
            pass

    return res


def show_streams(imgs: list[tuple[str, str]]) -> list[tuple[float, float, int]]:
    return [archive_video_params(img, name) for name, img in imgs]


def load_urls(urls: list[str]) -> list[tuple[float, float, int]]:
    if st.session_state.get('checked_urls'):
        return show_streams(st.session_state.checked_urls)
    else:
        with st.spinner("Проверка ссылок"):
            st.session_state.checked_urls = check_urls(urls)
        if not st.session_state.checked_urls:
            st.error("Не удалось открыть ни одну ссылку")
        else:
            return show_streams(st.session_state.checked_urls)
    return []


def send_to_rec(urls: list[str], params: list[tuple[float, float, int]]):
    send_urls_to_queue(urls, params)
    st.session_state['accepted'] = True


def main():
    if st.session_state.get('accepted'):
        st.success("Трансляции добавлены на распознавание, их можно посмотреть во вкладе 'История'")
        def rep():
            st.session_state.__setitem__('accepted', None)
            st.session_state.urls = None
            st.session_state.checked_urls = None
        st.button("Повторить", on_click=rep, key="rep_btn")
    else:
        st.title("RTMP-адрес для получения видеотрансляции")
        st.write("Введите список адресов или загрузите файл")
        res = sac.tabs([
            sac.TabsItem(label='Файл'),
            sac.TabsItem(label='Текст'),
        ], format_func='title', on_change=lambda: st.session_state.__setitem__('checked_urls', None),
            key="rtmp_urls", align='center')
        if res == "Файл":
            st.session_state.urls = list(set(get_urls_from_file()))
        else:
            st.session_state.urls = list(set(get_urls_from_text()))
        cols = st.columns(2)
        loaded = cols[0].button("Загрузить", use_container_width=True)
        urls_params = []
        if not st.session_state.get('urls'):
            if loaded and not st.session_state.urls:
                st.error("Список ссылок пуст")
                return
            elif loaded and st.session_state.urls:
                urls_params = load_urls(st.session_state.urls)
        else:
            urls_params = load_urls(st.session_state.urls)
        if urls_params:
            cols[1].button("Отправить на распознавание",
                           on_click=lambda: send_to_rec(st.session_state.urls, urls_params),
                           use_container_width=True)
