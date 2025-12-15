import streamlit as st
import pandas as pd
import os
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
st.markdown("<h1 align='center'>Dimensionamento do Impacto</h1>", unsafe_allow_html=True)
st.markdown("---")

# ========================
# Load Data
# ========================
journey_path = "jornadas_salvas/jornada_planejada_salva.csv"
impactos_path = "utils/conceitos_e_escalas_impactos.csv"

if not os.path.exists(journey_path):
    st.error("⚠️ Nenhuma jornada encontrada.")
    st.stop()

if not os.path.exists(impactos_path):
    st.error("⚠️ Arquivo de conceitos de impactos não encontrado.")
    st.stop()

df_jornada = pd.read_csv(journey_path)
df_impactos = pd.read_csv(impactos_path)
df_impactos.columns = df_impactos.columns.str.strip()

st.success("✅ Jornada carregada com sucesso!")
st.dataframe(df_jornada, use_container_width=True)

st.markdown("---")
st.markdown("### 🔹 Avaliação dos Impactos")
st.caption("1 = sem prejuízo | 5 = com prejuízos")

responses = []

# ========================
# Loop principal
# ========================
for idx, row in df_jornada.iterrows():
    comportamento = str(row["Comportamento"]).strip()
    categoria = str(row["Categoria"]).strip()
    tipo = str(row["Tipo"]).strip()

    with st.expander(f"Comportamento {idx + 1}: {comportamento}"):
        st.caption(f"**Categoria:** {categoria} | **Tipo:** {tipo}")

        for _, criterio in df_impactos.iterrows():
            nome = criterio["Critério-I"]
            pergunta = criterio["Pergunta"]
            nivel1 = criterio["1 - Sem prejuízo"]
            nivel5 = criterio["5 - Com prejuízos"]

            st.markdown(f"### 🔹 {nome}")
            st.markdown(f"**🗨️ Pergunta:** {pergunta}")

            col1, col2, col3 = st.columns([3, 4, 3])

            with col1:
                st.markdown(
                    f"<div style='font-size:0.88rem; line-height:1.2;'>1️⃣ {nivel1}</div>",
                    unsafe_allow_html=True
                )

            with col2:
                resposta = st.radio(
                    label="",
                    options=[1, 2, 3, 4, 5, "Não se aplica"],
                    index=None,
                    horizontal=True,
                    key=f"{idx}_{nome}_radio"
                )

                resposta_valor = None if resposta == "Não se aplica" else resposta

            with col3:
                st.markdown(
                    f"<div style='font-size:0.88rem; line-height:1.2; text-align:right;'>5️⃣ {nivel5}</div>",
                    unsafe_allow_html=True
                )

            observacao = st.text_area(
                "📝 Observação (opcional)",
                placeholder="Ex: impacto pontual, exceção, contexto específico…",
                key=f"{idx}_{nome}_obs"
            )

            responses.append({
                "Comportamento": comportamento,
                "Categoria": categoria,
                "Tipo": tipo,
                "Critério": nome,
                "Pergunta": pergunta,
                "Resposta": resposta_valor,
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
    os.makedirs("impactos_salvos", exist_ok=True)
    filename = "impactos_salvos/impacto_respostas_salvo.csv"

    df_respostas.to_csv(filename, index=False, encoding="utf-8-sig")

    st.success("✅ Respostas salvas com sucesso!")
    st.dataframe(df_respostas, use_container_width=True)
