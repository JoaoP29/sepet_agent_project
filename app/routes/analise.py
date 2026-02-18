import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_supabase
from app.dependencies import get_tenant_id
from app.agents.clinical_analyst import analisar_triagem

logger = logging.getLogger("sepet.analise")

router = APIRouter(prefix="/analise", tags=["Análise IA"])


@router.post("/{triagem_id}")
async def executar_analise(
    triagem_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """
    Dispara a análise de risco por IA para uma triagem específica.
    Atualiza os campos `alerta_risco` e `parecer_ia` na tabela `triagens`.
    """
    db = get_supabase()

    # 1) Buscar a triagem
    try:
        result = (
            db.table("triagens")
            .select("*")
            .eq("id", triagem_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result.data:
        raise HTTPException(status_code=404, detail="Triagem não encontrada.")

    triagem = result.data[0]
    respostas = triagem.get("respostas_triagem", {})
    agendamento_id = triagem.get("agendamento_id")

    # 2) Buscar dados do pet (agendamento) — usa colunas reais do banco
    pet_info = {}
    meta_pet = respostas.get("_meta_pet", {})

    if agendamento_id:
        try:
            ag_result = (
                db.table("agendamentos")
                .select("*")
                .eq("id", agendamento_id)
                .eq("tenant_id", tenant_id)
                .execute()
            )
            if ag_result.data:
                ag = ag_result.data[0]
                pet_info = {
                    "pet_nome": ag.get("nome_animal", ""),
                    "pet_especie": ag.get("especie", ""),
                    "pet_raca": ag.get("raca", ""),
                    "pet_porte": ag.get("porte", ""),
                    "pet_idade_anos": meta_pet.get("idade_anos", 0),
                    "pet_idade_meses": meta_pet.get("idade_meses", 0),
                    "pet_sexo": meta_pet.get("sexo", ""),
                    "pet_peso_kg": meta_pet.get("peso_kg", 0),
                }
        except Exception as e:
            logger.warning(f"Erro ao buscar dados do pet: {e}")

    # 3) Executar análise
    logger.info(f"Iniciando análise de risco para triagem {triagem_id}")
    resultado = analisar_triagem(respostas, pet_info)

    # 4) Atualizar a triagem no banco
    try:
        db.table("triagens").update({
            "alerta_risco": resultado["alerta_risco"],
            "parecer_ia": resultado["parecer_ia"],
        }).eq("id", triagem_id).execute()
    except Exception as e:
        logger.error(f"Erro ao atualizar triagem: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar parecer: {e}")

    logger.info(
        f"Análise concluída para triagem {triagem_id}: "
        f"alerta_risco={resultado['alerta_risco']}"
    )

    return {
        "triagem_id": triagem_id,
        "alerta_risco": resultado["alerta_risco"],
        "parecer_ia": resultado["parecer_ia"],
        "status": "analise_concluida",
    }
