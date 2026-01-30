import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Diagnóstico JAC - Jornada da Análise de Crédito", layout="centered")

st.title("📊 Diagnóstico de Maturidade de Crédito")
st.markdown("Responda às perguntas abaixo para descobrir em qual nível da **JAC (Jornada da Análise de Crédito)** sua empresa está.")

# Definição das Perguntas e Grupos (Níveis)
questions = [
    # Nível 1 - Descoberta
    {"id": 1, "nivel": "Nível 1 (Descoberta)", "pergunta": "Existe um guia ou checklist para evitar decisões subjetivas nas análises manuais?"},
    {"id": 2, "nivel": "Nível 1 (Descoberta)", "pergunta": "O checklist está disponível nas ferramentas usadas (planilhas, ERP, CRM) para consulta imediata?"},
    {"id": 3, "nivel": "Nível 1 (Descoberta)", "pergunta": "Os clientes são classificados formalmente por risco/perfil e essa classificação é usada nas decisões?"},
    {"id": 4, "nivel": "Nível 1 (Descoberta)", "pergunta": "Existem critérios claros e documentados para definição de limites?"},

    # Nível 2 - Evolução
    {"id": 5, "nivel": "Nível 2 (Evolução)", "pergunta": "Alguma ferramenta sugere limites com base em dados históricos e comportamento?"},
    {"id": 6, "nivel": "Nível 2 (Evolução)", "pergunta": "Há níveis formais de alçada de aprovação ajustados ao valor e ao risco?"},
    {"id": 7, "nivel": "Nível 2 (Evolução)", "pergunta": "Existe registro completo e rastreável de quem aprovou cada decisão?"},
    {"id": 8, "nivel": "Nível 2 (Evolução)", "pergunta": "O processo de crédito está integrado aos sistemas de vendas e gestão (ERP, CRM)?"},
    {"id": 9, "nivel": "Nível 2 (Evolução)", "pergunta": "Existem regras de liberação automática configuradas e funcionando nos sistemas atuais?"},

    # Nível 3 - Consolidação
    {"id": 10, "nivel": "Nível 3 (Consolidação)", "pergunta": "As metas comerciais e as regras de crédito são construídas e revisadas juntas para aumentar vendas com segurança?"},
    {"id": 11, "nivel": "Nível 3 (Consolidação)", "pergunta": "O time financeiro atua como parceiro do comercial para viabilizar negócios com segurança?"},
    {"id": 12, "nivel": "Nível 3 (Consolidação)", "pergunta": "As sugestões de limites são revisadas e ajustadas periodicamente com base em dados atualizados?"},
    {"id": 13, "nivel": "Nível 3 (Consolidação)", "pergunta": "O tempo médio para aprovar crédito é medido e acompanhado regularmente?"},
    {"id": 14, "nivel": "Nível 3 (Consolidação)", "pergunta": "Os indicadores de crédito são acompanhados em relatórios ou dashboards (Excel, BI etc.)?"},

    # Nível 4 - Alta Performance
    {"id": 15, "nivel": "Nível 4 (Alta Performance)", "pergunta": "A equipe comercial sabe explicar e defender os critérios de crédito para clientes e negociações?"},
]

opcoes = {
    0: "0 - Inexistente (Não há processo/ferramenta)",
    1: "1 - Informal/Parcial (Inconsistente/Ocasional)",
    2: "2 - Estruturado (Processo claro/Documentado/Sustentado)"
}

respostas_usuario = {}

# Loop para criar o formulário
with st.form("diagnostico_form"):
    for q in questions:
        st.markdown(f"**{q['pergunta']}**")
        respostas_usuario[q['pergunta']] = st.radio(
            f"Selecione para a pergunta {q['id']}:",
            options=[0, 1, 2],
            format_func=lambda x: opcoes[x],
            key=q['id']
        )
        st.markdown("---")

    submitted = st.form_submit_button("Gerar Diagnóstico")

if submitted:
    st.success("Respostas enviadas com sucesso! Gerando análise...")

    # Compilação dos dados para o Prompt
    texto_para_prompt = "O cliente respondeu ao diagnóstico de maturidade de crédito (JAC). Abaixo as respostas:\n\n"

    scores = {"Nível 1 (Descoberta)": 0, "Nível 2 (Evolução)": 0, "Nível 3 (Consolidação)": 0, "Nível 4 (Alta Performance)": 0}
    max_scores = {"Nível 1 (Descoberta)": 4*2, "Nível 2 (Evolução)": 5*2, "Nível 3 (Consolidação)": 5*2, "Nível 4 (Alta Performance)": 1*2}

    for q in questions:
        resposta = respostas_usuario[q['pergunta']]
        nivel = q['nivel']
        scores[nivel] += resposta
        texto_para_prompt += f"- Pergunta: {q['pergunta']}\n  - Nível JAC: {nivel}\n  - Resposta do Cliente: {opcoes[resposta]}\n\n"

    texto_para_prompt += "Resumo dos Scores por Nível:\n"
    for nivel, score in scores.items():
        percentual = (score / max_scores[nivel]) * 100
        texto_para_prompt += f"- {nivel}: {percentual:.1f}% de aproveitamento.\n"

    st.subheader("📋 Copie o texto abaixo e cole no seu PROMPT:")
    st.text_area("Dados para a IA:", value=texto_para_prompt, height=400)

    st.info("Dica: Se você tiver acesso à API da OpenAI, podemos conectar seu prompt diretamente aqui para a resposta sair automática.")

