import streamlit as st

st.set_page_config(page_title="Mapeamento Anti-Sludge", page_icon="🧠")   # Adicionar ícone aqui

# --- Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Página de Login ---
if not st.session_state.logged_in:
    st.image("cinco_logo.png")

    st.markdown("<h2 align='center'> 🔐 Login </h2>", unsafe_allow_html=True)

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.success("✅ Login realizado com sucesso! Use o menu lateral.")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha inválidos.")

# --- Se já estiver logado ---
else:
    st.image("cinco_logo.png")

    st.sidebar.success("✅ Você está logado! Use o menu lateral para navegar.")
    st.write("👈 Selecione uma página no menu lateral.")
