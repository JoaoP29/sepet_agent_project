import os
from dotenv import load_dotenv

load_dotenv()

# ----- Supabase -----
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

# ----- MiniMax / LLM -----
MINIMAX_API_KEY: str = os.getenv("MINIMAX_API_KEY", "")

# ----- Constantes do SEPET -----
SEPET_ENDERECO = "Av. Umberto Calderaro, 934 – Adrianópolis, Manaus-AM"
SEPET_EMAIL = "agendamento@sepet.am.gov.br"
SEPET_TELEFONE = "(92) 99207-1671"
