# 🐾 SEPET — Sistema de Castração de Pets

Sistema web para gerenciamento de agendamentos de castração de animais, com triagem clínica automatizada e análise de risco assistida por **Inteligência Artificial**.

> Projeto desenvolvido para o **Serviço de Castração de Pets da SEPET** — Manaus/AM.

---

## 📋 Funcionalidades

- **Agendamento de Castração** — Formulário completo com dados do tutor, do pet e data de atendimento.
- **Triagem Clínica** — Questionário de 19 perguntas avaliando o estado de saúde do animal.
- **Análise de Risco com IA** — Agente inteligente (MiniMax AI) que analisa as respostas da triagem e emite um parecer técnico veterinário, identificando alertas de risco automaticamente.
- **Comprovante de Agendamento** — Geração de comprovante com todos os dados do agendamento e QR Code.
- **Painel de Gestão** — Visualização e gerenciamento dos agendamentos realizados.

---

## 🛠️ Tecnologias Utilizadas

| Camada      | Tecnologia                                                     |
| ----------- | -------------------------------------------------------------- |
| **Backend** | [Python 3.12](https://python.org) + [FastAPI](https://fastapi.tiangolo.com) |
| **Frontend** | [Vue 3](https://vuejs.org) + [Tailwind CSS 4](https://tailwindcss.com) + [Vite](https://vite.dev) |
| **Banco de Dados** | [Supabase](https://supabase.com) (PostgreSQL gerenciado)       |
| **IA / LLM** | [LangChain](https://python.langchain.com) + [MiniMax API](https://www.minimaxi.com) (via `ChatOpenAI`) |
| **HTTP Client** | [Axios](https://axios-http.com)                                |

---

## 🏗️ Arquitetura do Projeto

```
sepet_agent_project/
├── app/                        # Backend (FastAPI)
│   ├── agents/
│   │   └── clinical_analyst.py # 🤖 Agente de IA — Analista Clínico
│   ├── routes/
│   │   ├── agendamentos.py     # CRUD de agendamentos
│   │   ├── triagens.py         # Registro de triagens
│   │   ├── analise.py          # Disparo de análise por IA
│   │   └── comprovantes.py     # Geração de comprovantes
│   ├── services/
│   │   └── comprovante.py      # Lógica de geração de comprovante
│   ├── config.py               # Variáveis de ambiente
│   ├── database.py             # Conexão Supabase (singleton)
│   ├── dependencies.py         # Injeção de dependências
│   ├── models.py               # Modelos Pydantic
│   └── main.py                 # Entrypoint FastAPI
├── frontend/                   # Frontend (Vue 3)
│   ├── src/
│   │   ├── views/
│   │   │   ├── AgendamentoView.vue  # Página de agendamento
│   │   │   └── GestaoView.vue       # Painel de gestão
│   │   ├── components/
│   │   │   ├── InputField.vue       # Campo de entrada reutilizável
│   │   │   ├── SelectField.vue      # Campo de seleção reutilizável
│   │   │   ├── ToggleQuestion.vue   # Toggle para triagem
│   │   │   ├── TriagemForm.vue      # Formulário de triagem
│   │   │   └── TermoAutorizacao.vue # Termo de autorização
│   │   ├── services/
│   │   │   └── api.js          # Cliente HTTP (Axios)
│   │   ├── router/
│   │   │   └── index.js        # Rotas da aplicação
│   │   ├── App.vue             # Componente raiz
│   │   └── main.js             # Entrypoint Vue
│   └── package.json
├── .env.example                # Template de variáveis de ambiente
├── requirements.txt            # Dependências Python
└── README.md
```

---

## 🤖 Multi-Agente de IA — Analista Clínico

O sistema utiliza um **pipeline multi-agente** orquestrado por **LangChain** com 3 etapas sequenciais:

```
Dados da Triagem  →  🔍 Lupa (Analista)  →  ⚖️ Juiz (Verificador)  →  📝 Relator (Redator)  →  JSON final
```

| Agente | Papel | Responsabilidade |
|--------|-------|------------------|
| **Lupa** | Analista de Triagem | Extrai e organiza todos os dados clínicos do animal e as 19 respostas do questionário |
| **Juiz** | Verificador de Riscos | Analisa os dados extraídos e emite um veredito: ALTO RISCO ou BAIXO RISCO |
| **Relator** | Redator Clínico | Redige o parecer técnico final em formato JSON (`alerta_risco` + `parecer_ia`) |

Cada agente recebe a saída do anterior via `ChatOpenAI` (LangChain) conectado à **API MiniMax**.

**Critérios de Risco Automáticos:**
- Tutor não compreendeu o risco anestésico → 🔴 Alto Risco
- Desmaio, convulsão ou dificuldade respiratória → 🔴 Alto Risco
- Animal sem jejum de 12h → ⚠️ Risco (bloqueante)
- Animal com mais de 7 anos → ⚠️ Atenção especial

> Caso a API de IA esteja indisponível, o sistema utiliza uma **análise determinística de fallback** para garantir que nenhum risco passe despercebido.

---

## ⚙️ Pré-requisitos

- **Python** 3.12 ou superior (recomendado: 3.12)
- **Node.js** 18 ou superior
- **npm** 9 ou superior
- Conta no **Supabase** com as tabelas `agendamentos`, `triagens` e `tenants` criadas
- Chave de API da **MiniMax**

---

## 🚀 Como Configurar

### 1. Clone o repositório

```bash
git clone https://github.com/JoaoP29/sepet_agent_project.git
cd sepet_agent_project
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais reais:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key-aqui
MINIMAX_API_KEY=sua-api-key-minimax-aqui
```

### 3. Configure o Backend

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure o Frontend

```bash
cd frontend
npm install
cd ..
```

---

## ▶️ Como Executar

Abra **dois terminais** na raiz do projeto:

**Terminal 1 — Backend:**

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

O backend ficará disponível em: `http://localhost:8000`

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

O frontend ficará disponível em: `http://localhost:5173`

---

## 📡 Endpoints da API

| Método | Rota                        | Descrição                          |
| ------ | --------------------------- | ---------------------------------- |
| `GET`  | `/`                         | Health check                       |
| `POST` | `/agendamentos/`            | Criar novo agendamento             |
| `GET`  | `/agendamentos/`            | Listar agendamentos                |
| `GET`  | `/agendamentos/{id}`        | Obter agendamento por ID           |
| `GET`  | `/triagens/`                | Listar triagens                    |
| `GET`  | `/triagens/{agendamento_id}`| Obter triagem por agendamento      |
| `POST` | `/analise/{triagem_id}`     | Disparar análise de risco por IA   |
| `GET`  | `/comprovantes/{agendamento_id}` | Gerar comprovante de agendamento |

A documentação Swagger interativa está disponível em: `http://localhost:8000/docs`

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.