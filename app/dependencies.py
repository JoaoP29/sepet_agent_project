from fastapi import Header, HTTPException


async def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    """Extrai e valida o header X-Tenant-ID para isolamento multitenancy."""
    if not x_tenant_id or not x_tenant_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Header X-Tenant-ID é obrigatório e não pode estar vazio.",
        )
    return x_tenant_id.strip()
