import fractions

import av
import cv2
import streamlit as st
from streamlit_webrtc import WebRtcMode, create_video_source_track, webrtc_streamer, VideoHTMLAttributes

from models.archive_from_history import ArchiveFromHistory


def video_source_callback(arc: ArchiveFromHistory) -> av.VideoFrame:
    cap = cv2.VideoCapture(arc.url)

    def inner(pts: int, time_base: fractions.Fraction):
        r, frame = cap.read()

        return av.VideoFrame.from_ndarray(frame, format="bgr24")

    return inner


def watch(arc: ArchiveFromHistory, back: callable):
    key = arc.title
    with st.container():
        video_source_track = create_video_source_track(
            video_source_callback(arc), key="video_source_track")
        st.button("Назад", on_click=lambda: back() or video_source_track.stop(), key=f"back_{key}")
        st.text(arc.title)

        def on_change():
            ctx = st.session_state["player"]
            stopped = not ctx.state.playing and not ctx.state.signalling
            if stopped:
                video_source_track.stop()

        webrtc_streamer(
            key="player",
            mode=WebRtcMode.RECVONLY,
            source_video_track=video_source_track,
            media_stream_constraints={"video": True, "audio": False},
            on_change=on_change,
            translations={
                "start": "Старт",
                "stop": "Стоп"
            }
        )
