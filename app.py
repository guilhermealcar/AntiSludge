import streamlit as st

st.set_page_config(page_title="Mapeamento Anti-Sludge", page_icon="")   # Adicionar ícone aqui

# --- Login ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "admin" and password == "123":
            st.session_state["logged_in"] = True
            st.success("✅ Login realizado com sucesso! Use o menu lateral.")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha inválidos.")

else:
    st.sidebar.success("✅ Você está logado! Use o menu lateral para navegar.")
    st.write("👈 Selecione uma página no menu lateral.")
