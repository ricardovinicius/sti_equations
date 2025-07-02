import streamlit as st
import extra_streamlit_components as stx

def get_manager():
    if 'cookie_manager' not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
    return st.session_state.cookie_manager

cookie_manager = get_manager()
cookies = cookie_manager.get_all()