"""
Serviço de gestão de aulas coletivas:
- Instrutor: cria e gerencia turmas
- Associado/Recepcionista: agenda e cancela reservas com controle de vagas
  e verificação do limite semanal do plano
"""

from datetime import date, timedelta

from src.constants import MODALIDADES, VAGAS_POR_AULA, PLANOS
from src.utils.display import titulo, linha, pausar
from src.utils.storage import salvar


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _vagas_ocupadas(dados, aula_id):
    return sum(
        1 for ag in dados["agendamentos"]
        if ag["aula_id"] == aula_id and ag["status"] == "confirmado"
    )


def _aulas_na_semana(dados, assoc_id, data_str):
    """Conta quantas aulas confirmadas o associado tem na semana da data_str."""
    data = date.fromisoformat(data_str)
    inicio_semana = data - timedelta(days=data.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    count = 0
    for ag in dados["agendamentos"]:
        if ag["id_associado"] != assoc_id or ag["status"] != "confirmado":
            continue
        # busca a data da aula referenciada
        for aula in dados["aulas"]:
            if aula["id"] == ag["aula_id"]:
                d = date.fromisoformat(aula["data"])
                if inicio_semana <= d <= fim_semana:
                    count += 1
    return count


# ──────────────────────────────────────────────
# Funções do Instrutor
# ──────────────────────────────────────────────

def criar_turma(dados):
    titulo("CRIAR TURMA DE AULA")

    print("\nModalidades:")
    for i, m in enumerate(MODALIDADES, 1):
        print(f"  {i}. {m}")
    escolha = input("Escolha a modalidade (1-5): ").strip()

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(MODALIDADES)):
        print("Opção inválida.")
        pausar()
        return

    modalidade = MODALIDADES[int(escolha) - 1]
    data_aula = input("Data da aula (AAAA-MM-DD): ").strip()
    hora = input("Hora (ex: 08:00): ").strip()
    vagas_str = input(f"Número de vagas (padrão {VAGAS_POR_AULA}): ").strip()
    vagas = int(vagas_str) if vagas_str.isdigit() else VAGAS_POR_AULA

    aula_id = str(dados["proximo_id_aula"])
    dados["proximo_id_aula"] += 1

    dados["aulas"].append({
        "id": aula_id,
        "modalidade": modalidade,
        "data": data_aula,
        "hora": hora,
        "vagas": vagas,
        "status": "ativa",
    })

    salvar(dados)
    print(f"\n✔ Turma [{aula_id}] de {modalidade} criada para {data_aula} às {hora} ({vagas} vagas).")
    pausar()


def listar_turmas(dados):
    titulo("TURMAS CADASTRADAS")
    ativas = [a for a in dados["aulas"] if a["status"] == "ativa"]
    if not ativas:
        print("Nenhuma turma ativa.")
        pausar()
        return
    linha()
    print(f"{'ID':<4} {'Modalidade':<20} {'Data':<12} {'Hora':<7} {'Vagas'}")
    linha()
    for a in ativas:
        ocupadas = _vagas_ocupadas(dados, a["id"])
        livres = a["vagas"] - ocupadas
        print(f"[{a['id']:<3}] {a['modalidade']:<20} {a['data']:<12} {a['hora']:<7} {livres}/{a['vagas']} livres")
    linha()
    pausar()


def cancelar_turma(dados):
    titulo("CANCELAR TURMA")
    aula_id = input("ID da turma: ").strip()

    turma = next((a for a in dados["aulas"] if a["id"] == aula_id and a["status"] == "ativa"), None)
    if not turma:
        print("Turma não encontrada.")
        pausar()
        return

    turma["status"] = "cancelada"
    # Cancela todos os agendamentos vinculados
    for ag in dados["agendamentos"]:
        if ag["aula_id"] == aula_id and ag["status"] == "confirmado":
            ag["status"] = "cancelado_turma"

    salvar(dados)
    print("✔ Turma cancelada e agendamentos removidos.")
    pausar()


# ──────────────────────────────────────────────
# Funções do Recepcionista / Associado
# ──────────────────────────────────────────────

def agendar_aula(dados):
    titulo("AGENDAR AULA")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    assoc = dados["associados"][assoc_id]
    if assoc["status"] != "ativo":
        print(f"Plano do associado está {assoc['status']}. Não é possível agendar.")
        pausar()
        return

    ativas = [a for a in dados["aulas"] if a["status"] == "ativa"]
    if not ativas:
        print("Nenhuma turma disponível.")
        pausar()
        return

    linha()
    print(f"{'ID':<4} {'Modalidade':<20} {'Data':<12} {'Hora':<7} {'Vagas livres'}")
    linha()
    for a in ativas:
        livres = a["vagas"] - _vagas_ocupadas(dados, a["id"])
        print(f"[{a['id']:<3}] {a['modalidade']:<20} {a['data']:<12} {a['hora']:<7} {livres}")
    linha()

    aula_id = input("ID da turma: ").strip()
    turma = next((a for a in ativas if a["id"] == aula_id), None)
    if not turma:
        print("Turma não encontrada.")
        pausar()
        return

    # Verifica vagas
    if _vagas_ocupadas(dados, aula_id) >= turma["vagas"]:
        print("Turma sem vagas disponíveis.")
        pausar()
        return

    # Verifica duplicidade
    ja_agendado = any(
        ag["aula_id"] == aula_id and ag["id_associado"] == assoc_id and ag["status"] == "confirmado"
        for ag in dados["agendamentos"]
    )
    if ja_agendado:
        print("Associado já agendado nessa turma.")
        pausar()
        return

    # Verifica limite semanal do plano
    plano = PLANOS[assoc["plano_key"]]
    aulas_semana = _aulas_na_semana(dados, assoc_id, turma["data"])
    if aulas_semana >= plano["aulas_semana"]:
        print(f"Limite de {plano['aulas_semana']} aulas/semana atingido para o plano {assoc['plano']}.")
        pausar()
        return

    dados["agendamentos"].append({
        "aula_id": aula_id,
        "id_associado": assoc_id,
        "nome": assoc["nome"],
        "modalidade": turma["modalidade"],
        "data": turma["data"],
        "hora": turma["hora"],
        "status": "confirmado",
    })

    salvar(dados)
    print(f"\n✔ Aula de {turma['modalidade']} agendada para {turma['data']} às {turma['hora']}!")
    pausar()


def listar_aulas_associado(dados):
    titulo("AULAS AGENDADAS DO ASSOCIADO")
    assoc_id = input("ID do associado: ").strip()

    ativas = [
        ag for ag in dados["agendamentos"]
        if ag["id_associado"] == assoc_id and ag["status"] == "confirmado"
    ]

    if not ativas:
        print("Nenhuma aula agendada.")
        pausar()
        return

    linha()
    for ag in ativas:
        print(f"{ag['data']} {ag['hora']} | {ag['modalidade']}")
    linha()
    pausar()


def cancelar_agendamento(dados):
    titulo("CANCELAR AGENDAMENTO")
    assoc_id = input("ID do associado: ").strip()

    ativos = [
        (i, ag) for i, ag in enumerate(dados["agendamentos"])
        if ag["id_associado"] == assoc_id and ag["status"] == "confirmado"
    ]

    if not ativos:
        print("Nenhum agendamento ativo.")
        pausar()
        return

    for pos, (_, ag) in enumerate(ativos):
        print(f"  {pos}. {ag['modalidade']} — {ag['data']} {ag['hora']}")

    escolha = input("Número para cancelar: ").strip()
    if not escolha.isdigit() or int(escolha) >= len(ativos):
        print("Opção inválida.")
        pausar()
        return

    idx, _ = ativos[int(escolha)]
    dados["agendamentos"][idx]["status"] = "cancelado"
    salvar(dados)
    print("✔ Agendamento cancelado.")
    pausar()
