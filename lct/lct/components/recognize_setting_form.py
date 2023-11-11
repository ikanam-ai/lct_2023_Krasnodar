import streamlit as st


def recognize_settings_form() -> None | bool:
    with st.form("Настройки распознавания"):
        cols = st.columns(2)
        threshold = cols[0].slider("Threshold", 0.0, 1.0, 0.5, 0.05)
        n = cols[1].slider("Распозавать каждый n-ый кадр", 0, 100, 10, 1)

        cols = st.columns(3)

        submitted = cols[1].form_submit_button("Применить", use_container_width=True)

        return submitted
