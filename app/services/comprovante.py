"""
Serviço de geração de comprovantes — SEPET
Gera o HTML do comprovante de agendamento com dados do animal,
aviso obrigatório e informações de contato.
"""
from datetime import datetime
from app.config import SEPET_ENDERECO, SEPET_EMAIL, SEPET_TELEFONE


def gerar_comprovante_html(agendamento: dict, triagem: dict | None = None) -> str:
    """Gera o HTML completo do comprovante de agendamento."""

    # Campos diretos da tabela agendamentos
    nome = agendamento.get("nome_animal", "N/A")
    especie = agendamento.get("especie", "N/A")
    raca = agendamento.get("raca", "SRD")
    porte = agendamento.get("porte", "N/A")
    nome_tutor = agendamento.get("nome_tutor", "N/A")
    cpf_tutor = agendamento.get("cpf_tutor", "N/A")
    data_atendimento = agendamento.get("data_atendimento", "N/A")
    status_ia = agendamento.get("status_ia", "Pendente")
    agendamento_id = agendamento.get("id", "N/A")

    # Campos extras armazenados no JSONB da triagem
    meta_pet = {}
    meta_tutor = {}
    if triagem:
        respostas = triagem.get("respostas_triagem", {})
        meta_pet = respostas.get("_meta_pet", {})
        meta_tutor = respostas.get("_meta_tutor", {})

    idade_anos = meta_pet.get("idade_anos", 0)
    idade_meses = meta_pet.get("idade_meses", 0)
    sexo = meta_pet.get("sexo", "N/A")
    peso = meta_pet.get("peso_kg", 0)
    telefone_tutor = meta_tutor.get("telefone", "N/A")

    # Formatação de idade
    partes_idade = []
    if idade_anos > 0:
        partes_idade.append(f"{idade_anos} Ano{'s' if idade_anos > 1 else ''}")
    if idade_meses > 0:
        partes_idade.append(f"{idade_meses} Mes{'es' if idade_meses > 1 else ''}")
    idade_formatada = " e ".join(partes_idade) if partes_idade else "Não informado"

    # Parecer IA
    parecer_ia = ""
    alerta_risco = False
    if triagem:
        parecer_ia = triagem.get("parecer_ia", "")
        alerta_risco = triagem.get("alerta_risco", False)

    data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprovante de Agendamento – SEPET</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f4f8;
            padding: 20px;
            color: #1a202c;
        }}
        .comprovante {{
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0d9488, #6366f1);
            color: white;
            padding: 30px 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 24px; font-weight: 800; }}
        .header p {{ font-size: 12px; opacity: 0.9; margin-top: 4px; }}
        .header .protocolo {{
            margin-top: 12px;
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 6px 16px;
            border-radius: 8px;
            font-size: 12px;
        }}
        .body {{ padding: 30px 40px; }}
        .section {{
            margin-bottom: 24px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 20px;
        }}
        .section:last-child {{ border-bottom: none; }}
        .section h2 {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #0d9488;
            margin-bottom: 12px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}
        .info-item {{
            font-size: 13px;
        }}
        .info-item .label {{
            color: #718096;
            font-size: 11px;
            text-transform: uppercase;
        }}
        .info-item .value {{
            font-weight: 600;
            color: #1a202c;
        }}
        .aviso {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
            color: #92400e;
            font-weight: 500;
        }}
        .alerta {{
            background: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
            color: #991b1b;
            margin-bottom: 16px;
        }}
        .parecer {{
            background: #ede9fe;
            border-left: 4px solid #6366f1;
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
            color: #3730a3;
        }}
        .footer {{
            background: #1e293b;
            color: #94a3b8;
            padding: 20px 40px;
            text-align: center;
            font-size: 12px;
        }}
        .footer a {{ color: #5eead4; text-decoration: none; }}
        .footer .contatos {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="comprovante">
        <div class="header">
            <h1>🐾 SEPET</h1>
            <p>Sistema de Esterilização de Pets – Manaus/AM</p>
            <div class="protocolo">Protocolo: {agendamento_id}</div>
        </div>

        <div class="body">
            <div class="section">
                <h2>📋 Dados do Animal</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="label">Nome</div>
                        <div class="value">{nome}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Idade</div>
                        <div class="value">{idade_formatada}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Espécie</div>
                        <div class="value">{especie}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Raça</div>
                        <div class="value">{raca}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Porte</div>
                        <div class="value">{porte}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Sexo</div>
                        <div class="value">{sexo}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Peso</div>
                        <div class="value">{peso} kg</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Status</div>
                        <div class="value">{status_ia}</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>👤 Dados do Tutor</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="label">Nome</div>
                        <div class="value">{nome_tutor}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">CPF</div>
                        <div class="value">{cpf_tutor}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Telefone</div>
                        <div class="value">{telefone_tutor}</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Data do Atendimento</div>
                        <div class="value">{data_atendimento}</div>
                    </div>
                </div>
            </div>

            {"<div class='section'><div class='alerta'>🚨 <strong>ALERTA DE RISCO:</strong> Foram identificados fatores de risco na triagem clínica deste animal.</div></div>" if alerta_risco else ""}

            {"<div class='section'><h2>🤖 Parecer da IA</h2><div class='parecer'>" + parecer_ia + "</div></div>" if parecer_ia else ""}

            <div class="section">
                <div class="aviso">
                    ⚠️ <strong>AVISO OBRIGATÓRIO:</strong> O questionário de triagem clínica é
                    indispensável para a anestesia. As informações prestadas são de responsabilidade
                    do tutor e a veracidade dos dados é essencial para a segurança do animal.
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="contatos">
                📧 <a href="mailto:{SEPET_EMAIL}">{SEPET_EMAIL}</a> ·
                📞 {SEPET_TELEFONE}
            </div>
            <div>📍 {SEPET_ENDERECO}</div>
            <div style="margin-top: 8px; font-size: 10px; color: #64748b;">
                Emitido em {data_emissao}
            </div>
        </div>
    </div>
</body>
</html>"""

    return html


def gerar_comprovante_json(agendamento: dict, triagem: dict | None = None) -> dict:
    """Gera os dados estruturados do comprovante."""
    meta_pet = {}
    meta_tutor = {}
    if triagem:
        respostas = triagem.get("respostas_triagem", {})
        meta_pet = respostas.get("_meta_pet", {})
        meta_tutor = respostas.get("_meta_tutor", {})

    idade_anos = meta_pet.get("idade_anos", 0)
    idade_meses = meta_pet.get("idade_meses", 0)
    partes = []
    if idade_anos > 0:
        partes.append(f"{idade_anos} Ano{'s' if idade_anos > 1 else ''}")
    if idade_meses > 0:
        partes.append(f"{idade_meses} Mes{'es' if idade_meses > 1 else ''}")

    return {
        "protocolo": agendamento.get("id"),
        "animal": {
            "nome": agendamento.get("nome_animal"),
            "idade": " e ".join(partes) if partes else "Não informado",
            "especie": agendamento.get("especie"),
            "raca": agendamento.get("raca"),
            "porte": agendamento.get("porte"),
            "sexo": meta_pet.get("sexo"),
            "peso_kg": meta_pet.get("peso_kg"),
        },
        "tutor": {
            "nome": agendamento.get("nome_tutor"),
            "cpf": agendamento.get("cpf_tutor"),
            "telefone": meta_tutor.get("telefone"),
        },
        "data_atendimento": agendamento.get("data_atendimento"),
        "status_ia": agendamento.get("status_ia"),
        "parecer_ia": triagem.get("parecer_ia") if triagem else None,
        "alerta_risco": triagem.get("alerta_risco") if triagem else False,
        "aviso_obrigatorio": (
            "O questionário de triagem clínica é indispensável para a anestesia. "
            "As informações prestadas são de responsabilidade do tutor."
        ),
        "contato": {
            "email": SEPET_EMAIL,
            "telefone": SEPET_TELEFONE,
            "endereco": SEPET_ENDERECO,
        },
        "emitido_em": datetime.now().isoformat(),
    }
