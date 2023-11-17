import streamlit as st

from numpy import ndarray


def archive_video_params(img: ndarray, name: str) -> tuple[float, float, int]:
    key = f"archive_video_params_{name}"
    storage = st.session_state.setdefault(key, {})
    w, h, *_ = img.shape
    with st.container():
        cols = st.columns(2)
        cols[0].image(img)
        cols[1].text(name)
        storage['threshold'] = cols[1].slider("Threshold", 0.0, 1.0, 1, 0.05, key=f"{name}_Threshold")
        storage['n_frames'] = cols[1].slider("Распознавать каждый n кадр", 1, 100, 10, 1, key=f"{name}_n_frames")
        res_cols = cols[1].columns(2)
        default_res = (0.1, 0.25, 0.5, 0.75, 1)
        b_cols = st.columns(len(default_res))
        ratio = storage.setdefault('ratio', 1)
        res_cols[0].number_input("Ширина", value=int(w * ratio), disabled=True, key=f"{name}_ш")
        res_cols[1].number_input("Высота", value=int(h * ratio), disabled=True, key=f"{name}_в")
        for i, e in enumerate(default_res):
            btn = b_cols[i].button(f"{e}x", use_container_width=True, key=f"{name}_{e}_btn",
                                   on_click=lambda e=e: storage.__setitem__('ratio',e ))
        st.divider()

        return storage['threshold'], storage['ratio'], storage['n_frames']
