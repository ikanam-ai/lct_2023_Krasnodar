import streamlit as st
import streamlit_authenticator as stauth
from services.mongo import Mongo
from config import Config
from main import main as main_

config = Config()


@st.cache_resource
def init_connection():
    return Mongo(config)


st.session_state.mongo_db = init_connection()

authenticator = stauth.Authenticate(
    {
        'usernames': {
            config.USER_LOGIN: {
                'email': 'jsmith@gmail.com',
                'name': 'John Smith',
                'password': stauth.Hasher([config.USER_PASSWORD]).generate()[0]
            }
        }
    },
    'some_cookie_name',
    'some_signature_key',
    30,
    []
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    main_()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
