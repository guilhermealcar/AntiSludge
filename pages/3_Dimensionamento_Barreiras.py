import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.auth import check_login

# ========== Authentication ==========
check_login()

st.set_page_config(layout="centered")

# ========== Header ==========
st.image("cinco_logo.png")
st.markdown("<h1 align='center'> Dimensionamento de Barreiras </h1>", unsafe_allow_html=True)
st.markdown("---")

# ========== Load Data ==========
journey_path = "jornadas_salvas/jornada_planejada_salva.csv"
conceitos_path = "utils/conceitos_e_escalas_barreiras.csv"

if not os.path.exists(journey_path):
    st.error("⚠️ Nenhuma jornada foi encontrada. Volte à página **Mapeamento Comportamental** e salve sua jornada primeiro.")
    st.stop()

if not os.path.exists(conceitos_path):
    st.error("⚠️ O arquivo `conceitos_e_escalas_barreiras.csv` não foi encontrado em `utils/`.")
    st.stop()

df_jornada = pd.read_csv(journey_path)
df_conceitos = pd.read_csv(conceitos_path)
df_conceitos.columns = df_conceitos.columns.str.strip()

st.success("✅ Jornada carregada com sucesso!")
st.dataframe(df_jornada, use_container_width=True)

st.markdown("---")
st.markdown("### 🔹 Avaliação das Barreiras")
st.caption("Para cada comportamento da jornada, clique para expandir e responder as perguntas (1 = sem barreiras, 5 = barreiras impeditivas).")

responses = []

# ==========================================================
# BLOCO NOVO — estilo idêntico ao de Impactos
# ==========================================================
def bloco_barreira(pergunta, desc1, desc5, key):
    st.markdown(f"### 🗨️ {pergunta}")

    # colunas: esquerda / centro maior / direita
    col1, col2, col3 = st.columns([3, 4, 3])

    with col1:
        st.markdown(
            f"""
            <div style='font-size: 0.88rem; line-height:1.2;'>
            <strong>1️⃣</strong> {desc1}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        resposta = st.radio(
            label="",
            options=[1, 2, 3, 4, 5],
            horizontal=True,
            key=key
        )

    with col3:
        st.markdown(
            f"""
            <div style='font-size: 0.88rem; text-align:right; line-height:1.2;'>
            <strong>5️⃣</strong> {desc5}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    return resposta

# ========== Loop sobre Jornada ==========
for idx, row in df_jornada.iterrows():
    categoria = str(row["Categoria"]).strip()
    tipo = str(row["Tipo"]).strip()
    comportamento = str(row["Comportamento"]).strip()

    with st.expander(f"Comportamento {idx + 1}: {comportamento}"):
        st.caption(f"**Categoria:** {categoria} | **Tipo:** {tipo}")

        # filtra perguntas
        perguntas = df_conceitos[
            (df_conceitos["Categoria"].str.strip() == categoria)
            & (df_conceitos["Tipo"].str.strip() == tipo)
        ]

        if perguntas.empty:
            st.warning("Nenhuma pergunta correspondente encontrada para este comportamento.")
            continue

        # cada pergunta
        for _, q in perguntas.iterrows():

            resposta = bloco_barreira(
                pergunta=q["Pergunta"],
                desc1=q["1 - Sem barreiras"],
                desc5=q["5 - Com barreiras impeditivas"],
                key=f"{idx}_{q['Ref #']}"
            )

            responses.append({
                "Comportamento": comportamento,
                "Categoria": categoria,
                "Tipo": tipo,
                "Critério-B": q["Critério-B"],
                "Pergunta": q["Pergunta"],
                "Resposta": resposta,
                "Sem Barreiras": q["1 - Sem barreiras"],
                "Com Barreiras Impeditivas": q["5 - Com barreiras impeditivas"]
            })

st.markdown("---")

# ========== Save Responses ==========
if st.button("💾 Salvar Respostas"):
    if not responses:
        st.warning("⚠️ Nenhuma resposta foi registrada.")
        st.stop()

    df_respostas = pd.DataFrame(responses)
    os.makedirs("barreiras_salvas", exist_ok=True)
    filename = "barreiras_salvas/barreiras_resposta_salva.csv"

    df_respostas.to_csv(filename, index=False, encoding="utf-8-sig")

    st.success(f"✅ Respostas salvas com sucesso em `{filename}`!")
    st.dataframe(df_respostas, use_container_width=True)

    st.download_button(
        label="⬇️ Baixar Respostas (CSV)",
        data=df_respostas.to_csv(index=False).encode("utf-8"),
        file_name=os.path.basename(filename),
        mime="text/csv",
    )
