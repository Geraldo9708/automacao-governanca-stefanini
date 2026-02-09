from automacao_pf.db_handler import buscar_status_infra

def validar_entrega_fabrica(issue_id):
    res = buscar_status_infra(issue_id)
    
    # 1. Tratamento de erro: Caso o ID não exista no banco
    if not res.data:
        return f"❌ Erro: Demanda {issue_id} não encontrada no banco."

    status = res.data[0]
    script = status['script_banco_executado']
    doc = status['doc_homologacao_anexado']
    
    # 2. Lógica de Decisão 
    
    # CASO A: TUDO PRONTO (Sucesso para a Área Gestora)
    if script and doc:
        return "✅ Pronto para Homologação! Notificando Área Gestora."
    
    # CASO B: NADA PRONTO (Pendência Geral ou Início de Sprint)
    elif not script and not doc:
        return f"⚪ Pendência Geral: {issue_id} aguarda definições de Infra e Fábrica."
    
    # CASO C: FALHA ESPECÍFICA (Bloqueio técnico)
    else:
        detalhe = "falta Script de Banco" if not script else "falta Documentação"
        return f"⚠️ Bloqueado: Pendência técnica ({detalhe})."
