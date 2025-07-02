import streamlit as st
import pandas as pd
from streamlit_app import get_data, save_data, reset_data

st.markdown("# Perfil 🎉")
st.sidebar.markdown("# Perfil 🎉")

data = get_data()

# ========== Interface ==========
st.metric("Problemas Resolvidos", data["resolvidos"])
st.metric("Pontos Obtidos", data["pontos"])



# ========== Gráfico Simples ==========
st.subheader("Distribuição por Dificuldade")

df = pd.DataFrame(
    {
        "Resolvidos": data["por_dificuldade"].values()
    },
    index=data["por_dificuldade"].keys()
)

st.bar_chart(df)

# ========== Ações ==========
st.divider()
if st.button("Resetar Progresso", key="reset_progress_button"):
    reset_data()
    st.success("Progresso resetado!")
    st.rerun()
