import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(page_title="Diagnóstico JAC - Perplexity", layout="centered")

st.title("📊 Diagnóstico de Maturidade de Crédito")
st.markdown("Responda às perguntas para receber uma análise completa via IA.")

# --- SEU PROMPT PERSONALIZADO AQUI ---
# Edite este texto entre as aspas com o prompt que você já tem pronto.
PROMPT_DO_EDVAN = """
Você é um especialista em crédito e risco (Christopher Medeiros).
Analise os dados abaixo e forneça um diagnóstico detalhado sobre o nível de maturidade da empresa na metodologia JAC.
Seja direto, aponte os pontos fortes e o que falta para o próximo nível.
"""
# -------------------------------------

# Perguntas (Mesma estrutura anterior)
questions = [
    {"id": 1, "nivel": "Nível 1 (Descoberta)", "pergunta": "Existe um guia ou checklist para evitar decisões subjetivas nas análises manuais?"},
    {"id": 2, "nivel": "Nível 1 (Descoberta)", "pergunta": "O checklist está disponível nas ferramentas usadas (planilhas, ERP, CRM) para consulta imediata?"},
    {"id": 3, "nivel": "Nível 1 (Descoberta)", "pergunta": "Os clientes são classificados formalmente por risco/perfil e essa classificação é usada nas decisões?"},
    {"id": 4, "nivel": "Nível 1 (Descoberta)", "pergunta": "Existem critérios claros e documentados para definição de limites?"},
    {"id": 5, "nivel": "Nível 2 (Evolução)", "pergunta": "Alguma ferramenta sugere limites com base em dados históricos e comportamento?"},
    {"id": 6, "nivel": "Nível 2 (Evolução)", "pergunta": "Há níveis formais de alçada de aprovação ajustados ao valor e ao risco?"},
    {"id": 7, "nivel": "Nível 2 (Evolução)", "pergunta": "Existe registro completo e rastreável de quem aprovou cada decisão?"},
    {"id": 8, "nivel": "Nível 2 (Evolução)", "pergunta": "O processo de crédito está integrado aos sistemas de vendas e gestão (ERP, CRM)?"},
    {"id": 9, "nivel": "Nível 2 (Evolução)", "pergunta": "Existem regras de liberação automática configuradas e funcionando nos sistemas atuais?"},
    {"id": 10, "nivel": "Nível 3 (Consolidação)", "pergunta": "As metas comerciais e as regras de crédito são construídas e revisadas juntas para aumentar vendas com segurança?"},
    {"id": 11, "nivel": "Nível 3 (Consolidação)", "pergunta": "O time financeiro atua como parceiro do comercial para viabilizar negócios com segurança?"},
    {"id": 12, "nivel": "Nível 3 (Consolidação)", "pergunta": "As sugestões de limites são revisadas e ajustadas periodicamente com base em dados atualizados?"},
    {"id": 13, "nivel": "Nível 3 (Consolidação)", "pergunta": "O tempo médio para aprovar crédito é medido e acompanhado regularmente?"},
    {"id": 14, "nivel": "Nível 3 (Consolidação)", "pergunta": "Os indicadores de crédito são acompanhados em relatórios ou dashboards (Excel, BI etc.)?"},
    {"id": 15, "nivel": "Nível 4 (Alta Performance)", "pergunta": "A equipe comercial sabe explicar e defender os critérios de crédito para clientes e negociações?"},
]

opcoes = {
    0: "0 - Inexistente",
    1: "1 - Informal/Parcial",
    2: "2 - Estruturado"
}

respostas_usuario = {}

with st.form("diagnostico_form"):
    for q in questions:
        st.markdown(f"**{q['pergunta']}**")
        respostas_usuario[q['pergunta']] = st.radio(
            f"Opção:",
            options=[0, 1, 2],
            format_func=lambda x: opcoes[x],
            key=q['id'],
            label_visibility="collapsed"
        )
        st.markdown("---")

    submitted = st.form_submit_button("Gerar Relatório com IA")

if submitted:
    # 1. Compilar os dados
    texto_respostas = "Respostas do Cliente:\n"
    scores = {"Nível 1 (Descoberta)": 0, "Nível 2 (Evolução)": 0, "Nível 3 (Consolidação)": 0, "Nível 4 (Alta Performance)": 0}

    for q in questions:
        resp = respostas_usuario[q['pergunta']]
        scores[q['nivel']] += resp
        texto_respostas += f"- {q['pergunta']}: {opcoes[resp]}\n"

    # 2. Montar a mensagem final para a API
    mensagem_final = f"{PROMPT_DO_EDVAN}\n\n{texto_respostas}"

    # 3. Chamar a API da Perplexity
    try:
        with st.spinner('A Inteligência Artificial está analisando seu perfil...'):
            client = OpenAI(
                api_key=st.secrets["PERPLEXITY_API_KEY"], # Pega a chave dos segredos
                base_url="https://api.perplexity.ai"
            )

            response = client.chat.completions.create(
                model="sonar-pro", # Modelo recomendado da Perplexity
                messages=[
                    {"role": "system", "content": "Você é um consultor especialista em crédito."},
                    {"role": "user", "content": mensagem_final},
                ]
            )

            analise = response.choices[0].message.content

            st.success("Análise Concluída!")
            st.subheader("📢 Diagnóstico JAC:")
            st.write(analise)

    except Exception as e:
        st.error(f"Erro ao conectar com a IA: {e}")
        st.info("Verifique se a chave da API está configurada corretamente nos 'Secrets' do Streamlit.")
