import streamlit as st
from utils.auth import check_login

# Verifica se o usuário está logado
check_login()

st.set_page_config(layout="centered")
st.image("cinco_logo.png")
left, mid, right = st.columns([1, 10, 1])
with mid:
    st.markdown("<h1 align='center'> Compreensão do Contexto </h1>", unsafe_allow_html=True)
    st.markdown("----")
    b1 = st.button("Sobre sludges", use_container_width=True)
    b2 = st.button("Informações gerais", use_container_width=True)
    b3 = st.button("Informações sobre usuários(as)", use_container_width=True)
    b4 = st.button("Informações sobre tempos", use_container_width=True)
    b5 = st.button("Informações sobre indicadores", use_container_width=True)
    b6 = st.button("Possíveis dificuldades", use_container_width=True)

if b1: st.session_state["section"] = "sobre_sludges"
elif b2: st.session_state["section"] = "info_gerais"
elif b3: st.session_state["section"] = "info_usuarios"
elif b4: st.session_state["section"] = "info_tempos"
elif b5: st.session_state["section"] = "info_indicadores"
elif b6: st.session_state["section"] = "possiveis_dificuldades"

#### Sobre sludges
if st.session_state.get("section") == "sobre_sludges":

    st.markdown("----")
    st.markdown("## Sobre sludges")

    st.markdown("### Você sabe o que são SLUDGES?")

    st.markdown("""
    São as barreiras práticas, emocionais ou sociais, sejam intencionais ou acidentais,
                que podem dificultar ou desencorajar determinados comportamentos e prejudicar
                o alcance dos objetivos das políticas públicas. Isso leva à desistência ou
                adiamento das ações das pessoas usuárias devido a dificuldades encontradas nos
                processos, mesmo que essas ações sejam benéficas para elas.
    """)

    st.markdown("### Impacto dos sludges nas políticas públicas")

    st.markdown("""
    As barreiras dentro das políticas públicas são fonte de desperdício de recursos e causa de ineficiência nas políticas públicas e, muitas vezes, são problemas ocultos. Alguns exemplos de impactos negativos dos sludges:

    🔎 **Desengajamento e Exclusão Social** - problemas como o uso de linguagem complexa, falta de informação, entre outros, pode desencorajar a participação das pessoas em programas governamentais e limitar o seu acesso a serviços públicos.

    🔎 **Inequidade** - sludges podem afetar de forma desproporcional grupos marginalizados ou economicamente vulnerabilizados, que podem ter menos recursos para superar essas barreiras, aumentando assim a desigualdade.

    🔎 **Custos adicionais** - sludges podem gerar custos adicionais para o governo e para os cidadãos, seja por meio de recursos desperdiçados em processos ineficientes ou por oportunidades perdidas devido à burocracia excessiva.

    🔎 **Ineficácia das políticas** - obstáculos e complexidade excessiva nas políticas públicas dificultam o acesso aos serviços e comprometem o alcance das metas institucionais.
    """)

    st.markdown("### F5 - Mapeamento Anti-Sludge")

    st.markdown("""
    O F5 Mapeamento Anti-Sludge da CINCO permite identificar e quantificar as barreiras comportamentais e dimensionar o impacto negativo dessas barreiras nas pessoas usuárias do serviço público digital. A aplicação de intervenções comportamentais pode reduzir tais atritos, e melhorar a qualidade do atendimento.

    Portanto, um dos objetivos do método anti-sludge da CINCO é melhorar a experiência dos C68 dos serviços públicos por meio do diagnóstico de barreiras, contribuindo assim com a melhoria do impacto e da efetividade das políticas públicas.

    Depois de definido o processo ou serviço a ser avaliado, o diagnóstico de sludges/barreiras é composto por 3 fases (Exploratória, Análise e Síntese), que por sua vez contemplam 6 etapas (Compreensão do Contexto, Mapeamento omportamental, Classificação dos Comportamentos, Dimensionamento do Impacto, Validação e Apresentação dos Resultados).

    Você está sendo convidada(o) a participar da 1ª etapa - Compreensão do Contexto, cujo objetivo é "Compreender melhor o contexto no qual o processo ou serviço sendo avaliado está inserido, por meio do levantamento de informações como objetivos, quantidade estimada de usuários, dados de monitoramento, hipóteses, dentre outras informações". 

    Vamos lá!?
    """)

#### Informações gerais
if st.session_state.get("section") == "info_gerais":
    
    st.markdown("----")
    st.markdown("## Informações gerais")

    with st.form("info_gerais_form"):
        nome = st.text_input("Qual o nome do processo ou serviço público que será analisado?")
        processo = st.text_input("Descreva o processo ou serviço público que será analisado.")
        objetivo = st.text_input("Qual o objetivo principal desse processo ou serviço?")
        esfera_gov = st.text_input("Qual esfera de governo é provedora do processo ou serviço público?")
        abrangemcia = st.text_input("Qual abrangência do processo ou serviço público?")
        publico_especifico = st.text_input("Caso você tenha respondido 'público específico' na pergunta anterior, descreva o público do processo ou serviço em análise.")

        submitted = st.form_submit_button("Enviar")

        if submitted:
            st.success("✅ Informações gerais salvas com sucesso!")
        else:
            st.info("⚠️ Por favor, preencha o formulário e clique em 'Enviar'.")
    
#### Informações sobre usuários(as)
if st.session_state.get("section") == "info_usuarios":
    
    st.markdown("----")
    st.markdown("## Informações sobre usuários(as)")

    with st.form("info_usuarios_form"):
        numero_usuarios = st.number_input("Qual o número estimado de usuários beneficiados pelo processo ou serviço no horizonte temporal de um ano?", min_value=0, step=1)
        selecao_compreensao_perfil = st.radio("Dentre as pessoas usuárias do processo ou serviço, há algum perfil cuja jornada comportamental a equipe deseja compreender melhor?", ("Sim", "Não"))
        info_compreensao_perfil = st.text_input("Se sim, descreva as principais características do perfil que será foco do mapeamento.")
        selecao_desenhou_processo = st.radio("Existe uma jornada do usuário planejada pela equipe que desenhou o processo?", ("Sim", "Não"))
        info_desenhou_processo = st.text_input("Se sim, descreva sucintamente a jornada planejada.")
        info_nao_desenhou_processo = st.text_input("Se não, descreva os comportamentos a serem realizados para atingir o objetivo com o processo ou serviço com base na experiência da equipe. Especifique, na descrição, se a jornada se refere ao perfil definido como foco para o mapeamento ou se às pessoas usuárias de maneira geral.")
        necessidade_servico_publico_considerado = st.text_input("Qual a necessidade que as pessoas usuárias têm pelo serviço público considerado? Responda de acordo com o perfil específico definido pela equipe ou de maneira geral, conforme o caso.")
        selecao_possibilidade_jornada = st.radio("As pessoas usuárias possuem mais de uma possibilidade de jornada possível para atingir seu objetivo com o processo?", ("Sim", "Não"))
        info_selecao_possibilidade_jornada = st.text_input("Se sim, quais são as jornadas possíveis para as pessoas usuárias?")

        submitted = st.form_submit_button("Enviar")

        if submitted:
            st.success("✅ Informações gerais salvas com sucesso!")
        else:
            st.info("⚠️ Por favor, preencha o formulário e clique em 'Enviar'.")

#### Informações sobre tempos
if st.session_state.get("section") == "info_tempos":
    
    st.markdown("----")
    st.markdown("## Informações sobre tempos envolvidos")

    with st.form("info_tempos_form"):
        estimativa_tempo_medio = st.text_input("Informe uma estimativa do tempo médio dedicado (em dias ou horas e minutos) por uma pessoa usuária do início da interação até obter o resultado desejado com o processo ou serviço público em análise.")

        submitted = st.form_submit_button("Enviar")

        if submitted:
            st.success("✅ Informações sobre tempos salvas com sucesso!")
        else:
            st.info("⚠️ Por favor, preencha o formulário e clique em 'Enviar'.")

#### Informações sobre indicadores
if st.session_state.get("section") == "info_indicadores":
    
    st.markdown("----")
    st.markdown("## Informações sobre indicadores de desempenho")

    with st.form("info_indicadores_form"):
        selecao_indicadores_desempenho = st.radio("Existem indicadores de desempenho para o processo ou serviço em análise?", ("Sim", "Não"))
        info_indicadores_desempenho = st.text_input("Se sim, descreva o principal indicador de desempenho que tem relação com o processo ou serviço em análise, explicando como ocorre essa relação.")

        submitted = st.form_submit_button("Enviar")

        if submitted:
            st.success("✅ Informações sobre indicadores salvas com sucesso!")
        else:
            st.info("⚠️ Por favor, preencha o formulário e clique em 'Enviar'.")

#### Possíveis dificuldades
if st.session_state.get("section") == "possiveis_dificuldades":
    
    st.markdown("----")
    st.markdown("## Levantamento de possíveis dificuldades comportamentais")

    with st.form("possiveis_dificuldades_form"):
        selecao_possiveis_dificuldades = st.radio("Existem registros de reclamação e de avaliação de satisfação por parte das pessoas usuárias do processo ou serviço público?", ("Sim", "Não"))
        info_possiveis_dificuldades = st.text_input("Se sim, descreva os principais registros de reclamação e de avaliação de satisfação das pessoas usuárias do processo ou serviço público.")
        selecao_quantidade_usuarios = st.radio("Existem registros de dados sobre a quantidade de pessoas usuárias que inicia o processo ou serviço comparada com a quantidade que o conclui satisfatoriamente?", ("Sim", "Não"))
        info_quantidade_usuarios = st.text_input("Se sim, descreva os principais registros.")
        selecao_dificuldade_previamente_identificada = st.radio("Existem registros de dados sobre dificuldades previamente identificadas por meio de relatos de executores e pessoas usuárias do processo ou serviço?", ("Sim", "Não"))
        info_dificuldade_previamente_identificada = st.text_input("Se sim, descreva os principais registros de dados sobre dificuldades previamente identificadas por meio de relatos de executores do processo ou serviço público.")
        info_dificuldade_previamente_identificada_2 = st.text_input("Se sim, também descreva os principais registros de dados sobre dificuldades previamente identificadas por meio de relatos de pessoas usuárias do processo ou serviço público.")
        selecao_hipoteses_dificuldades = st.radio("A equipe responsável tem hipóteses sobre dificuldades no serviço ou processo sendo avaliado?", ("Sim", "Não"))
        info_hipoteses_dificuldades = st.text_input("Se sim, descreva as principais hipóteses sobre dificuldades no serviço ou processo sendo avaliado.")

        submitted = st.form_submit_button("Enviar")

        if submitted:
            st.success("✅ Informações sobre possíveis dificuldades salvas com sucesso!")
        else:
            st.info("⚠️ Por favor, preencha o formulário e clique em 'Enviar'.")