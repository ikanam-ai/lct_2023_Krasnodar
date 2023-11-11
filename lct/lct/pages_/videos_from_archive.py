import os
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from components.archive_video_params import archive_video_params
from utils.from_archive import extract_videos, create_thumbnail
from send import send_videos_to_queue


def main():
    user = st.session_state['username']
    st.title("Распознование из архива")
    uploaded_file: UploadedFile | None = st.file_uploader("Загрузите zip архив с видео", type=["zip"])
    submit_btn = st.columns(3)

    if uploaded_file is None:
        return

    with st.spinner("Идет загрузка и обработка архива..."):
        temp_folder = f"temp_videos/{user}"
        extract_videos(uploaded_file, temp_folder)
        st.subheader("Настройка распознавания")
        video_files = os.listdir(temp_folder)
        files_params = []
        for i, video_file in enumerate(video_files):
            video_path = os.path.join(temp_folder, video_file)
            thumbnail = create_thumbnail(video_path)

            if thumbnail is None:
                return
            files_params.append(archive_video_params(thumbnail, video_file))
        send = submit_btn[1].button("Начать распознавание", use_container_width=True)
        if send:
            send_videos_to_queue(temp_folder, files_params)
            st.toast("Отправлено на распознавание, готовность можно увидеть в разделе истории")