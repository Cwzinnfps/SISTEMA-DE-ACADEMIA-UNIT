"""
Serviço financeiro: registro de pagamentos, extrato e cálculo de mensalidades.
"""

from datetime import date

from src.constants import PLANOS
from src.utils.display import titulo, linha, pausar
from src.utils.storage import salvar


def registrar_pagamento(dados):
    titulo("REGISTRAR PAGAMENTO")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    assoc = dados["associados"][assoc_id]
    print(f"Associado: {assoc['nome']} | Plano: {assoc['plano']}")

    descricao = input("Descrição (ex: Mensalidade): ").strip() or "Mensalidade"
    valor_str = input("Valor (R$): ").strip()

    try:
        valor = float(valor_str.replace(",", "."))
    except ValueError:
        print("Valor inválido.")
        pausar()
        return

    dados["pagamentos"].append({
        "id_associado": assoc_id,
        "data": date.today().isoformat(),
        "desc": descricao,
        "valor": valor,
        "tipo": "entrada",
    })

    salvar(dados)
    print(f"✔ Pagamento de R$ {valor:.2f} registrado.")
    pausar()


def extrato(dados):
    titulo("EXTRATO DE PAGAMENTOS")
    assoc_id = input("ID do associado (ou ENTER para todos): ").strip()

    pagamentos = dados["pagamentos"]
    if assoc_id:
        pagamentos = [p for p in pagamentos if p["id_associado"] == assoc_id]

    if not pagamentos:
        print("Nenhum pagamento encontrado.")
        pausar()
        return

    linha()
    print(f"{'Data':<12} {'ID':<4} {'Tipo':<10} {'Descrição':<30} {'Valor':>10}")
    linha()
    total = 0
    for p in sorted(pagamentos, key=lambda x: x["data"]):
        tipo = p.get("tipo", "entrada")
        print(f"{p['data']:<12} {p['id_associado']:<4} {tipo:<10} {p['desc']:<30} R$ {p['valor']:>8.2f}")
        total += p["valor"]
    linha()
    print(f"{'TOTAL':>58} R$ {total:>8.2f}")
    pausar()


def calcular_mensalidade(dados):
    titulo("CALCULAR MENSALIDADE")
    assoc_id = input("ID do associado: ").strip()

    if assoc_id not in dados["associados"]:
        print("Associado não encontrado.")
        pausar()
        return

    assoc = dados["associados"][assoc_id]
    plano = PLANOS[assoc["plano_key"]]
    valor_mensal = round(plano["valor"] / plano["meses"], 2)

    print(f"\nAssociado : {assoc['nome']}")
    print(f"Plano     : {assoc['plano']} (R$ {plano['valor']:.2f} / {plano['meses']} mês/es)")
    print(f"Mensalidade equivalente: R$ {valor_mensal:.2f}")
    print(f"Vencimento do plano: {assoc['vencimento']}")
    pausar()
