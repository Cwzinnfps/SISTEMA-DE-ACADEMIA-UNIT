"""
Serviço de gestão de associados: cadastro, listagem, congelamento,
renovação e cancelamento antecipado com multa.
"""

from datetime import date, timedelta

from src.constants import PLANOS, PLANO_POR_NOME
from src.utils.display import titulo, linha, pausar
from src.utils.storage import salvar


def cadastrar_associado(dados):
    titulo("CADASTRAR ASSOCIADO")
    nome = input("Nome completo: ").strip()
    cpf = input("CPF: ").strip()
    email = input("E-mail: ").strip()

    # Verifica CPF duplicado
    for a in dados["associados"].values():
        if a["cpf"] == cpf:
            print("CPF já cadastrado.")
            pausar()
            return

    print("\nPlanos disponíveis:")
    for k, p in PLANOS.items():
        congelar = "Sim" if p["pode_congelar"] else "Não"
        print(f"  {k}. {p['nome']:10} | R$ {p['valor']:8.2f} | {p['meses']} mês/es "
              f"| {p['aulas_semana']} aulas/sem | Congelamento: {congelar} "
              f"| Multa: {int(p['multa_pct']*100)}%")
    escolha = input("Escolha o plano (1-4): ").strip()

    if escolha not in PLANOS:
        print("Plano inválido.")
        pausar()
        return

    plano = PLANOS[escolha]
    hoje = date.today()
    vencimento = (hoje + timedelta(days=30 * plano["meses"])).isoformat()
    assoc_id = str(dados["proximo_id"])
    dados["proximo_id"] += 1

    dados["associados"][assoc_id] = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "plano": plano["nome"],
        "plano_key": escolha,
        "inicio": hoje.isoformat(),
        "vencimento": vencimento,
        "status": "ativo",          # ativo | congelado | cancelado
        "congelado_em": None,
        "dias_congelados": 0,
    }

    dados["pagamentos"].append({
        "id_associado": assoc_id,
        "data": hoje.isoformat(),
        "desc": f"Adesão — Plano {plano['nome']}",
        "valor": plano["valor"],
        "tipo": "entrada",
    })

    salvar(dados)
    print(f"\n✔ Cadastrado! ID: {assoc_id} | Plano: {plano['nome']} | Vence: {vencimento}")
    pausar()


def listar_associados(dados):
    titulo("ASSOCIADOS CADASTRADOS")
    if not dados["associados"]:
        print("Nenhum associado cadastrado.")
        pausar()
        return

    linha()
    print(f"{'ID':<4} {'Nome':<25} {'Plano':<12} {'Status':<10} {'Vencimento'}")
    linha()
    for aid, a in dados["associados"].items():
        print(f"[{aid:<3}] {a['nome']:<25} {a['plano']:<12} {a['status']:<10} {a['vencimento']}")
    linha()
    pausar()


def congelar_plano(dados):
    titulo("CONGELAR PLANO")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    a = dados["associados"][assoc_id]
    plano = PLANOS[a["plano_key"]]

    if not plano["pode_congelar"]:
        print(f"O plano {a['plano']} não permite congelamento.")
        pausar()
        return

    if a["status"] == "congelado":
        print("Plano já está congelado.")
        pausar()
        return

    if a["status"] != "ativo":
        print("Apenas planos ativos podem ser congelados.")
        pausar()
        return

    a["status"] = "congelado"
    a["congelado_em"] = date.today().isoformat()
    salvar(dados)
    print(f"✔ Plano de {a['nome']} congelado a partir de hoje.")
    pausar()


def descongelar_plano(dados):
    titulo("DESCONGELAR PLANO")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    a = dados["associados"][assoc_id]
    if a["status"] != "congelado":
        print("O plano não está congelado.")
        pausar()
        return

    hoje = date.today()
    congelado_em = date.fromisoformat(a["congelado_em"])
    dias = (hoje - congelado_em).days
    a["dias_congelados"] = a.get("dias_congelados", 0) + dias

    # Prorroga o vencimento pelos dias congelados
    venc_atual = date.fromisoformat(a["vencimento"])
    novo_venc = venc_atual + timedelta(days=dias)
    a["vencimento"] = novo_venc.isoformat()
    a["status"] = "ativo"
    a["congelado_em"] = None

    salvar(dados)
    print(f"✔ Plano reativado. Dias congelados: {dias}. Novo vencimento: {novo_venc.isoformat()}")
    pausar()


def cancelar_plano(dados):
    titulo("CANCELAMENTO ANTECIPADO DE PLANO")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    a = dados["associados"][assoc_id]
    if a["status"] == "cancelado":
        print("Plano já cancelado.")
        pausar()
        return

    plano = PLANOS[a["plano_key"]]
    hoje = date.today()
    vencimento = date.fromisoformat(a["vencimento"])
    dias_restantes = max((vencimento - hoje).days, 0)
    valor_dia = plano["valor"] / (plano["meses"] * 30)
    valor_restante = valor_dia * dias_restantes
    multa = round(valor_restante * plano["multa_pct"], 2)

    print(f"\nAssociado : {a['nome']}")
    print(f"Plano     : {a['plano']}")
    print(f"Vencimento: {a['vencimento']}")
    print(f"Dias restantes: {dias_restantes}")
    print(f"Multa ({int(plano['multa_pct']*100)}%): R$ {multa:.2f}")
    confirma = input("\nConfirmar cancelamento? (s/n): ").strip().lower()

    if confirma != "s":
        print("Cancelamento abortado.")
        pausar()
        return

    a["status"] = "cancelado"
    if multa > 0:
        dados["pagamentos"].append({
            "id_associado": assoc_id,
            "data": hoje.isoformat(),
            "desc": f"Multa cancelamento — Plano {a['plano']}",
            "valor": multa,
            "tipo": "multa",
        })

    salvar(dados)
    print(f"✔ Plano cancelado. Multa de R$ {multa:.2f} registrada.")
    pausar()


def renovar_plano(dados):
    titulo("RENOVAR PLANO")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    a = dados["associados"][assoc_id]
    print(f"\nAssociado : {a['nome']}")
    print(f"Plano atual: {a['plano']} | Vencimento: {a['vencimento']}")

    print("\nNovos planos:")
    for k, p in PLANOS.items():
        print(f"  {k}. {p['nome']:10} | R$ {p['valor']:.2f} | {p['meses']} mês/es")
    escolha = input("Escolha o plano para renovação (1-4): ").strip()

    if escolha not in PLANOS:
        print("Plano inválido.")
        pausar()
        return

    plano = PLANOS[escolha]
    hoje = date.today()
    # Se ainda vigente, prorroga a partir do vencimento atual
    venc_atual = date.fromisoformat(a["vencimento"])
    base = venc_atual if venc_atual > hoje else hoje
    novo_venc = (base + timedelta(days=30 * plano["meses"])).isoformat()

    a["plano"] = plano["nome"]
    a["plano_key"] = escolha
    a["vencimento"] = novo_venc
    a["status"] = "ativo"

    dados["pagamentos"].append({
        "id_associado": assoc_id,
        "data": hoje.isoformat(),
        "desc": f"Renovação — Plano {plano['nome']}",
        "valor": plano["valor"],
        "tipo": "entrada",
    })

    salvar(dados)
    print(f"✔ Plano renovado para {plano['nome']}. Novo vencimento: {novo_venc}")
    pausar()
