import streamlit as st
from utils.auth import check_login
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Verifica se o usuário está logado
check_login()

st.image("cinco_logo.png")

st.set_page_config(page_title="Resultados", page_icon="📊", layout="wide")

st.title("📊 Resultados Gerais da Jornada")

# --- Caminhos dos arquivos ---
try:
    df_jornada = pd.read_csv("jornadas_salvas/jornada_planejada_salva.csv")
    df_barreiras = pd.read_csv("barreiras_salvas/barreiras_resposta_salva.csv")
    df_impacto = pd.read_csv("impactos_salvos/impactos_respostas_salvo.csv")
except FileNotFoundError:
    st.error("⚠️ Um ou mais arquivos não foram encontrados. Verifique se a jornada, barreiras e impactos foram salvos corretamente.")
    st.stop()

# --- Layout inicial ---
st.markdown("### 📍 Visão geral")
col1, col2, col3 = st.columns(3)
col1.metric("Etapas da Jornada", len(df_jornada))
col2.metric("Total de Barreiras Avaliadas", len(df_barreiras))
col3.metric("Total de Impactos Avaliados", len(df_impacto))

st.divider()

# =====================================================
# 🔹 ANÁLISE DE BARREIRAS
# =====================================================
st.subheader("🔹 Análise de Barreiras")

# Médias por categoria
barreiras_media_cat = df_barreiras.groupby("Categoria")["Resposta"].mean().reset_index()

fig_bar_cat = px.bar(
    barreiras_media_cat,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    title="Média das Respostas por Categoria (Barreiras)",
    text_auto=".2f"
)
st.plotly_chart(fig_bar_cat, use_container_width=True)

# Distribuição geral das notas
fig_hist_bar = px.histogram(
    df_barreiras,
    x="Resposta",
    nbins=5,
    title="Distribuição das Notas (1 a 5) das Barreiras",
    color="Categoria",
    barmode="overlay"
)
st.plotly_chart(fig_hist_bar, use_container_width=True)

# =====================================================
# 🔹 ANÁLISE DE IMPACTOS
# =====================================================
st.subheader("🔹 Análise de Impactos")

impacto_media_cat = df_impacto.groupby("Categoria")["Resposta"].mean().reset_index()

fig_bar_imp = px.bar(
    impacto_media_cat,
    x="Categoria",
    y="Resposta",
    color="Categoria",
    title="Média das Respostas por Categoria (Impactos)",
    text_auto=".2f"
)
st.plotly_chart(fig_bar_imp, use_container_width=True)

# Distribuição das notas de impacto
fig_hist_imp = px.histogram(
    df_impacto,
    x="Resposta",
    nbins=5,
    title="Distribuição das Notas (1 a 5) dos Impactos",
    color="Categoria",
    barmode="overlay"
)
st.plotly_chart(fig_hist_imp, use_container_width=True)

# =====================================================
# 🔹 CORRELAÇÃO ENTRE BARREIRAS E IMPACTOS
# =====================================================
st.subheader("🔹 Correlação entre Barreiras e Impactos")

# Combinar por Comportamento / Categoria / Tipo
merged = pd.merge(
    df_barreiras[["Comportamento", "Categoria", "Tipo", "Resposta"]],
    df_impacto[["Comportamento", "Categoria", "Tipo", "Resposta"]],
    on=["Comportamento", "Categoria", "Tipo"],
    suffixes=("_Barreira", "_Impacto"),
    how="inner"
)

if not merged.empty:
    fig_scatter = px.scatter(
        merged,
        x="Resposta_Barreira",
        y="Resposta_Impacto",
        color="Categoria",
        hover_data=["Comportamento", "Tipo"],
        title="Relação entre Respostas de Barreiras e Impactos"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Ainda não há dados suficientes para comparar Barreiras e Impactos.")

# =====================================================
# 🔹 EVOLUÇÃO DA JORNADA
# =====================================================
st.subheader("🔹 Evolução da Jornada e Barreiras por Etapa")

# Média das barreiras por comportamento
barreiras_jornada = df_barreiras.groupby("Comportamento")["Resposta"].mean().reset_index()
barreiras_jornada = barreiras_jornada.merge(df_jornada, on="Comportamento", how="left")

fig_line = px.line(
    barreiras_jornada,
    x="Comportamento",
    y="Resposta",
    markers=True,
    title="Evolução das Barreiras ao Longo da Jornada",
    hover_data=["Categoria", "Tipo"]
)
st.plotly_chart(fig_line, use_container_width=True)

# =====================================================
# 🔹 INSIGHTS AUTOMÁTICOS
# =====================================================
st.subheader("💡 Insights Automáticos")

media_barreiras = df_barreiras["Resposta"].mean()
media_impactos = df_impacto["Resposta"].mean()

st.write(f"• A **média geral das barreiras** foi **{media_barreiras:.2f}**, indicando nível {'alto' if media_barreiras <= 2 else 'moderado' if media_barreiras <= 3.5 else 'baixo'} de dificuldade.")
st.write(f"• A **média geral dos impactos** foi **{media_impactos:.2f}**, sugerindo impacto {'crítico' if media_impactos >= 4 else 'moderado' if media_impactos >= 2.5 else 'baixo'} sobre a jornada.")
st.write("• Categorias com maiores médias de barreiras podem indicar gargalos específicos na experiência do usuário.")