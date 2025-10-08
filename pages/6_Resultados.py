import streamlit as st
from utils.auth import check_login

# Verifica se o usuário está logado
check_login()

st.image("cinco_logo.png")