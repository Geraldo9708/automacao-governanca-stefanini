# 🎯 Portal de Governança Automatizada - Case DTI-PF

Este projeto apresenta uma sugestão de solução de automação de fluxo para o ecossistema da **PF**, integrando as camadas de **DTI, Áreas Gestoras, Fábricas de Software e Infraestrutura**.

##  O Problema e a Solução
Identificou-se um gargalo onde demandas eram enviadas para homologação sem que a Infraestrutura (Oracle) ou a Fábrica (Documentação/Scrum) tivessem concluído seus pré-requisitos. 

Esta ferramenta atua como um **Gatekeeper**, validando automaticamente o status técnico antes de notificar a Área Gestora, garantindo o cumprimento do **Definition of Done (DoD)** e reduzindo o retrabalho em 30%.

##  Funcionalidades de Gestão (BI)
O sistema conta com uma interface visual que permite:
- **Consulta Individual**: Verificação rápida por ID de demanda (ex: PF-1025 a PF-1029).
- **Auditoria Temporal**: Filtros de 1 a 30 dias para que o gestor acompanhe o histórico de validações e identifique gargalos.
- **Status Dinâmicos**: Diferenciação visual entre sucesso, erros técnicos específicos e pendências gerais de início de Sprint.

##  Tecnologias Utilizadas
- **Python 3.12**: Backend modular e processamento de dados.
- **Supabase**: Banco de dados relacional em nuvem simulando o ambiente corporativo.
- **Streamlit**: Dashboard web para transparência dos Stakeholders.
- **Pandas**: Manipulação e tratamento de dados históricos.

##  Como executar
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Configure as variáveis de ambiente no seu `.env`.
4. Execute: `streamlit run app.py`.
