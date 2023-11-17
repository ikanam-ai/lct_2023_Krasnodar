import streamlit as st
from pymongo.collection import Collection


def main():
    st.title("Настройка модели для распознавания")
    st.write(("Дообучить модель можно в разделе 'Обучение' после чего она появится тут и ее можно"
             " установить как модель по умолчанию для дальнейших распознаваний."))
    col: Collection = st.session_state.mongo_db.models_collection
    all_ = list(col.find({}))
    current = [i for i in all_ if i['selected']][0]
    index = all_.index(current)
    new_ = st.selectbox("Модель", [i['name'] for i in all_], index=index, key="select_model")
    st.text(f"В этой модели используется {len(current['frames'])} дополнительных изображений")
    if new_ != current['name']:
        col.update_one({"_id": current['_id']}, {"$set": {"selected": False}})
        col.update_one({"name": new_}, {"$set": {"selected": True}})
        st.toast(f"Модель '{new_}' установлена по умолчанию")
