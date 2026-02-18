import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.database import get_supabase
from app.dependencies import get_tenant_id
from app.services.comprovante import gerar_comprovante_html, gerar_comprovante_json

logger = logging.getLogger("sepet.comprovantes")

router = APIRouter(prefix="/comprovantes", tags=["Comprovantes"])


@router.get("/{agendamento_id}", response_class=HTMLResponse)
async def gerar_comprovante(
    agendamento_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """
    Gera o comprovante de agendamento em formato HTML.
    Inclui dados do animal, tutor, parecer IA e contatos oficiais.
    """
    db = get_supabase()

    # Buscar agendamento
    try:
        ag_result = (
            db.table("agendamentos")
            .select("*")
            .eq("id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not ag_result.data:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    agendamento = ag_result.data[0]

    # Buscar triagem (pode não existir ainda)
    triagem = None
    try:
        tr_result = (
            db.table("triagens")
            .select("*")
            .eq("agendamento_id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
        if tr_result.data:
            triagem = tr_result.data[0]
    except Exception as e:
        logger.warning(f"Erro ao buscar triagem: {e}")

    html = gerar_comprovante_html(agendamento, triagem)
    return HTMLResponse(content=html)


@router.get("/{agendamento_id}/json")
async def gerar_comprovante_dados(
    agendamento_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """
    Retorna os dados do comprovante em formato JSON.
    """
    db = get_supabase()

    try:
        ag_result = (
            db.table("agendamentos")
            .select("*")
            .eq("id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not ag_result.data:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    agendamento = ag_result.data[0]

    triagem = None
    try:
        tr_result = (
            db.table("triagens")
            .select("*")
            .eq("agendamento_id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
        if tr_result.data:
            triagem = tr_result.data[0]
    except Exception as e:
        logger.warning(f"Erro ao buscar triagem: {e}")

    return gerar_comprovante_json(agendamento, triagem)
