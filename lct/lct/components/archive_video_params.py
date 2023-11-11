import streamlit as st

from numpy import ndarray


def archive_video_params(img: ndarray, name: str) -> tuple[float, float, int]:
    w, h, *_ = img.shape
    with st.container():
        cols = st.columns(2)
        cols[0].image(img)
        cols[1].subheader(name)
        threshold = cols[1].slider("Threshold", 0.0, 1.0, 0.5, 0.05, key=f"{name}_Threshold")
        n_frames = cols[1].slider("Распознавать каждый n кадр", 1, 100, 10, 1, key=f"{name}_n_frames")
        res_cols = cols[1].columns(2)
        default_res = (0.1, 0.25, 0.5, 0.75, 1)
        b_cols = st.columns(len(default_res))
        width, height, ratio = w, h, 1
        for i, e in enumerate(default_res):
            btn = b_cols[i].button(f"{e}x", use_container_width=True, key=f"{name}_{e}_btn")
            if btn:
                ratio = e
        res_cols[0].number_input("Ширина", value=int(w * ratio), disabled=True, key=f"{name}_ш")
        res_cols[1].number_input("Высота", value=int(h * ratio), disabled=True, key=f"{name}_в")
        st.divider()

        return threshold, ratio, n_frames
