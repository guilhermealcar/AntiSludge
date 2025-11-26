import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.auth import check_login

# ========================
# Login
# ========================
check_login()

st.set_page_config(layout="centered")

# ========================
# Header
# ========================
st.image("cinco_logo.png")
st.markdown("<h1 align='center'> Dimensionamento do Impacto </h1>", unsafe_allow_html=True)
st.markdown("---")

# ========================
# Load Data
# ========================
journey_path = "jornadas_salvas/jornada_planejada_salva.csv"
impactos_path = "utils/conceitos_e_escalas_impactos.csv"

if not os.path.exists(journey_path):
    st.error("⚠️ Nenhuma jornada encontrada. Volte à página **Mapeamento Comportamental** e salve a jornada primeiro.")
    st.stop()

if not os.path.exists(impactos_path):
    st.error("⚠️ O arquivo `conceitos_e_escalas_impactos.csv` não foi encontrado em `utils/`.")
    st.stop()

df_jornada = pd.read_csv(journey_path)
df_impactos = pd.read_csv(impactos_path)
df_impactos.columns = df_impactos.columns.str.strip()

st.success("✅ Jornada carregada com sucesso!")
st.dataframe(df_jornada, use_container_width=True)

st.markdown("---")
st.markdown("### 🔹 Avaliação dos Impactos")
st.caption("Para cada comportamento mapeado, clique para expandir e avaliar o impacto conforme os critérios abaixo (1 = sem prejuízo, 5 = com prejuízos).")

# ========================
# Avaliação
# ========================
responses = []

for idx, row in df_jornada.iterrows():
    comportamento = str(row["Comportamento"]).strip()
    categoria = str(row["Categoria"]).strip()
    tipo = str(row["Tipo"]).strip()

    with st.expander(f"Comportamento {idx + 1}: {comportamento}"):
        st.caption(f"**Categoria:** {categoria} | **Tipo:** {tipo}")

        for _, criterio in df_impactos.iterrows():
            nome_criterio = criterio["Critério-I"]
            conceito = criterio["Critério-I-Conceito"]
            exemplo = criterio["Exemplo-I"]
            descricao = criterio["Descrição-I"]
            pergunta = criterio["Pergunta"]
            nivel1 = criterio["1 - Sem prejuízo"]
            nivel5 = criterio["5 - Com prejuízos"]

            st.markdown(f"### 🔹 {nome_criterio}")
            with st.expander("📘 Detalhes do critério"):
                st.write(f"**Conceito:** {conceito}")
                st.write(f"**Exemplo:** {exemplo}")
                st.write(f"**Descrição:** {descricao}")

            # ========================
            # NOVO FORMATO DE PERGUNTA (igual ao de Barreiras)
            # ========================
            st.markdown(f"**🗨️ Pergunta:** {pergunta}")

            # deixe a coluna do meio maior para evitar quebra dos botões
            col1, col2, col3 = st.columns([3, 4, 3])

            with col1:
                # resumo do nível 1 (texto à esquerda)
                st.markdown(f"<div style='font-size:0.88rem; line-height:1.1;'>{'1️⃣ '}{nivel1}</div>", unsafe_allow_html=True)

            with col2:
                # rótulo compacto para o radio (evita texto longo que força quebra)
                resposta = st.radio(
                    label="",
                    options=[1, 2, 3, 4, 5],
                    horizontal=True,
                    key=f"{idx}_{nome_criterio}"
                )

            with col3:
                # resumo do nível 5 (texto à direita)
                st.markdown(f"<div style='font-size:0.88rem; line-height:1.1; text-align:right;'>{'5️⃣ '}{nivel5}</div>", unsafe_allow_html=True)

            responses.append({
                "Comportamento": comportamento,
                "Categoria": categoria,
                "Tipo": tipo,
                "Critério": nome_criterio,
                "Pergunta": pergunta,
                "Resposta": resposta,
                "1 - Sem prejuízo": nivel1,
                "5 - Com prejuízos": nivel5
            })

st.markdown("---")

# ========================
# Save Responses
# ========================
if st.button("💾 Salvar Respostas"):
    if not responses:
        st.warning("⚠️ Nenhuma resposta foi registrada.")
        st.stop()

    df_respostas = pd.DataFrame(responses)
    os.makedirs("impactos_salvos", exist_ok=True)

    filename = "impactos_salvos/impacto_respostas_salvo.csv"
    df_respostas.to_csv(filename, index=False, encoding="utf-8-sig")

    st.success(f"✅ Respostas salvas com sucesso em `{filename}`!")
    st.dataframe(df_respostas, use_container_width=True)

    st.download_button(
        label="⬇️ Baixar Respostas (CSV)",
        data=df_respostas.to_csv(index=False).encode("utf-8"),
        file_name=os.path.basename(filename),
        mime="text/csv",
    )
