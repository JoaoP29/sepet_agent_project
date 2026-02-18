```markdown
# 🤖 Prompt 2: Agentes de IA (CrewAI + MiniMax)

**Configuração:** Configure a orquestração de agentes usando **CrewAI** e a **API da MiniMax**.  
**Tarefa:** Criar o fluxo de análise de risco pós-agendamento.

---

### 📋 Requisitos

1. **Instalação de Dependências**
   - Instale `crewai` e `langchain-openai`.

2. **Agente Analista Clínico**
   - **Missão:** Realizar a leitura do campo `respostas_triagem` no banco de dados.
   - **Lógica de Risco:** 
     - Se o tutor respondeu **'Não'** para *"Entendeu o risco anestésico?"* ou indicou problemas graves, o agente deve marcar `alerta_risco = True` na tabela `triagens`.
   - **Geração de Parecer:**
     - Redigir o campo `parecer_ia` com base no histórico do animal.
     - *Exemplo:* "Animal com 13 anos e 6 meses, requer atenção especial".
```