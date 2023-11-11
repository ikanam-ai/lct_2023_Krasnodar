import streamlit as st
from config import Config


def main() -> None:
    config = Config()
    st.title("Использование api уведомлений")
    st.text("Для получения уведовлений достаточно открыть соединение по websockets, пример кода ниже.")
    if config.NOTIF_URL and config.NOTIF_PSWD:
        st.text("Данные для подключения:")
        st.text(f"Url: {config.NOTIF_URL}")
        st.text(f"Пароль: {config.NOTIF_PSWD}")
    with open("lct/docs/api_example.py", "r", encoding="utf-8") as f:
        code = f.read()
    st.code(code, language="python", line_numbers=True)
