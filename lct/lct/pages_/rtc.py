import cv2
import streamlit as st
import streamlit_antd_components as sac
from streamlit.runtime.uploaded_file_manager import UploadedFile
from send import send_urls_to_queue


def get_urls_from_file() -> list[str] | None:
    uploaded_file: UploadedFile | None = st.file_uploader("Загрузите zip архив с видео", type=["txt", "csv"])

    return uploaded_file.readlines() if uploaded_file else None


def get_urls_from_text() -> list[str] | None:
    rtmp_urls = st.text_area("RTMP-адреса")

    return rtmp_urls.split("\n") if rtmp_urls else None


def check_urls(urls: list[str]) -> list[str]:
    res = []
    for url in urls:
        try:
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                res.append(url)
        except:
            pass
        finally:
            cap.release()
    return res


def add_url(url: list[str]) -> None:
    ...


def main():
    st.title("RTMP-адрес для получения видеотрансляции")
    st.write("Введите список адресов или загрузите файл")
    res = sac.tabs([
        sac.TabsItem(label='Файл'),
        sac.TabsItem(label='Текст'),
    ], format_func='title')
    urls = None
    if res == "Файл":
        urls = get_urls_from_file()
    else:
        urls = get_urls_from_text()
    if not urls:
        return
    with st.spinner("Проверка ссылок"):
        checked_urls = check_urls(urls)
    if not checked_urls:
        st.error("Не удалось открыть ни одну ссылку")
    else:
        add_url(checked_urls)
        st.success("Следующие трансляции добавлены в очередь")
        for url in urls:
            st.text(url)
