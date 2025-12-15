import streamlit as st
import pandas as pd
import os
from utils.auth import check_login

# ========================
# Authentication
# ========================
check_login()
st.set_page_config(layout="centered")

# ========================
# Header
# ========================
st.image("cinco_logo.png")
st.markdown("<h1 align='center'>Dimensionamento de Barreiras</h1>", unsafe_allow_html=True)
st.markdown("---")

# ========================
# Load Data
# ========================
journey_path = "jornadas_salvas/jornada_planejada_salva.csv"
conceitos_path = "utils/conceitos_e_escalas_barreiras.csv"

if not os.path.exists(journey_path):
    st.error("⚠️ Nenhuma jornada encontrada. Salve a jornada primeiro.")
    st.stop()

if not os.path.exists(conceitos_path):
    st.error("⚠️ Arquivo de conceitos de barreiras não encontrado.")
    st.stop()

df_jornada = pd.read_csv(journey_path)
df_conceitos = pd.read_csv(conceitos_path)
df_conceitos.columns = df_conceitos.columns.str.strip()

st.success("✅ Jornada carregada com sucesso!")
st.dataframe(df_jornada, use_container_width=True)

st.markdown("---")
st.markdown("### 🔹 Avaliação das Barreiras")
st.caption("1 = sem barreiras | 5 = barreiras impeditivas")

responses = []

# ========================
# Função de Bloco
# ========================
def bloco_barreira(pergunta, desc1, desc5, key):
    st.markdown(f"### 🗨️ {pergunta}")

    col1, col2, col3 = st.columns([3, 4, 3])

    with col1:
        st.markdown(
            f"<div style='font-size:0.88rem; line-height:1.2;'><strong>1️⃣</strong> {desc1}</div>",
            unsafe_allow_html=True
        )

    with col2:
        resposta = st.radio(
            label="",
            options=[1, 2, 3, 4, 5, "Não se aplica"],
            index=None,
            horizontal=True,
            key=f"{key}_radio"
        )

        resposta_valor = None if resposta == "Não se aplica" else resposta

    with col3:
        st.markdown(
            f"<div style='font-size:0.88rem; line-height:1.2; text-align:right;'><strong>5️⃣</strong> {desc5}</div>",
            unsafe_allow_html=True
        )

    observacao = st.text_area(
        "📝 Observação (opcional)",
        placeholder="Ex: exceção, fator externo, contexto específico…",
        key=f"{key}_obs"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    return resposta_valor, observacao

# ========================
# Loop principal
# ========================
for idx, row in df_jornada.iterrows():
    comportamento = str(row["Comportamento"]).strip()
    categoria = str(row["Categoria"]).strip()
    tipo = str(row["Tipo"]).strip()

    with st.expander(f"Comportamento {idx + 1}: {comportamento}"):
        st.caption(f"**Categoria:** {categoria} | **Tipo:** {tipo}")

        perguntas = df_conceitos[
            (df_conceitos["Categoria"].str.strip() == categoria) &
            (df_conceitos["Tipo"].str.strip() == tipo)
        ]

        if perguntas.empty:
            st.warning("Nenhuma pergunta encontrada para este comportamento.")
            continue

        for _, q in perguntas.iterrows():
            resposta, observacao = bloco_barreira(
                pergunta=q["Pergunta"],
                desc1=q["1 - Sem barreiras"],
                desc5=q["5 - Com barreiras impeditivas"],
                key=f"{idx}_{q['Ref #']}"
            )

            responses.append({
                "Comportamento": comportamento,
                "Categoria": categoria,
                "Tipo": tipo,
                "Critério": q["Critério-B"],
                "Pergunta": q["Pergunta"],
                "Resposta": resposta,
                "Observação": observacao
            })

st.markdown("---")

# ========================
# Save
# ========================
if st.button("💾 Salvar Respostas"):
    if not responses:
        st.warning("⚠️ Nenhuma resposta registrada.")
        st.stop()

    df_respostas = pd.DataFrame(responses)
    os.makedirs("barreiras_salvas", exist_ok=True)
    filename = "barreiras_salvas/barreiras_resposta_salva.csv"

    df_respostas.to_csv(filename, index=False, encoding="utf-8-sig")

    st.success("✅ Respostas salvas com sucesso!")
    st.dataframe(df_respostas, use_container_width=True)
