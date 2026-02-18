"""
Agente Analista Clínico — SEPET
Analisa o questionário de triagem e gera parecer com alerta de risco.
Usa a API MiniMax (compatível com OpenAI) via SDK openai.
"""
import json
import logging
from openai import OpenAI
from app.config import MINIMAX_API_KEY

logger = logging.getLogger("sepet.agente_clinico")

# MiniMax API é compatível com o endpoint OpenAI
client = OpenAI(
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimaxi.chat/v1",
)

SYSTEM_PROMPT = """Você é um agente veterinário analista clínico do SEPET (Serviço de Esterilização de Pets).
Sua missão é analisar o questionário de triagem clínica de um animal e emitir um parecer técnico.

Regras:
1. Identifique TODOS os sinais de risco baseando-se nas respostas do questionário.
2. Se o tutor respondeu 'Não' para "Entendeu o risco anestésico?" (entendeu_risco_anestesico = false), marque como ALTO RISCO.
3. Se o animal apresenta desmaio, convulsão ou dificuldade respiratória, marque como ALTO RISCO.
4. Se o animal NÃO está em jejum de 12h (jejum_12h = false), marque como RISCO — não pode prosseguir sem jejum.
5. Calcule a idade exata do animal (ex: "13 anos e 6 meses") e mencione no parecer se for relevante (animais com mais de 7 anos merecem atenção especial).
6. Redija um parecer claro, objetivo e profissional.

Responda SEMPRE em formato JSON com esta estrutura:
{
  "alerta_risco": true/false,
  "parecer_ia": "Texto do parecer técnico completo"
}
"""


def analisar_triagem(respostas_triagem: dict, pet_info: dict) -> dict:
    """
    Analisa o questionário de triagem e retorna alerta_risco + parecer_ia.

    Args:
        respostas_triagem: dict com as 19 respostas do questionário
        pet_info: dict com informações do pet (nome, espécie, raça, idade, porte, peso)

    Returns:
        dict com { alerta_risco: bool, parecer_ia: str }
    """
    prompt_usuario = f"""
Analise a triagem clínica do seguinte animal:

**Dados do Animal:**
- Nome: {pet_info.get('pet_nome', 'N/A')}
- Espécie: {pet_info.get('pet_especie', 'N/A')}
- Raça: {pet_info.get('pet_raca', 'N/A')}
- Porte: {pet_info.get('pet_porte', 'N/A')}
- Idade: {pet_info.get('pet_idade_anos', 0)} ano(s) e {pet_info.get('pet_idade_meses', 0)} mese(s)
- Peso: {pet_info.get('pet_peso_kg', 0)} kg
- Sexo: {pet_info.get('pet_sexo', 'N/A')}

**Respostas do Questionário de Triagem:**
{json.dumps(respostas_triagem, indent=2, ensure_ascii=False)}

Emita o parecer técnico em formato JSON.
"""

    try:
        response = client.chat.completions.create(
            model="MiniMax-Text-01",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_usuario},
            ],
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        resultado = json.loads(content)

        logger.info(
            f"Parecer gerado para {pet_info.get('pet_nome', 'N/A')}: "
            f"alerta_risco={resultado.get('alerta_risco', False)}"
        )

        return {
            "alerta_risco": resultado.get("alerta_risco", False),
            "parecer_ia": resultado.get("parecer_ia", "Parecer não disponível."),
        }

    except Exception as e:
        logger.error(f"Erro ao gerar parecer IA: {e}")

        # Fallback: análise determinística simples
        return _analise_fallback(respostas_triagem, pet_info)


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
