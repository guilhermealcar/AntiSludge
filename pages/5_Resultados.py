import streamlit as st
from utils.auth import check_login
import pandas as pd
import plotly.express as px

# ========================
# Login
# ========================
check_login()
st.set_page_config(layout="centered")

# ========================
# Header
# ========================
st.image("cinco_logo.png")
st.markdown("<h1 style='text-align:center;'>Resultados Gerais</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ========================
# Carregar arquivos
# ========================
try:
    df_jornada = pd.read_csv("jornadas_salvas/jornada_planejada_salva.csv")
    df_barreiras = pd.read_csv("barreiras_salvas/barreiras_resposta_salva.csv")
    df_impacto = pd.read_csv("impactos_salvos/impacto_respostas_salvo.csv")
except FileNotFoundError:
    st.error("⚠️ Arquivos não encontrados. Envie os CSVs na página inicial.")
    st.stop()

# ========================
# Paleta de cores
# ========================
CORES = ["#006D77", "#83C5BE", "#FFDDD2", "#E29578", "#6D597A"]

# =====================================================
# 🔹 DADOS COMBINADOS (BARREIRAS + IMPACTOS)
# =====================================================
barreiras_crit = (
    df_barreiras
    .dropna(subset=["Resposta"])
    .groupby("Critério")["Resposta"]
    .mean()
    .reset_index()
)
barreiras_crit["Tipo Avaliação"] = "Barreiras"

impactos_crit = (
    df_impacto
    .dropna(subset=["Resposta"])
    .groupby("Critério")["Resposta"]
    .mean()
    .reset_index()
)
impactos_crit["Tipo Avaliação"] = "Impactos"

df_comparativo = pd.concat([barreiras_crit, impactos_crit], ignore_index=True)

# =====================================================
# 🔹 VISÃO GERAL
# =====================================================
st.subheader("🔹 Visão Geral dos Dados")

col1, col2, col3, col4 = st.columns(4)

total_comportamentos = df_jornada["Comportamento"].nunique()
total_barreiras = df_barreiras["Resposta"].notna().sum()
total_impactos = df_impacto["Resposta"].notna().sum()

criterios_barreiras = df_barreiras["Critério"].dropna().unique()
criterios_impactos = df_impacto["Critério"].dropna().unique()
total_criterios = len(set(criterios_barreiras).union(set(criterios_impactos)))

col1.metric("Total de Comportamentos", total_comportamentos)
col2.metric("Barreiras Respondidas", total_barreiras)
col3.metric("Impactos Respondidos", total_impactos)
col4.metric("Total de Critérios", total_criterios)

st.markdown("---")

# =====================================================
# 🔹 ANÁLISE DE BARREIRAS
# =====================================================
st.header("🔹 Análise de Barreiras")

st.subheader("🔸 Barreiras por Critério")

barreiras_media_criterio = (
    df_barreiras
    .dropna(subset=["Resposta"])
    .groupby("Critério")["Resposta"]
    .mean()
    .reset_index()
    .sort_values("Resposta", ascending=False)
)

fig_bar_crit_bar = px.bar(
    barreiras_media_criterio,
    x="Critério",
    y="Resposta",
    color="Critério",
    color_discrete_sequence=CORES,
    title="Média das Barreiras por Critério",
    text="Resposta"
)

fig_bar_crit_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_bar_crit_bar.update_layout(yaxis=dict(range=[0, 5]))

st.plotly_chart(fig_bar_crit_bar, use_container_width=True)

# ========================
# MÉDIA POR CATEGORIA
# ========================
barreiras_media_cat = (
    df_barreiras
    .dropna(subset=["Resposta"])
    .groupby("Categoria")["Resposta"]
    .mean()
    .reset_index()
)

fig_bar_cat = px.bar(
    barreiras_media_cat,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Média das Barreiras por Categoria",
    text="Resposta"
)

fig_bar_cat.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_bar_cat.update_layout(yaxis=dict(range=[0, 5]))
st.plotly_chart(fig_bar_cat, use_container_width=True)

# =====================================================
# 🔹 ANÁLISE DE IMPACTOS
# =====================================================
st.header("🔹 Análise de Impactos")

st.subheader("🔸 Impactos por Critério")

impacto_media_criterio = (
    df_impacto
    .dropna(subset=["Resposta"])
    .groupby("Critério")["Resposta"]
    .mean()
    .reset_index()
    .sort_values("Resposta", ascending=False)
)

fig_bar_crit_imp = px.bar(
    impacto_media_criterio,
    x="Critério",
    y="Resposta",
    color="Critério",
    color_discrete_sequence=CORES,
    title="Média dos Impactos por Critério",
    text="Resposta"
)

fig_bar_crit_imp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_bar_crit_imp.update_layout(yaxis=dict(range=[0, 5]))
st.plotly_chart(fig_bar_crit_imp, use_container_width=True)

# =====================================================
# 🔹 COMPARAÇÃO BARREIRAS x IMPACTOS
# =====================================================
st.header("🔹 Comparação entre Barreiras e Impactos")

fig_comp = px.bar(
    df_comparativo,
    x="Critério",
    y="Resposta",
    color="Tipo Avaliação",
    barmode="group",
    color_discrete_sequence=["#006D77", "#E29578"],
    title="Comparação Média: Barreiras vs Impactos por Critério",
    text="Resposta"
)

fig_comp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_comp.update_layout(yaxis=dict(range=[0, 5]))

st.plotly_chart(fig_comp, use_container_width=True)

# =====================================================
# 🔹 INSIGHTS AUTOMÁTICOS
# =====================================================
st.header("🔹 Resumo Automático")

media_barreiras = df_barreiras["Resposta"].mean()
media_impactos = df_impacto["Resposta"].mean()

st.success(f"""
• **Média geral das barreiras:** `{media_barreiras:.2f}`  
• **Média geral dos impactos:** `{media_impactos:.2f}`  

**Interpretação:**
- Barreiras: nível **{"alto" if media_barreiras <= 2 else "moderado" if media_barreiras <= 3.5 else "baixo"}**
- Impactos: impacto **{"crítico" if media_impactos >= 4 else "moderado" if media_impactos >= 2.5 else "baixo"}**

📎 *Use esses dados para priorizar ações de melhoria no fluxo do usuário.*
""")
