import streamlit as st
from pathlib import Path

st.title("🗺️ Mapeamento Comportamental")

# Exibe a imagem do mapeamento
image_path = Path(__file__).parent.parent / "assets" / "mapeamento.png"
st.image(str(image_path), use_container_width=True)

# Botões
col1, col2 = st.columns(2)
with col1:
    if st.button("Jornada Planejada"):
        st.info("Abrindo jornada planejada...")
with col2:
    if st.button("Jornada Padrão"):
        st.success("Abrindo jornada padrão...")
