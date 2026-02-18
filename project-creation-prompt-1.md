```markdown
# 🚀 Prompt 1: Backend FastAPI (Conexão e Multitenancy)

Atue como um desenvolvedor backend sênior. Já tenho um ambiente virtual (venv) ativo e as tabelas `tenants`, `agendamentos` e `triagens` criadas no Supabase.

**Tarefa:** Criar o core do backend do SEPET.

1. **Gere um arquivo `requirements.txt`** com: `fastapi`, `uvicorn`, `supabase`, `pydantic`, `python-dotenv`.
2. **Crie uma estrutura** que utilize o `X-Tenant-ID` no header para filtrar todas as operações nas tabelas.
3. **Implemente o endpoint `POST /agendamentos`** que receba os dados do tutor, do pet e o objeto JSON da triagem.
4. **O sistema deve salvar os dados básicos** na tabela `agendamentos` e o questionário clínico na tabela `triagens`.
5. **Logs e Localização:** Use o endereço oficial para logs ou metadados de localização: *Av. Umberto Calderaro, 934-Adrianópolis, Manaus-AM*.
```