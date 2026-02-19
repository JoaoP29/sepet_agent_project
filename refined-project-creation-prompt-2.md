```markdown
# 🤖 Prompt para o Antigravity: Refatoração para Multi-Agent com CrewAI

> **Persona:** Atue como um Engenheiro de IA.
> **Objetivo:** Refatorar o módulo `app/agents/clinical_analyst.py` para utilizar o framework **CrewAI** em vez de chamadas diretas ao SDK da OpenAI.

## 🎯 Objetivo Geral
Implementar uma orquestração sequencial com 3 agentes distintos para processar dados de triagem e informações do pet.

## ⚙️ Configurações Iniciais
- **Dependências:** Adicionar `crewai` e `langchain-openai` ao `requirements.txt`.
- **LLM:** Configurar o CrewAI para usar **MiniMax** via `ChatOpenAI` (LangChain).
  - **Endpoint:** `https://api.minimaxi.chat/v1`
  - **Modelo:** `MiniMax-Text-01`

## 👥 Estrutura de Agentes e Tarefas

### 1. Agente Analista de Triagem (O "Lupa")
- **Perfil:** Especialista em coleta de dados veterinários.
- **Tarefa:** Extrair e organizar informações do pet (ex: "O que imaginar", 13 anos e 6 meses) e as 19 respostas do questionário.
- **Foco:** Garantir que nenhum dado vital foi omitido.

### 2. Agente Verificador de Riscos (O "Juiz")
- **Perfil:** Auditor de segurança cirúrgica veterinária.
- **Tarefa:** Analisar as respostas extraídas em busca de pontos críticos:
  - Falta de jejum.
  - Desconhecimento do risco anestésico.
  - Desmaios ou convulsões.
- **Saída:** Emitir um veredito booleano (`True`/`False`) para `alerta_risco`.

### 3. Agente de Redação Clínica (O "Relator")
- **Perfil:** Redator médico veterinário.
- **Tarefa:** Consolidar as informações do "Lupa" e o veredito do "Juiz".
- **Saída:** Parecer profissional e humanizado para o campo `parecer_ia`, mencionando se o animal é geriátrico ou se há riscos específicos.

## 🛠️ Entrega Técnica
- **Formato de Saída:** Objeto JSON: `{"alerta_risco": bool, "parecer_ia": str}`.
- **Ponto de Entrada:** Manter a função `analisar_triagem`, disparando a execução da Crew.
- **Resiliência:** Preservar a lógica de `_analise_fallback` para falhas na API MiniMax.

---

### 💡 Por que este prompt é eficaz?
1. **Contexto Mantido:** Cita dados reais ("O que imaginar", "13 anos e 6 meses") para alinhar a compreensão da IA.
2. **Segurança Técnica:** Garante o fallback determinístico, essencial para o SEPET (saúde pública).
3. **Foco no Documento:** Reforça pontos críticos como jejum e termos de consentimento.
```