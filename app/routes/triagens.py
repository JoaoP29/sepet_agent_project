import logging
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_supabase
from app.dependencies import get_tenant_id
from app.models import TriagemResponse

logger = logging.getLogger("sepet.triagens")

router = APIRouter(prefix="/triagens", tags=["Triagens"])


@router.get("/", response_model=list[TriagemResponse])
async def listar_triagens(tenant_id: str = Depends(get_tenant_id)):
    """Lista todas as triagens do tenant."""
    db = get_supabase()
    try:
        result = (
            db.table("triagens")
            .select("*")
            .eq("tenant_id", tenant_id)
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as e:
        logger.error(f"Erro ao listar triagens: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return [TriagemResponse(**row) for row in result.data]


@router.get("/{agendamento_id}", response_model=TriagemResponse)
async def obter_triagem(
    agendamento_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """Retorna a triagem associada a um agendamento específico."""
    db = get_supabase()
    try:
        result = (
            db.table("triagens")
            .select("*")
            .eq("agendamento_id", agendamento_id)
            .eq("tenant_id", tenant_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not result.data:
        raise HTTPException(status_code=404, detail="Triagem não encontrada.")

    return TriagemResponse(**result.data[0])
