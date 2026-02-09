import streamlit as st
import pandas as pd # pip install pandas (se necessário)
from automacao_pf.main import validar_entrega_fabrica
from automacao_pf.db_handler import buscar_relatorio_geral

st.set_page_config(page_title="Gestão DTI-PF", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* 1. Botão Validar: Amarelo com borda preta */
    div.stButton > button:first-child {
        background-color: #FFCC00 !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* 2. Inputs e Selectbox: Contorno Amarelo ao clicar (Remove o Rosa) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        border-color: #003366 !important; /* Borda padrão azul */
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #FFCC00 !important; /* Borda amarela ao clicar */
        box-shadow: 0 0 0 0.2rem rgba(255, 204, 0, 0.25) !important;
    }

    /* 3. Abas: Letras em Azul Escuro e Marca-texto em Amarelo */
    button[data-baseweb="tab"] {
        color: #003366 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #FFCC00 !important;
    }

    /* 4. Tabela e Títulos */
    thead tr th {
        background-color: #000000 !important;
        color: white !important;
    }
    h1, h2, h3, h4 {
        color: #003366 !important;
    }
    
    /* Garantia global contra o contorno rosa */
    .stSelectbox:focus-within, .stTextInput:focus-within {
        border-color: #FFCC00 !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.title(" Portal de Governança e Auditoria DTI-PF")
# Texto de Contexto Refinado
st.markdown("""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #003366;">
    <h4 style="margin-top: 0; color: #003366;"> Sobre este Portal</h4>
    <p style="font-size: 14px; color: #000000;">
        Esta ferramenta automatiza a validação do <b>Definition of Done (DoD)</b> entre as equipes de Infraestrutura e Fábrica de Software.
    </p>
    <p style="font-size: 14px; font-weight: bold; color: #003366; margin-bottom: 0;">
        ⚠️ Dados para Teste: Utilize os IDs de PF-1025 a PF-1029.
    </p>
</div>
<br>
""", unsafe_allow_html=True)

# Abas para organizar a visão do Gestor
aba1, aba2 = st.tabs(["🔍 Consulta Individual", "📊 Relatório Geral (Gestão)"])

with aba1:
    issue_id = st.text_input("ID da Demanda:", placeholder="PF-1025")
    if st.button("Validar"):
        resultado = validar_entrega_fabrica(issue_id)
        st.info(resultado)

with aba2:
    st.subheader("Filtros de Período")
    # Seletor de tempo
    periodo = st.selectbox("Visualizar atualizações de:", 
                          ["Ontem", "Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias"])
    
    mapeamento_dias = {"Ontem": 1, "Últimos 7 dias": 7, "Últimos 15 dias": 15, "Últimos 30 dias": 31}
    dias = mapeamento_dias[periodo]

    # Busca os dados para a lista
    res = buscar_relatorio_geral(dias)
    
    if res.data:
        # 1. Cria o DataFrame
        df = pd.DataFrame(res.data)
        
        # 2. Renomeia as colunas (Ajuste para bater com as colunas do banco)
        # O banco retorna: id, issue_jira, script_banco_executado, doc_homologacao_anexado, data_validacao
        df.columns = ['ID', 'Ticket Jira', 'Banco OK', 'Doc OK', 'Data Atualização']
        
        # 3. Converte a coluna para data de verdade e ordena
        df['Data Atualização'] = pd.to_datetime(df['Data Atualização'])
        df = df.sort_values(by='Data Atualização', ascending=False)
        
        # 4. Exibe a tabela com formatação limpa 
        st.dataframe(df.style.format({"Data Atualização": lambda t: t.strftime('%d/%m/%Y %H:%M')}), use_container_width=True)
    else:
        st.warning("Nenhuma atualização encontrada neste período.")
