from __future__ import annotations
from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Modelos de Triagem (questionário clínico)
# ──────────────────────────────────────────────
class TriagemCreate(BaseModel):
    """Respostas do questionário clínico (19 perguntas)."""
    tosse: bool = Field(False, description="Animal apresenta tosse?")
    espirro: bool = Field(False, description="Animal apresenta espirro?")
    vomito: bool = Field(False, description="Animal apresenta vômito?")
    diarreia: bool = Field(False, description="Animal apresenta diarreia?")
    perda_apetite: bool = Field(False, description="Perda de apetite?")
    perda_peso: bool = Field(False, description="Perda de peso?")
    apatia: bool = Field(False, description="Animal está apático?")
    desmaio: bool = Field(False, description="Animal já desmaiou?")
    convulsao: bool = Field(False, description="Animal já teve convulsão?")
    dificuldade_respirar: bool = Field(False, description="Dificuldade para respirar?")
    secrecao_nasal: bool = Field(False, description="Secreção nasal?")
    secrecao_ocular: bool = Field(False, description="Secreção ocular?")
    lesoes_pele: bool = Field(False, description="Lesões de pele?")
    alergias: bool = Field(False, description="Animal tem alergias conhecidas?")
    cirurgia_anterior: bool = Field(False, description="Já fez cirurgia anterior?")
    medicacao_uso: bool = Field(False, description="Está em uso de medicação?")
    vacinas_em_dia: bool = Field(False, description="Vacinas estão em dia?")
    jejum_12h: bool = Field(False, description="Está em jejum de 12 horas?")
    entendeu_risco_anestesico: bool = Field(
        False, description="Tutor entendeu o risco anestésico?"
    )
    observacoes: str = Field("", description="Observações adicionais do tutor")


class TriagemResponse(BaseModel):
    id: str | None = None
    agendamento_id: str | None = None
    respostas_triagem: dict[str, Any] = {}
    alerta_risco: bool = False
    parecer_ia: str | None = None
    created_at: str | None = None


# ──────────────────────────────────────────────
# Modelos de Agendamento
# ──────────────────────────────────────────────
class AgendamentoCreate(BaseModel):
    """Dados para criação de um novo agendamento."""
    # Tutor
    nome_tutor: str = Field(..., min_length=2, description="Nome completo do tutor")
    cpf_tutor: str = Field("", description="CPF do tutor")
    telefone_tutor: str = Field("", description="Telefone do tutor")
    email_tutor: str = Field("", description="E-mail do tutor")

    # Pet
    nome_animal: str = Field(..., min_length=1, description="Nome do pet")
    especie: str = Field(..., description="Espécie (Canina, Felina, etc.)")
    raca: str = Field("SRD", description="Raça do pet")
    porte: str = Field(..., description="Porte (P, M, G, XG)")
    idade_anos: int = Field(0, ge=0, description="Idade em anos")
    idade_meses: int = Field(0, ge=0, le=11, description="Idade em meses")
    sexo: str = Field("", description="Sexo do pet (M/F)")
    peso_kg: float = Field(0, ge=0, description="Peso em kg")

    # Agendamento
    data_atendimento: date = Field(..., description="Data solicitada para o procedimento")

    # Triagem
    triagem: TriagemCreate


class AgendamentoResponse(BaseModel):
    """Resposta alinhada com a tabela `agendamentos` do Supabase."""
    id: str | None = None
    tenant_id: str | None = None
    nome_tutor: str = ""
    cpf_tutor: str = ""
    nome_animal: str = ""
    especie: str = ""
    raca: str = ""
    porte: str = ""
    data_atendimento: str | None = None
    status_ia: str = "Pendente"
    created_at: str | None = None
