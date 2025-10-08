import streamlit as st

def check_login():
    """Impede o acesso se o usuário não estiver logado."""
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Você precisa fazer login para acessar esta página.")
        st.stop()
