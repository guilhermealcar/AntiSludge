import streamlit as st
from utils.auth import check_login

# Verifica se o usuário está logado
check_login()

st.title("📑 Dimensionamento de Barreiras")
st.write("Aqui você pode dimensionar as barreiras observadas.")
