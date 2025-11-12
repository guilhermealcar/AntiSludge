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
st.markdown("<h2 align='center'>🎯 Dimensionamento do Impacto</h2>", unsafe_allow_html=True)
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
st.markdown("### ⚖️ Avaliação dos Impactos")
st.caption("Para cada comportamento mapeado, avalie o impacto conforme os critérios abaixo (1 = sem prejuízo, 5 = com prejuízos).")

# ========================
# Avaliação
# ========================
responses = []

for idx, row in df_jornada.iterrows():
    comportamento = str(row["Comportamento"]).strip()
    categoria = str(row["Categoria"]).strip()
    tipo = str(row["Tipo"]).strip()

    st.markdown(f"## 🧩 Comportamento {idx + 1}: {comportamento}")
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

        st.markdown(f"**🗨️ Pergunta:** {pergunta}")
        st.caption(f"💡 1️⃣ {nivel1}\n\n5️⃣ {nivel5}")

        resposta = st.radio(
            f"Selecione o nível de impacto ({nome_criterio})",
            options=[1, 2, 3, 4, 5],
            horizontal=True,
            key=f"{idx}_{nome_criterio}"
        )

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
if st.button("💾 Salvar Respostas de Impacto"):
    if not responses:
        st.warning("⚠️ Nenhuma resposta foi registrada.")
        st.stop()

    df_respostas = pd.DataFrame(responses)
    os.makedirs("impactos_salvos", exist_ok=True)

    filename = f"impactos_salvos/impactos_respostas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_respostas.to_csv(filename, index=False, encoding="utf-8-sig")

    st.success(f"✅ Respostas salvas com sucesso em `{filename}`!")
    st.dataframe(df_respostas, use_container_width=True)

    st.download_button(
        label="⬇️ Baixar Respostas (CSV)",
        data=df_respostas.to_csv(index=False).encode("utf-8"),
        file_name=os.path.basename(filename),
        mime="text/csv",
    )
