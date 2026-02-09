import streamlit as st
import pandas as pd # pip install pandas (se necessário)
from automacao_pf.main import validar_entrega_fabrica
from automacao_pf.db_handler import buscar_relatorio_geral

st.set_page_config(page_title="Gestão DTI-PF", page_icon="🛡️", layout="wide")

st.title(" Portal de Governança e Auditoria DTI-PF")
# Texto de Contexto Refinado
st.markdown("""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
    <h4 style="margin-top: 0;"> Sobre este Portal</h4>
    <p style="font-size: 14px; color: #31333F;">
        Esta ferramenta automatiza a validação do <b>Definition of Done (DoD)</b> entre as equipes de Infraestrutura e Fábrica de Software. 
        Garante que nenhuma demanda avance para homologação sem os devidos artefatos técnicos.
    </p>
    <p style="font-size: 14px; font-weight: bold; color: #ff4b4b; margin-bottom: 0;">
        ⚠️ Dados para Teste: Utilize os IDs de PF-1025 a PF-1029 para simular cenários reais de governança.
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
        
        # 2. Renomeia as colunas (Ajuste para bater com as colunas do seu banco)
        # O banco retorna: id, issue_jira, script_banco_executado, doc_homologacao_anexado, data_validacao
        df.columns = ['ID', 'Ticket Jira', 'Banco OK', 'Doc OK', 'Data Atualização']
        
        # 3. Converte a coluna para data de verdade e ordena
        df['Data Atualização'] = pd.to_datetime(df['Data Atualização'])
        df = df.sort_values(by='Data Atualização', ascending=False)
        
        # 4. Exibe a tabela com formatação limpa (mostra apenas data e hora, sem microsegundos)
        st.dataframe(df.style.format({"Data Atualização": lambda t: t.strftime('%d/%m/%Y %H:%M')}), use_container_width=True)
    else:
        st.warning("Nenhuma atualização encontrada neste período.")
