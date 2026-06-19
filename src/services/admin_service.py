"""
Serviço administrativo: relatórios gerenciais e gestão de instrutores.
"""

from datetime import date

from src.utils.display import titulo, linha, pausar
from src.utils.storage import salvar


def relatorio_geral(dados):
    titulo("RELATÓRIO GERAL")
    total_assoc = len(dados["associados"])
    ativos = sum(1 for a in dados["associados"].values() if a["status"] == "ativo")
    congelados = sum(1 for a in dados["associados"].values() if a["status"] == "congelado")
    cancelados = sum(1 for a in dados["associados"].values() if a["status"] == "cancelado")

    total_turmas = len([a for a in dados["aulas"] if a["status"] == "ativa"])
    total_agend = sum(1 for ag in dados["agendamentos"] if ag["status"] == "confirmado")
    total_freq = len(dados["frequencias"])

    receita = sum(p["valor"] for p in dados["pagamentos"])

    linha()
    print(f"  Associados cadastrados : {total_assoc}")
    print(f"    ↳ Ativos             : {ativos}")
    print(f"    ↳ Congelados         : {congelados}")
    print(f"    ↳ Cancelados         : {cancelados}")
    print(f"  Turmas ativas          : {total_turmas}")
    print(f"  Agendamentos ativos    : {total_agend}")
    print(f"  Presenças registradas  : {total_freq}")
    print(f"  Receita total          : R$ {receita:.2f}")
    linha()
    pausar()


def associados_vencendo(dados):
    titulo("ASSOCIADOS COM PLANO VENCENDO (próximos 30 dias)")
    hoje = date.today()
    linha()
    encontrou = False
    for aid, a in dados["associados"].items():
        if a["status"] != "ativo":
            continue
        venc = date.fromisoformat(a["vencimento"])
        dias = (venc - hoje).days
        if 0 <= dias <= 30:
            print(f"[{aid}] {a['nome']:<25} | {a['plano']:<12} | Vence em {dias} dia(s) ({a['vencimento']})")
            encontrou = True
    if not encontrou:
        print("Nenhum plano vencendo nos próximos 30 dias.")
    linha()
    pausar()


def cadastrar_instrutor(dados):
    titulo("CADASTRAR INSTRUTOR")
    nome = input("Nome: ").strip()
    especialidade = input("Especialidade (ex: Yoga, Spinning): ").strip()

    inst_id = str(dados["proximo_id_instrutor"])
    dados["proximo_id_instrutor"] += 1

    dados["instrutores"][inst_id] = {
        "nome": nome,
        "especialidade": especialidade,
    }

    salvar(dados)
    print(f"✔ Instrutor cadastrado com ID {inst_id}.")
    pausar()


def listar_instrutores(dados):
    titulo("INSTRUTORES CADASTRADOS")
    if not dados["instrutores"]:
        print("Nenhum instrutor cadastrado.")
        pausar()
        return
    linha()
    for iid, inst in dados["instrutores"].items():
        print(f"[{iid}] {inst['nome']:<25} | {inst['especialidade']}")
    linha()
    pausar()
