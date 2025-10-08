import streamlit as st
import pandas as pd
import base64
import streamlit.components.v1 as components
import datetime
from io import StringIO

st.set_page_config(layout="centered")

# ========================
# Mapping Categoria -> Tipo
# ========================
categoria_map = {
    "Busca e Acesso": "Envolve o conjunto de comportamentos que a pessoa usuária realiza para localizar, acessar e verificar informações.\n ex:\n - inserir palavras-chave para encontrar informações específicas;\n - navegar pelos menus principais e secundários do site ou aplicativo;\n - ler e verificar informações apresentadas;\n - realizar login.",
    "Preparação e Entrega": "Envolve o conjunto de comportamentos necessários para elaborar, preencher, encaminhar informações e manifestar concordância.\n ex:\n - preencher informações de cadastro;\n - solicitar agendamento;\n - anexar certificados de cursos realizados;\n - assinar documento;\n - confirmar leitura ou recebimento de mensagem;",
    "Interação": "Envolve os comportamentos de interação, simultâneos ou não, para tirar dúvidas, enviar sugestões ou reclamações.\n ex:\n - entrar em contato com o suporte para tirar dúvida;\n - entrar em contato com a Ouvidoria para registrar uma reclamação.",
    "Escolha": "Envolve os comportamentos relacionados à análise e seleção de alternativas que sejam relevantes para a continuidade do processo. Pequenas escolhas que tenham pouco ou nenhum impacto no andamento do processo, não precisam ser registradas.\n ex:\n - escolher entre as opções de pagamento disponíveis (boleto, dévbito, PIX);\n - indicar o tipo de declaração do imposto de renda (simplificada ou completa).",
    "Espera": "Envolve o comportamento de aguardar uma ação externa.\n ex?\n - aguardar a resposta de um e-mail;\n - aguardar seu atendimento em fila de espera virtual.",
    "Outros": "Envolve comportamentos relevantes que não estão presentes nas opções pré-definidas ou são específicos do processo que está sendo mapeado.\n ex:\n - comprovar requisito específico do processo;\n - entrar em contato com agente externo ao serviço para tirar dúvidas (como familiar ou colega de trabalho)"
}

tipo_map = {
    "Procurar site ou aplicativo": "É o comportamento da pessoa usuária relacionado a identificar e buscar a plataforma digital mais adequada para se conectar com o serviço.\n ex:\n - localizar o site do INSS.",
    "Acessar serviço": "É o comportamento da pessoa usuária que envolve estabelecer uma conexão com site ou aplicativo do serviço.\n ex:\n - entrar na página do INSS.",
    "Verificar elegibilidade": "É o comportamento de buscar identificar se um indivíduo ou instituição cumpre os requisitos necessários para utilizar um serviço ou acessar um benefício.\n ex:\n - checar requisitos para solicitar desconto da taxa de inscrição de um concurso público",
    "Realizar login": "É o comportamento da pessoa usuária de autenticar-se em uma plataforma digital para ter acesso a funcionalidades e recursos restritos.\n ex:\n - realizar reconhecimento facial ou digital;\n - utilizar autenticação social (via redes sociais).",
    "Navegar": "É o comportamento da pessoa usuária de interagir com as diferentes telas e recursos disponíveis na plataforma digital do orgão ou serviço.\n ex:\n - clicar em links internos para navegar entre as diferentes páginas de um site.",
    "Acessar conteúdo": "É o comportamento da pessoa usuária de interagir com informações apresentadas na plataforma digital, envolvendo atenção e compreensão do texto ou imagens, inclusive por meio de tecnologias acessíveis.\n ex:\n - fazer leitura de informações sobre renovação de documentos.",

    "Preencher": "É o comportamento da pessoa usuária de inserir dados específicos, em campos pré-determinados, com o objetivo de registrar ou comunicar informações relevantes para solicitar o serviço fim.\n ex:\n - preencher um formulário para informar as atividades profissionais realizadas em determinado mês.",
    "Organizar e anexar": "É o comportamento da pessoa usuária de coletar, organizar e transferir para o site ou aplicativo informações e arquivos digitais para um determinado fim.\n ex:\n - reunir todos os documentos necessários para comprovar o desenvolvimento de um projeto (planilhas, cronogramas, relatórios).",
    "Enviar": "É o comportamento da pessoa usuária de transmitir os dados inseridos no formulário para o serviço.\n ex:\n - enviar informações para solicitação de passaporte.",
    "Consentir": "É o comportamento da pessoa usuária de manifestar concordância formal ou assinar os termos necessários para o serviço.\n ex:\n - assinar os termos para confirmar leitura e compreensão das condições de um contrato específico.",

    "Interagir sincronamente": "É o comportamento da pessoa usuária de comunicar-se instantaneamente com o suporte do serviço.\n ex:\n - iniciar uma conversa com atendente por meio de uma janela de chat integrada ao site do serviço.",
    "Interagir assincronamente": "É o comportamento da pessoa usuária de comunicar-se com o suporte do serviço de maneira não instantânea, com respostas em tempos distintos.\n ex:\n - enviar um e-mail para o suporte do serviço, expondo determinada questão. ",

    "Selecionar entre alternativas": "É o comportamento da pessoa usuária de escolher entre diferentes opções ou atributos de um serviço, a fim de personalizar a experiência do usuário ou atender a necessidades específicas.\n ex:\n - escolher entre as opções disponíveis para entrar em contato com o suporte ao enfrentar dificuldades de acesso.",

    "Espera passiva": "É o comportamento da pessoa usuária de aguardar a resposta.\n ex:\n - aguardar a resposta de um e-mail.",
    "Espera ativa": "É o comportamento da pessoa usuária de aguardar sua vez de ser atendido em um sistema que o posiciona em uma fila virtual.\n ex:\n - aguardar sua vez de ser atendido(a) em chat online.",

    "Comportamento novo": "Refere-se a um comportamento exclusivo ou atípico de determinado processo.\n ex:\n - cumprir algum requisito ou ação pouco usual em outros processos;\n - entrar em contato com agente externo ao serviço para tirar dúvidas (como familiar ou colega de trabalho)."
}

categoria_tipo_map = {
    "Busca e Acesso": [
        "Procurar site ou aplicativo", "Acessar serviço",
        "Verificar elegibilidade", "Realizar login", "Navegar", "Acessar conteúdo"
    ],
    "Preparação e Entrega": [
        "Preencher", "Organizar e anexar", "Enviar", "Consentir"
    ],
    "Interação": [
        "Interagir sincronamente", "Interagir assincronamente"
    ],
    "Escolha": [
        "Selecionar entre alternativas"
    ],
    "Espera": [
        "Espera passiva", "Espera ativa"
    ],
    "Outros": ["Comportamento novo"],
}

# ========================
# Layout
# ========================
left, mid, right = st.columns([1, 10, 1])
with mid:
    st.markdown("# 🗺️ Mapeamento Comportamental")
    st.markdown("----")
    b1 = st.button("Informações Gerais", use_container_width=True)
    b2 = st.button("Jornada Planejada", use_container_width=True)
    b3 = st.button("Jornada Padrão", use_container_width=True)

if b1:
    st.session_state["section"] = "info_gerais"
elif b2:
    st.session_state["section"] = "jornada_planejada"
elif b3:
    st.session_state["section"] = "jornada_padrao"

# ========================
# Informações gerais
# ========================
if st.session_state.get("section") == "info_gerais":

    st.markdown("----")
    st.markdown("## Informações Gerais")

    st.markdown("### O que faremos aqui?")
    st.markdown("""
    Esta etapa tem o objetivo de mapear os comportamentos da jornada padrão.
    \nO ponto de partida é a **jornada planejada** pelos implementadores da política pública como sendo o melhor caminho para as pessoas usuárias acessarem o serviço pretendido.
    \nComo o planejado nem sempre é o que de fato acontece, **jornadas individuais**, reais, devem ser mapeadas por meio da observação dos comportamentos realizados por algumas pessoas.
    \nA partir dessa observação e da análise comparativa entre elas, a equipe responsável pelo mapeamento identificará a **jornada padrão**, que é a jornada a ser considerada e dimensionada na próxima etapa.
    """)

    st.markdown("### Tipos de jornada")
    st.markdown("#### Jornada Planejada")
    st.markdown("É a jornada construída a partir das informações disponibilizadas pela equipe do serviço ou a partir do manual do serviço.")
    st.markdown("#### Jornada Individual")
    st.markdown("É a jornada de uma pessoa usuária, observada individualmente.")
    st.markdown("#### Jornada Padrão")
    st.markdown("Trata-se de uma jornada 'normalizada', baseada nas jornadas dos usuários (que normalmente as pessoas fazem).")

    st.markdown("> ❗Siga a sequência de passos e vá aprofundando o conhecimento sobre o processo que está sendo analisado. Use o glossário para dúvidas conceituais.")

    st.markdown("### Passo-a-passo")
    st.write(":yellow[1° (Planilha)]: Selecione **Jornada Planejada** no menu acima para ser direcionado...")
    st.write(":yellow[2° (MIRO)]: Mapeie os comportamentos relacionados na ordem em que devem acontecer...")
    st.write(":yellow[3° (MIRO)]: Valide a **Jornada Planejada** com a equipe do serviço, se possível...")
    st.write(":yellow[4° (Planilha)]: Transfira da **Jornada Planejada** e valide para os locais correspondentes...")
    st.write(":yellow[5° (Planilha)]: Selecione **Jornada Padrão**, clique em 'Planejamento da observação'...")
    st.write(":yellow[6° (Teams)]: Realize a observação de pessoas usuárias...")
    st.write(":yellow[7° (Planilha)]: Transfira para a **Jornada** de cada pessoa usuária...")
    st.write(":yellow[8° (Planilha)]: Defina a **Jornada padrão**, síntese das jornadas individuais...")
    st.write(":yellow[9° (Planilha)]: Prossiga para a etapa 3, Classificação Comportamental, pelo menu superior.")

# ========================
# Jornada Planejada
# ========================
if st.session_state.get("section") == "jornada_planejada":

    st.markdown("----")
    st.markdown("## Jornada Planejada")

    # Init storage
    if "rows" not in st.session_state:
        st.session_state.rows = [
            {"Comportamento": "", "Categoria": "Busca e Acesso", "Tipo": ""}
        ]

    new_rows = []
    for idx, row in enumerate(st.session_state.rows):
        with st.expander(f"Comportamento {idx+1}", expanded=True):
            comportamento = st.text_input(
                "Comportamento",
                row.get("Comportamento", ""),
                key=f"comp_{idx}"
            )

            categoria = st.selectbox(
                "Categoria",
                list(categoria_tipo_map.keys()),
                index=list(categoria_tipo_map.keys()).index(
                    row.get("Categoria", "Busca e Acesso")
                ),
                key=f"cat_{idx}"
            )

            # Mostrar descrição automática da categoria
            st.caption(f"📌 Descrição da categoria: {categoria_map[categoria]}")

            tipo_options = categoria_tipo_map[categoria]
            tipo = st.selectbox(
                "Tipo",
                tipo_options,
                index=tipo_options.index(row.get("Tipo", tipo_options[0]))
                if row.get("Tipo") in tipo_options else 0,
                key=f"tipo_{idx}"
            )

            # Mostrar descrição automática do tipo
            st.caption(f"📝 Descrição do tipo: {tipo_map[tipo]}")

            new_rows.append({
                "Comportamento": comportamento,
                "Categoria": categoria,
                "Tipo": tipo
            })

    # Update session state
    st.session_state.rows = new_rows

    # Add button for new rows
    if st.button("➕ Adicionar Comportamento"):
        st.session_state.rows.append({"Comportamento": "", "Categoria": "Busca e Acesso", "Tipo": ""})

    # ---------- Botão Salvar Jornada ----------
    if st.button("Salvar Jornada"):
        df = pd.DataFrame(st.session_state.rows)
        st.success("✅ Jornada salva com sucesso!")

        # Mostrar tabela no app
        st.dataframe(df, use_container_width=True)

        # Converter para CSV
        csv_str = df.to_csv(index=False)
        b64 = base64.b64encode(csv_str.encode()).decode()

        # Nome do arquivo com timestamp (opcional)
        filename = "jornada_planejada_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

        # HTML/JS que cria um link 'data:' e dispara o click automaticamente
        # (usamos components.html porque é mais confiável para executar JS)
        html = f"""
        <html>
        <body>
            <a id="dl" href="data:text/csv;base64,{b64}" download="{filename}"></a>
            <script>
            // Tenta disparar o download imediatamente.
            const a = document.getElementById('dl');
            if (a) {{
                // Em alguns browsers a execução imediata funciona; caso contrário,
                // o fallback (download_button) ficará visível abaixo para o usuário clicar.
                a.click();
            }}
            </script>
        </body>
        </html>
        """

        # Injetar o HTML (altura pequena para não ocupar muito espaço)
        components.html(html, height=50)

        # Fallback: se o navegador bloquear o download automático,
        # mostramos um botão visível para que o usuário baixe manualmente.
        st.markdown("---")
        st.info("Se o download não iniciar automaticamente, use o botão abaixo.")
        st.download_button(
            label="⬇️ Baixar Jornada (CSV)",
            data=csv_str,
            file_name=filename,
            mime="text/csv",
        )