"""
Serviço de frequência: check-in de presença e consulta do histórico
individual de treinos por associado.
"""

from datetime import date

from src.utils.display import titulo, linha, pausar
from src.utils.storage import salvar


def registrar_presenca(dados):
    titulo("REGISTRAR PRESENÇA")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    assoc = dados["associados"][assoc_id]
    if assoc["status"] != "ativo":
        print(f"Plano {assoc['status']}. Check-in não permitido.")
        pausar()
        return

    # Lista agendamentos confirmados de hoje
    hoje = date.today().isoformat()
    agendamentos_hoje = [
        ag for ag in dados["agendamentos"]
        if ag["id_associado"] == assoc_id and ag["status"] == "confirmado" and ag["data"] == hoje
    ]

    if not agendamentos_hoje:
        print(f"Nenhuma aula agendada para {assoc['nome']} hoje ({hoje}).")
        pausar()
        return

    print(f"\nAulas de hoje — {assoc['nome']}:")
    for pos, ag in enumerate(agendamentos_hoje):
        print(f"  {pos}. {ag['modalidade']} às {ag['hora']}")

    escolha = input("Número da aula para confirmar presença: ").strip()
    if not escolha.isdigit() or int(escolha) >= len(agendamentos_hoje):
        print("Opção inválida.")
        pausar()
        return

    ag_escolhido = agendamentos_hoje[int(escolha)]

    # Verifica se já fez check-in nessa aula
    ja = any(
        f["id_associado"] == assoc_id and f["aula_id"] == ag_escolhido["aula_id"]
        for f in dados["frequencias"]
    )
    if ja:
        print("Presença já registrada para essa aula.")
        pausar()
        return

    dados["frequencias"].append({
        "id_associado": assoc_id,
        "nome": assoc["nome"],
        "aula_id": ag_escolhido["aula_id"],
        "modalidade": ag_escolhido["modalidade"],
        "data": hoje,
        "hora": ag_escolhido["hora"],
    })

    salvar(dados)
    print(f"✔ Presença de {assoc['nome']} registrada em {ag_escolhido['modalidade']}.")
    pausar()


def historico_treinos(dados):
    titulo("HISTÓRICO DE TREINOS")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    assoc = dados["associados"][assoc_id]
    historico = [f for f in dados["frequencias"] if f["id_associado"] == assoc_id]

    print(f"\nAssociado: {assoc['nome']} | Plano: {assoc['plano']}")
    print(f"Total de presenças: {len(historico)}")

    if not historico:
        print("Nenhuma presença registrada.")
        pausar()
        return

    linha()
    print(f"{'Data':<12} {'Hora':<7} {'Modalidade'}")
    linha()
    for f in sorted(historico, key=lambda x: x["data"], reverse=True):
        print(f"{f['data']:<12} {f['hora']:<7} {f['modalidade']}")
    linha()
    pausar()
