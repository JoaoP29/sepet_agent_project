"""
Agente Analista Clínico — SEPET  (Multi-Agent com CrewAI)
Orquestra 3 agentes sequenciais para analisar triagem veterinária:
  1. Lupa   – Analista de Triagem (extrai e organiza dados)
  2. Juiz   – Verificador de Riscos (emite alerta_risco)
  3. Relator – Redator Clínico (gera parecer humanizado)

Usa MiniMax como LLM via OpenAICompletion (compatível OpenAI).
"""
import json
import logging
from crewai import Agent, Task, Crew, Process
from crewai.llms.providers.openai.completion import OpenAICompletion
from app.config import MINIMAX_API_KEY

logger = logging.getLogger("sepet.agente_clinico")


# ── Adaptador MiniMax ────────────────────────
class MiniMaxCompletion(OpenAICompletion):
    """MiniMax rejeita role='system' (erro 2013).
    Converte system → user com prefixo 'System:'.
    """

    def _format_messages(self, messages):
        formatted = super()._format_messages(messages)
        result = []
        for msg in formatted:
            if msg.get("role") == "system":
                result.append(
                    {"role": "user", "content": f"System: {msg['content']}"}
                )
            else:
                result.append(msg)
        return result


# ── LLM MiniMax (via OpenAI-compatible provider) ─
minimax_llm = MiniMaxCompletion(
    model="MiniMax-Text-01",
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimaxi.chat/v1",
    temperature=0.3,
    max_tokens=1000,
)


# ── Agentes ──────────────────────────────────

def _criar_agente_lupa() -> Agent:
    """Agente 1 — Analista de Triagem ('Lupa')."""
    return Agent(
        role="Analista de Triagem Veterinária",
        goal=(
            "Extrair, organizar e apresentar de forma clara TODOS os dados "
            "do animal e as 19 respostas do questionário de triagem clínica, "
            "garantindo que nenhuma informação vital seja omitida."
        ),
        backstory=(
            "Você é um especialista em coleta e organização de dados "
            "veterinários do SEPET (Serviço de Esterilização de Pets). "
            "Sua missão é garantir que todas as informações clínicas "
            "estejam corretamente catalogadas antes da análise de risco."
        ),
        llm=minimax_llm,
        verbose=True,
    )


def _criar_agente_juiz() -> Agent:
    """Agente 2 — Verificador de Riscos ('Juiz')."""
    return Agent(
        role="Auditor de Segurança Cirúrgica Veterinária",
        goal=(
            "Analisar os dados extraídos pelo Analista de Triagem e "
            "identificar TODOS os pontos críticos de risco, emitindo "
            "um veredito claro: ALTO RISCO (true) ou BAIXO RISCO (false)."
        ),
        backstory=(
            "Você é um auditor rigoroso de segurança cirúrgica veterinária. "
            "Sua experiência inclui anos avaliando casos pré-operatórios. "
            "Você segue regras estritas:\n"
            "- Se 'entendeu_risco_anestesico' = false → ALTO RISCO\n"
            "- Se há desmaio, convulsão ou dificuldade respiratória → ALTO RISCO\n"
            "- Se 'jejum_12h' = false → RISCO (não pode prosseguir)\n"
            "- Animais com 7+ anos merecem atenção especial (geriátricos)"
        ),
        llm=minimax_llm,
        verbose=True,
    )


def _criar_agente_relator() -> Agent:
    """Agente 3 — Redator Clínico ('Relator')."""
    return Agent(
        role="Redator Médico Veterinário",
        goal=(
            "Consolidar a análise dos agentes anteriores e redigir um "
            "parecer técnico profissional e humanizado sobre o animal. "
            "O parecer deve ser claro, objetivo e adequado para um "
            "documento oficial do SEPET."
        ),
        backstory=(
            "Você é um redator médico veterinário experiente. "
            "Sua função é transformar análises técnicas em pareceres "
            "claros e acessíveis, mencionando idade do animal, riscos "
            "identificados e recomendações específicas."
        ),
        llm=minimax_llm,
        verbose=True,
    )


# ── Função principal ─────────────────────────

def analisar_triagem(respostas_triagem: dict, pet_info: dict) -> dict:
    """
    Analisa o questionário de triagem usando 3 agentes CrewAI em sequência.

    Args:
        respostas_triagem: dict com as 19 respostas do questionário
        pet_info: dict com informações do pet (nome, espécie, raça, idade, porte, peso)

    Returns:
        dict com { alerta_risco: bool, parecer_ia: str }
    """
    # Montar contexto para os agentes
    contexto = f"""
Dados do Animal:
- Nome: {pet_info.get('pet_nome', 'N/A')}
- Espécie: {pet_info.get('pet_especie', 'N/A')}
- Raça: {pet_info.get('pet_raca', 'N/A')}
- Porte: {pet_info.get('pet_porte', 'N/A')}
- Idade: {pet_info.get('pet_idade_anos', 0)} ano(s) e {pet_info.get('pet_idade_meses', 0)} mese(s)
- Peso: {pet_info.get('pet_peso_kg', 0)} kg
- Sexo: {pet_info.get('pet_sexo', 'N/A')}

Respostas do Questionário de Triagem:
{json.dumps(respostas_triagem, indent=2, ensure_ascii=False)}
"""

    # ── Task 1: Lupa extrai e organiza ──
    task_lupa = Task(
        description=(
            f"Analise os seguintes dados clínicos de um animal agendado "
            f"para castração no SEPET. Extraia e organize TODAS as "
            f"informações relevantes, calculando a idade exata e "
            f"destacando quaisquer dados que mereçam atenção.\n\n{contexto}"
        ),
        expected_output=(
            "Um relatório organizado contendo: dados completos do animal "
            "(nome, espécie, raça, porte, peso, sexo, idade exata), "
            "e todas as 19 respostas do questionário claramente listadas "
            "com destaque para respostas positivas (sinais clínicos)."
        ),
        agent=_criar_agente_lupa(),
    )

    # ── Task 2: Juiz verifica riscos ──
    task_juiz = Task(
        description=(
            "Com base no relatório do Analista de Triagem, analise "
            "TODOS os pontos críticos de segurança cirúrgica:\n"
            "1. O tutor compreendeu o risco anestésico?\n"
            "2. O animal está em jejum de 12h?\n"
            "3. Há histórico de desmaio, convulsão ou dificuldade respiratória?\n"
            "4. O animal é geriátrico (7+ anos)?\n"
            "5. Há uso de medicação que pode interferir?\n\n"
            "Emita seu veredito final: o campo 'alerta_risco' deve ser "
            "'true' se QUALQUER risco crítico foi identificado, ou "
            "'false' se nenhum risco significativo foi encontrado.\n\n"
            "Responda OBRIGATORIAMENTE com o veredito no formato:\n"
            "VEREDITO: ALTO RISCO ou VEREDITO: BAIXO RISCO\n"
            "Seguido da lista de riscos identificados."
        ),
        expected_output=(
            "Um veredito claro (ALTO RISCO ou BAIXO RISCO) seguido da "
            "lista detalhada de todos os riscos identificados, com "
            "justificativa para cada um."
        ),
        agent=_criar_agente_juiz(),
    )

    # ── Task 3: Relator redige parecer ──
    task_relator = Task(
        description=(
            "Com base no relatório do Analista de Triagem e no veredito "
            "do Auditor de Riscos, redija o parecer técnico final.\n\n"
            "O parecer deve:\n"
            "- Mencionar o nome e a idade exata do animal\n"
            "- Listar os riscos identificados (se houver)\n"
            "- Indicar se o animal é geriátrico\n"
            "- Incluir recomendação final\n\n"
            "Responda OBRIGATORIAMENTE no seguinte formato JSON:\n"
            '{"alerta_risco": true/false, "parecer_ia": "Texto do parecer"}\n\n'
            "Onde 'alerta_risco' reflete o veredito do Auditor e "
            "'parecer_ia' contém o parecer profissional completo."
        ),
        expected_output=(
            'JSON com a estrutura: {"alerta_risco": bool, "parecer_ia": "texto"}. '
            "O parecer deve ser profissional, humanizado e adequado para "
            "um documento oficial do SEPET."
        ),
        agent=_criar_agente_relator(),
    )

    try:
        # ── Executar Crew sequencial ──
        logger.info(
            f"Iniciando análise multi-agente para "
            f"{pet_info.get('pet_nome', 'N/A')}..."
        )

        crew = Crew(
            agents=[task_lupa.agent, task_juiz.agent, task_relator.agent],
            tasks=[task_lupa, task_juiz, task_relator],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        raw_output = result.raw if hasattr(result, 'raw') else str(result)

        logger.info(f"Crew finalizada. Output bruto: {raw_output[:200]}...")

        # Tentar extrair JSON da resposta do Relator
        resultado = _extrair_json(raw_output)

        logger.info(
            f"Parecer gerado para {pet_info.get('pet_nome', 'N/A')}: "
            f"alerta_risco={resultado.get('alerta_risco', False)}"
        )

        return {
            "alerta_risco": resultado.get("alerta_risco", False),
            "parecer_ia": resultado.get("parecer_ia", "Parecer não disponível."),
        }

    except Exception as e:
        logger.error(f"Erro ao gerar parecer IA (CrewAI): {e}")
        # Fallback: análise determinística simples
        return _analise_fallback(respostas_triagem, pet_info)


# ── Helpers ───────────────────────────────────

def _extrair_json(texto: str) -> dict:
    """Tenta extrair um objeto JSON de um texto que pode conter markdown."""
    # Tenta parse direto
    try:
        return json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        pass

    # Procura JSON dentro de blocos ```json ... ``` ou { ... }
    import re
    # Tenta encontrar bloco ```json
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Tenta encontrar qualquer { ... } com alerta_risco
    match = re.search(r'\{[^{}]*"alerta_risco"[^{}]*\}', texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback: inferir do texto
    alerta = "ALTO RISCO" in texto.upper()
    return {
        "alerta_risco": alerta,
        "parecer_ia": texto.strip(),
    }


def _analise_fallback(respostas: dict, pet_info: dict) -> dict:
    """Análise de risco determinística (fallback se a IA falhar)."""
    riscos = []
    alerta = False

    if not respostas.get("entendeu_risco_anestesico", False):
        riscos.append("Tutor NÃO compreendeu o risco anestésico")
        alerta = True

    if not respostas.get("jejum_12h", False):
        riscos.append("Animal NÃO está em jejum de 12h")
        alerta = True

    for campo in ["desmaio", "convulsao", "dificuldade_respirar"]:
        if respostas.get(campo, False):
            riscos.append(f"Sinal grave detectado: {campo.replace('_', ' ')}")
            alerta = True

    idade_anos = pet_info.get("pet_idade_anos", 0)
    idade_meses = pet_info.get("pet_idade_meses", 0)
    nome = pet_info.get("pet_nome", "Animal")

    if idade_anos >= 7:
        riscos.append(
            f"Animal geriátrico ({idade_anos} ano(s) e {idade_meses} mese(s)), requer atenção especial"
        )

    if riscos:
        parecer = (
            f"Animal {nome} com {idade_anos} ano(s) e {idade_meses} mese(s). "
            f"Riscos identificados: {'; '.join(riscos)}. "
            f"Recomenda-se avaliação veterinária detalhada antes do procedimento."
        )
    else:
        parecer = (
            f"Animal {nome} com {idade_anos} ano(s) e {idade_meses} mese(s). "
            f"Nenhum risco significativo identificado na triagem. "
            f"Apto para o procedimento, sujeito a avaliação presencial."
        )

    return {"alerta_risco": alerta, "parecer_ia": parecer}
