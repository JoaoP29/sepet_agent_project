"""
Agente Analista Clínico — SEPET  (Multi-Agent com LangChain)
Orquestra 3 etapas sequenciais para analisar triagem veterinária:
  1. Lupa   – Analista de Triagem (extrai e organiza dados)
  2. Juiz   – Verificador de Riscos (emite alerta_risco)
  3. Relator – Redator Clínico (gera parecer humanizado)

Usa MiniMax-Text-01 como LLM via ChatOpenAI (compatível OpenAI).
"""
import json
import logging
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import MINIMAX_API_KEY

logger = logging.getLogger("sepet.agente_clinico")

# ── LLM MiniMax ──────────────────────────────
llm = ChatOpenAI(
    model="MiniMax-Text-01",
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimaxi.chat/v1",
    temperature=0.3,
    max_tokens=1000,
)


# ── Prompts dos agentes ──────────────────────

PROMPT_LUPA = (
    "Você é o Analista de Triagem Veterinária do SEPET "
    "(Serviço de Esterilização de Pets). "
    "Sua missão é extrair e organizar TODOS os dados clínicos "
    "do animal e as respostas do questionário de triagem, "
    "garantindo que nenhuma informação vital seja omitida.\n\n"
    "Apresente um relatório organizado com:\n"
    "- Dados completos do animal (nome, espécie, raça, porte, peso, sexo, idade exata)\n"
    "- Todas as respostas do questionário listadas\n"
    "- Destaque para respostas positivas (sinais clínicos)\n"
)

PROMPT_JUIZ = (
    "Você é o Auditor de Segurança Cirúrgica Veterinária do SEPET. "
    "Com base no relatório abaixo, analise TODOS os pontos críticos:\n\n"
    "Regras obrigatórias:\n"
    "- Se 'entendeu_risco_anestesico' = false → ALTO RISCO\n"
    "- Se há desmaio, convulsão ou dificuldade respiratória → ALTO RISCO\n"
    "- Se 'jejum_12h' = false → ALTO RISCO (não pode prosseguir)\n"
    "- Animais com 7+ anos → atenção especial (geriátricos)\n"
    "- Uso de medicação que pode interferir → risco adicional\n\n"
    "Responda com:\n"
    "VEREDITO: ALTO RISCO ou VEREDITO: BAIXO RISCO\n"
    "Seguido da lista de riscos identificados com justificativas."
)

PROMPT_RELATOR = (
    "Você é o Redator Médico Veterinário do SEPET. "
    "Com base no relatório e no veredito abaixo, redija o parecer técnico final.\n\n"
    "O parecer deve:\n"
    "- Mencionar o nome e a idade exata do animal\n"
    "- Listar os riscos identificados (se houver)\n"
    "- Indicar se o animal é geriátrico\n"
    "- Incluir recomendação final\n\n"
    "Responda OBRIGATORIAMENTE no seguinte formato JSON "
    "(sem texto fora do JSON):\n"
    '{"alerta_risco": true ou false, "parecer_ia": "Texto do parecer"}\n\n'
    "Onde 'alerta_risco' reflete o veredito do Auditor."
)


# ── Função principal ─────────────────────────

def analisar_triagem(respostas_triagem: dict, pet_info: dict) -> dict:
    """
    Analisa o questionário de triagem usando 3 etapas sequenciais com LangChain.

    Args:
        respostas_triagem: dict com as respostas do questionário
        pet_info: dict com informações do pet (nome, espécie, raça, idade, porte, peso)

    Returns:
        dict com { alerta_risco: bool, parecer_ia: str }
    """
    contexto = _montar_contexto(respostas_triagem, pet_info)
    nome = pet_info.get("pet_nome", "N/A")

    try:
        logger.info(f"Iniciando análise multi-agente LangChain para {nome}...")

        # ── Etapa 1: Lupa extrai e organiza ──
        logger.info("[Lupa] Extraindo dados...")
        resp_lupa = llm.invoke([
            SystemMessage(content=PROMPT_LUPA),
            HumanMessage(content=contexto),
        ])
        saida_lupa = resp_lupa.content
        logger.info(f"[Lupa] Concluído ({len(saida_lupa)} chars)")

        # ── Etapa 2: Juiz verifica riscos ──
        logger.info("[Juiz] Verificando riscos...")
        resp_juiz = llm.invoke([
            SystemMessage(content=PROMPT_JUIZ),
            HumanMessage(content=f"RELATÓRIO DO ANALISTA:\n\n{saida_lupa}"),
        ])
        saida_juiz = resp_juiz.content
        logger.info(f"[Juiz] Concluído ({len(saida_juiz)} chars)")

        # ── Etapa 3: Relator redige parecer ──
        logger.info("[Relator] Redigindo parecer...")
        resp_relator = llm.invoke([
            SystemMessage(content=PROMPT_RELATOR),
            HumanMessage(
                content=(
                    f"RELATÓRIO DO ANALISTA:\n\n{saida_lupa}\n\n"
                    f"VEREDITO DO AUDITOR:\n\n{saida_juiz}"
                )
            ),
        ])
        saida_relator = resp_relator.content
        logger.info(f"[Relator] Concluído ({len(saida_relator)} chars)")

        # Extrair JSON da resposta do Relator
        resultado = _extrair_json(saida_relator)

        logger.info(
            f"Parecer IA gerado para {nome}: "
            f"alerta_risco={resultado.get('alerta_risco', False)}"
        )

        return {
            "alerta_risco": resultado.get("alerta_risco", False),
            "parecer_ia": resultado.get("parecer_ia", "Parecer não disponível."),
        }

    except Exception as e:
        logger.error(f"Erro ao gerar parecer IA (LangChain): {e}")
        return _analise_fallback(respostas_triagem, pet_info)


# ── Helpers ───────────────────────────────────

def _montar_contexto(respostas: dict, pet_info: dict) -> str:
    """Monta o texto de contexto para os agentes."""
    return (
        f"Dados do Animal:\n"
        f"- Nome: {pet_info.get('pet_nome', 'N/A')}\n"
        f"- Espécie: {pet_info.get('pet_especie', 'N/A')}\n"
        f"- Raça: {pet_info.get('pet_raca', 'N/A')}\n"
        f"- Porte: {pet_info.get('pet_porte', 'N/A')}\n"
        f"- Idade: {pet_info.get('pet_idade_anos', 0)} ano(s) e "
        f"{pet_info.get('pet_idade_meses', 0)} mese(s)\n"
        f"- Peso: {pet_info.get('pet_peso_kg', 0)} kg\n"
        f"- Sexo: {pet_info.get('pet_sexo', 'N/A')}\n\n"
        f"Respostas do Questionário de Triagem:\n"
        f"{json.dumps(respostas, indent=2, ensure_ascii=False)}"
    )


def _extrair_json(texto: str) -> dict:
    """Tenta extrair um objeto JSON de um texto que pode conter markdown."""
    try:
        return json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        pass

    # Bloco ```json ... ```
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Qualquer { ... } com alerta_risco
    match = re.search(r'\{[^{}]*"alerta_risco"[^{}]*\}', texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Inferir do texto
    alerta = "ALTO RISCO" in texto.upper()
    return {"alerta_risco": alerta, "parecer_ia": texto.strip()}


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
            f"Animal geriátrico ({idade_anos} ano(s) e {idade_meses} mese(s)), "
            f"requer atenção especial"
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
