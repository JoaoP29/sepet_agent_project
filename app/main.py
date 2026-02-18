import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import SEPET_ENDERECO
from app.routes import agendamentos, triagens, analise, comprovantes

# ── Logging ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("sepet")


# ── Lifespan ─────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🐾 SEPET Backend iniciado | {SEPET_ENDERECO}")
    yield
    logger.info("🐾 SEPET Backend encerrado")


# ── App ──────────────────────────────────────
app = FastAPI(
    title="SEPET – Sistema de Esterilização de Pets",
    description=(
        "API para agendamento de esterilização, triagem clínica e "
        "análise de risco com IA. "
        f"Endereço: {SEPET_ENDERECO}"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware de log ────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    tenant = request.headers.get("X-Tenant-ID", "sem-tenant")
    logger.info(
        f"➡ {request.method} {request.url.path} | Tenant: {tenant} | "
        f"Local: {SEPET_ENDERECO}"
    )
    response = await call_next(request)
    return response


# ── Rotas ────────────────────────────────────
app.include_router(agendamentos.router)
app.include_router(triagens.router)
app.include_router(analise.router)
app.include_router(comprovantes.router)


# ── Health check ─────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "servico": "SEPET – Sistema de Esterilização de Pets",
        "endereco": SEPET_ENDERECO,
    }
