import random

import streamlit as st
from utils import cookie_manager
import json
import datetime

@st.fragment
def get_data():
    data = cookie_manager.get('progresso')
    if data:
        loaded_data = json.loads(data)
    else:
        loaded_data = {}

    loaded_data.setdefault("pontos", 0)
    loaded_data.setdefault("resolvidos", 0)
    loaded_data.setdefault("por_dificuldade", {
        "Fácil": 0,
        "Intermediário": 0,
        "Difícil": 0
    })
    return loaded_data

@st.fragment
def save_data(data: dict):
    cookie_manager.set(
        "progresso",
        json.dumps(data),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=30)
    )

@st.fragment
def reset_data():
    if cookie_manager.get("progresso"):
        cookie_manager.delete("progresso")





user_data = get_data()

if not user_data:
    user_data = {}

user_data.setdefault("pontos", 0)
user_data.setdefault("resolvidos", 0)
user_data.setdefault("por_dificuldade", {
    "Fácil": 0,
    "Intermediário": 0,
    "Difícil": 0
})



# Define the pages
main_page = st.Page("pages/main_page.py", title="Início", icon="🎈")
page_2 = st.Page("pages/problems.py", title="Problemas", icon="❄️")
page_3 = st.Page("pages/profile.py", title="Perfil", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()
