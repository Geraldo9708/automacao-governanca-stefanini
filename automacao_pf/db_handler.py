import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, timedelta

# Isso garante que ele procure o .env na pasta raiz do projeto
load_dotenv() 

def buscar_status_infra(issue_id):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    # Adicione este print temporário para testar se as chaves estão sendo lidas
    # print(f"DEBUG: URL={url} | KEY_INICIO={key[:5]}...") 

    supabase = create_client(url, key)
    return supabase.table("controle_sprints").select("*").eq("issue_jira", issue_id).execute()

def buscar_relatorio_geral(dias):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    # Calcula a data de corte (ex: hoje - 7 dias)
    data_corte = (datetime.now() - timedelta(days=dias)).isoformat()
    
    # Busca demandas atualizadas desde a data de corte
    return supabase.table("controle_sprints").select("*").gte("data_validacao", data_corte).execute()