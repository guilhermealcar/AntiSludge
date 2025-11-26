import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Mapeamento Anti-Sludge", layout="centered")

# --- Controle de Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Flag que diz se novos CSVs foram carregados e devem ser reconhecidos pelas outras páginas
if "csvs_atualizados" not in st.session_state:
    st.session_state.csvs_atualizados = False

# --- Página de Login ---
if not st.session_state.logged_in:
    st.image("cinco_logo.png")
    st.markdown("<h2 align='center'>🔐 Login</h2>", unsafe_allow_html=True)

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
    st.markdown("<h1 align='center'>Envio e Visualização de Arquivos</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.write("""
    Envie os arquivos CSV da **Jornada Planejada**, **Dimensionamento de Barreiras** e **Dimensionamento de Impacto**.
    Eles serão armazenados automaticamente nas pastas corretas, permitindo que as próximas páginas utilizem os dados.
    """)

    # ========================
    # Função auxiliar
    # ========================
    def salvar_csv(uploaded_file, pasta_destino, nome_arquivo):
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        with open(caminho_completo, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Arquivo `{nome_arquivo}` salvo em `{pasta_destino}/` com sucesso!")
        return caminho_completo

    # ========================
    # Upload dos arquivos
    # ========================
    uploaded_jornada = st.file_uploader("📂 Enviar Jornada Planejada (jornada_planejada_salva.csv)", type="csv")
    uploaded_barreiras = st.file_uploader("📂 Enviar Respostas de Barreiras (barreiras_resposta_salva.csv)", type="csv")
    uploaded_impactos = st.file_uploader("📂 Enviar Respostas de Impacto (impacto_respostas_salvo.csv)", type="csv")

    # ========================
    # Botão para salvar
    # ========================
    if st.button("💾 Salvar Arquivos Enviados"):
        if not uploaded_jornada and not uploaded_barreiras and not uploaded_impactos:
            st.warning("⚠️ Nenhum arquivo foi enviado.")
            st.stop()

        if uploaded_jornada:
            salvar_csv(uploaded_jornada, "jornadas_salvas", "jornada_planejada_salva.csv")

        if uploaded_barreiras:
            salvar_csv(uploaded_barreiras, "barreiras_salvas", "barreiras_resposta_salva.csv")

        if uploaded_impactos:
            salvar_csv(uploaded_impactos, "impactos_salvos", "impacto_respostas_salvo.csv")

        # Marca que novos arquivos foram carregados → páginas podem recarregar
        st.session_state.csvs_atualizados = True

        st.success("🎉 Todos os arquivos enviados foram salvos com sucesso!")

        st.rerun()

    # ========================
    # Exibir arquivos carregados
    # ========================
    st.markdown("---")
    st.markdown("### Visualizar conteúdo dos arquivos enviados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🔹 Jornada Planejada")
        caminho = "jornadas_salvas/jornada_planejada_salva.csv"
        if os.path.exists(caminho):
            st.dataframe(pd.read_csv(caminho), use_container_width=True)
        else:
            st.info("Nenhuma jornada carregada ainda.")

    with col2:
        st.caption("🔹 Barreiras Respondidas")
        caminho = "barreiras_salvas/barreiras_resposta_salva.csv"
        if os.path.exists(caminho):
            st.dataframe(pd.read_csv(caminho), use_container_width=True)
        else:
            st.info("Nenhum arquivo de barreiras carregado ainda.")

    with col3:
        st.caption("🔹 Impactos Respondidos")
        caminho = "impactos_salvos/impacto_respostas_salvo.csv"
        if os.path.exists(caminho):
            st.dataframe(pd.read_csv(caminho), use_container_width=True)
        else:
            st.info("Nenhum arquivo de impacto carregado ainda.")

    # ========================
    # Limpar arquivos
    # ========================
    st.markdown("---")
    if st.button("🗑️ Limpar Todos os Arquivos Salvos"):
        pastas = ["jornadas_salvas", "barreiras_salvas", "impactos_salvos"]
        for pasta in pastas:
            if os.path.exists(pasta):
                for arquivo in os.listdir(pasta):
                    os.remove(os.path.join(pasta, arquivo))

        # limpar estado
        st.session_state.csvs_atualizados = False

        st.warning("🗑️ Todos os arquivos foram removidos.")
        st.rerun()
