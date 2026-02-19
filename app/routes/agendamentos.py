import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_supabase
from app.dependencies import get_tenant_id
from app.models import AgendamentoCreate, AgendamentoResponse
from app.config import SEPET_ENDERECO
from app.agents.clinical_analyst import analisar_triagem

logger = logging.getLogger("sepet.agendamentos")

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.post("/", response_model=AgendamentoResponse, status_code=201)
async def criar_agendamento(
    dados: AgendamentoCreate,
    tenant_id: str = Depends(get_tenant_id),
):
    """
    Cria um novo agendamento com os dados do tutor, do pet e da triagem clínica.
    Salva os dados básicos em `agendamentos` e o questionário em `triagens`.
    Dispara automaticamente a análise de risco por IA.
    """
    db = get_supabase()

    # 1) Inserir na tabela agendamentos (SOMENTE colunas que existem no banco)
    agendamento_payload = {
        "tenant_id": tenant_id,
        "nome_tutor": dados.nome_tutor,
        "cpf_tutor": dados.cpf_tutor,
        "nome_animal": dados.nome_animal,
        "especie": dados.especie,
        "raca": dados.raca,
        "porte": dados.porte,
        "data_atendimento": dados.data_atendimento.isoformat(),
        "status_ia": "Pendente",
    }

    try:
        result = (
            db.table("agendamentos").insert(agendamento_payload).execute()
        )
    except Exception as e:
        logger.error(f"Erro ao inserir agendamento: {e} | Local: {SEPET_ENDERECO}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar agendamento: {e}")

    agendamento = result.data[0]
    agendamento_id = agendamento["id"]

    logger.info(
        f"Agendamento {agendamento_id} criado para tenant {tenant_id} | "
        f"Pet: {dados.nome_animal} | Local: {SEPET_ENDERECO}"
    )

    # 2) Montar respostas da triagem como JSON
    #    Inclui as respostas clínicas + dados extras do pet/tutor que não
    #    cabem na tabela agendamentos
    respostas = dados.triagem.model_dump()
    respostas["_meta_pet"] = {
        "idade_anos": dados.idade_anos,
        "idade_meses": dados.idade_meses,
        "sexo": dados.sexo,
        "peso_kg": dados.peso_kg,
    }
    respostas["_meta_tutor"] = {
        "telefone": dados.telefone_tutor,
        "email": dados.email_tutor,
    }

    triagem_payload = {
        "agendamento_id": agendamento_id,
        "tenant_id": tenant_id,
        "respostas_triagem": respostas,
        "alerta_risco": False,
        "parecer_ia": None,
    }

    try:
        triagem_result = (
            db.table("triagens").insert(triagem_payload).execute()
        )
    except Exception as e:
        logger.error(f"Erro ao inserir triagem: {e} | Local: {SEPET_ENDERECO}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar triagem: {e}")

    triagem_id = triagem_result.data[0]["id"]

    logger.info(
        f"Triagem {triagem_id} salva para agendamento {agendamento_id} | Local: {SEPET_ENDERECO}"
    )

    # 3) Disparar análise de risco por IA automaticamente
    pet_info = {
        "pet_nome": dados.nome_animal,
        "pet_especie": dados.especie,
        "pet_raca": dados.raca,
        "pet_porte": dados.porte,
        "pet_idade_anos": dados.idade_anos,
        "pet_idade_meses": dados.idade_meses,
        "pet_sexo": dados.sexo,
        "pet_peso_kg": dados.peso_kg,
    }

    try:
        logger.info(f"Iniciando análise IA para triagem {triagem_id}...")
        resultado_ia = analisar_triagem(respostas, pet_info)

        # Atualizar triagem com o parecer da IA
        db.table("triagens").update({
            "alerta_risco": resultado_ia["alerta_risco"],
            "parecer_ia": resultado_ia["parecer_ia"],
        }).eq("id", triagem_id).execute()

        # Atualizar status_ia do agendamento
        db.table("agendamentos").update({
            "status_ia": "Analisado",
        }).eq("id", agendamento_id).execute()

        agendamento["status_ia"] = "Analisado"

        logger.info(
            f"Análise IA concluída para triagem {triagem_id}: "
            f"alerta_risco={resultado_ia['alerta_risco']} | Local: {SEPET_ENDERECO}"
        )
    except Exception as e:
        logger.error(
            f"Erro na análise IA para triagem {triagem_id}: {e} | "
            f"O agendamento foi salvo, mas o parecer ficará pendente."
        )

    return AgendamentoResponse(**agendamento)


@router.get("/", response_model=list[AgendamentoResponse])
async def listar_agendamentos(tenant_id: str = Depends(get_tenant_id)):
    """Lista todos os agendamentos filtrados pelo tenant."""
    db = get_supabase()
    try:
        result = (
            db.table("agendamentos")
            .select("*")
            .eq("tenant_id", tenant_id)
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as e:
        logger.error(f"Erro ao listar agendamentos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return [AgendamentoResponse(**row) for row in result.data]


@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
async def obter_agendamento(
    agendamento_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """Retorna um agendamento específico pelo ID, respeitando o tenant."""
    db = get_supabase()
    try:
        result = (
            db.table("agendamentos")
            .select("*")
            .eq("id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result.data:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    return AgendamentoResponse(**result.data[0])
