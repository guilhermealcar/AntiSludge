import streamlit as st
from utils.auth import check_login
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# --- Carregar arquivos ---
try:
    df_jornada = pd.read_csv("jornadas_salvas/jornada_planejada_salva.csv")
    df_barreiras = pd.read_csv("barreiras_salvas/barreiras_resposta_salva.csv")
    df_impacto = pd.read_csv("impactos_salvos/impacto_respostas_salvo.csv")
except FileNotFoundError:
    st.error("⚠️ Arquivos não encontrados. Envie os CSVs na página inicial.")
    st.stop()

# Paleta de cores moderna
CORES = ["#006D77", "#83C5BE", "#FFDDD2", "#E29578", "#6D597A"]

# ========================
# Visão Geral
# ========================
st.subheader("🔹 Visão Geral dos Dados")

col1, col2, col3 = st.columns(3)
col1.metric("Total de Jornadas", len(df_jornada))
col2.metric("Total de Barreiras", len(df_barreiras))
col3.metric("Total de Impactos", len(df_impacto))

st.markdown("---")


# =====================================================
# 🔹 ANÁLISE DE BARREIRAS
# =====================================================
st.header("🔹 Análise de Barreiras")

# Médias por categoria
barreiras_media_cat = df_barreiras.groupby("Categoria")["Resposta"].mean().reset_index()

fig_bar_cat = px.bar(
    barreiras_media_cat,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Média das Respostas por Categoria",
    text="Resposta"
)
fig_bar_cat.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_bar_cat.update_layout(yaxis=dict(range=[0, 5]))
st.plotly_chart(fig_bar_cat, use_container_width=True)

# Distribuição das notas
fig_hist_bar = px.histogram(
    df_barreiras,
    x="Resposta",
    nbins=5,
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Distribuição das Notas das Barreiras",
    barmode="group"
)
st.plotly_chart(fig_hist_bar, use_container_width=True)

# Boxplot
fig_box_bar = px.box(
    df_barreiras,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Distribuição de Notas por Categoria"
)
st.plotly_chart(fig_box_bar, use_container_width=True)


# =====================================================
# 🔹 ANÁLISE DE IMPACTOS
# =====================================================
st.header("🔹 Análise de Impactos")

impacto_media_cat = df_impacto.groupby("Categoria")["Resposta"].mean().reset_index()

fig_bar_imp = px.bar(
    impacto_media_cat,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Média dos Impactos por Categoria",
    text="Resposta"
)
fig_bar_imp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig_bar_imp.update_layout(yaxis=dict(range=[0, 5]))
st.plotly_chart(fig_bar_imp, use_container_width=True)

fig_hist_imp = px.histogram(
    df_impacto,
    x="Resposta",
    nbins=5,
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Distribuição das Notas dos Impactos",
    barmode="group"
)
st.plotly_chart(fig_hist_imp, use_container_width=True)

fig_box_imp = px.box(
    df_impacto,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    color_discrete_sequence=CORES,
    title="Distribuição dos Impactos por Categoria"
)
st.plotly_chart(fig_box_imp, use_container_width=True)


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
