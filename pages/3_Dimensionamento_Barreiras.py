import streamlit as st
from utils.auth import check_login

# Verifica se o usuário está logado
check_login()

st.image("cinco_logo.png")
st.markdown("<h2 align='center'> 📑 Dimensionamento de Barreiras </h2>", unsafe_allow_html=True)
st.write("Aqui você pode dimensionar as barreiras observadas.")
