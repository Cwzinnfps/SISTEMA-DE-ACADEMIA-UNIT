"""
Menu principal do sistema com seleção de ator.
Atores: Recepcionista | Administrador | Instrutor | Associado
"""

from src.utils.storage import carregar
from src.utils.display import pausar

# Importações dos serviços
from src.services.associados_service import (
    cadastrar_associado, listar_associados,
    congelar_plano, descongelar_plano,
    cancelar_plano, renovar_plano,
)
from src.services.aulas_service import (
    criar_turma, listar_turmas, cancelar_turma,
    agendar_aula, listar_aulas_associado, cancelar_agendamento,
)
from src.services.frequencia_service import registrar_presenca, historico_treinos
from src.services.pagamentos_service import registrar_pagamento, extrato, calcular_mensalidade
from src.services.admin_service import (
    relatorio_geral, associados_vencendo,
    cadastrar_instrutor, listar_instrutores,
)


# ──────────────────────────────────────────────
# Menus por ator
# ──────────────────────────────────────────────

MENU_RECEPCIONISTA = {
    "1": ("Cadastrar associado",         cadastrar_associado),
    "2": ("Listar associados",           listar_associados),
    "3": ("Renovar plano",               renovar_plano),
    "4": ("Cancelar plano (com multa)",  cancelar_plano),
    "5": ("Congelar plano",              congelar_plano),
    "6": ("Descongelar plano",           descongelar_plano),
    "7": ("Agendar aula para associado", agendar_aula),
    "8": ("Cancelar agendamento",        cancelar_agendamento),
    "9": ("Registrar presença",          registrar_presenca),
    "10": ("Registrar pagamento",        registrar_pagamento),
    "11": ("Ver extrato",                extrato),
}

MENU_ADMINISTRADOR = {
    "1": ("Relatório geral",             relatorio_geral),
    "2": ("Planos vencendo (30 dias)",   associados_vencendo),
    "3": ("Listar associados",           listar_associados),
    "4": ("Extrato de pagamentos",       extrato),
    "5": ("Cadastrar instrutor",         cadastrar_instrutor),
    "6": ("Listar instrutores",          listar_instrutores),
}

MENU_INSTRUTOR = {
    "1": ("Criar turma",                 criar_turma),
    "2": ("Listar turmas",               listar_turmas),
    "3": ("Cancelar turma",              cancelar_turma),
    "4": ("Ver frequência de turma",     historico_treinos),
}

MENU_ASSOCIADO = {
    "1": ("Ver minhas aulas agendadas",  listar_aulas_associado),
    "2": ("Agendar aula",                agendar_aula),
    "3": ("Cancelar agendamento",        cancelar_agendamento),
    "4": ("Meu histórico de treinos",    historico_treinos),
    "5": ("Meu extrato financeiro",      extrato),
    "6": ("Calcular mensalidade",        calcular_mensalidade),
}

ATORES = {
    "1": ("Recepcionista", MENU_RECEPCIONISTA),
    "2": ("Administrador", MENU_ADMINISTRADOR),
    "3": ("Instrutor",     MENU_INSTRUTOR),
    "4": ("Associado",     MENU_ASSOCIADO),
}


# ──────────────────────────────────────────────
# Funções de exibição
# ──────────────────────────────────────────────

def _cabecalho_ator(nome_ator, menu):
    print("\n" + "=" * 45)
    print(f"   ACADEMIA UNIT-PE — {nome_ator.upper()}")
    print("=" * 45)
    for k, (desc, _) in menu.items():
        print(f"  {k:>2}. {desc}")
    print("   0. Voltar / Sair")


def _executar_menu(dados, nome_ator, menu):
    while True:
        _cabecalho_ator(nome_ator, menu)
        opcao = input("\nOpção: ").strip()

        if opcao == "0":
            break
        if opcao in menu:
            _, funcao = menu[opcao]
            funcao(dados)
        else:
            print("Opção inválida.")


def iniciar():
    dados = carregar()

    while True:
        print("\n" + "=" * 45)
        print("   ACADEMIA UNIT-PE — SISTEMA DE GESTÃO")
        print("=" * 45)
        for k, (nome, _) in ATORES.items():
            print(f"  {k}. Entrar como {nome}")
        print("  0. Sair")

        ator = input("\nQuem está acessando? ").strip()

        if ator == "0":
            print("\nAté logo!\n")
            break

        if ator in ATORES:
            nome_ator, menu = ATORES[ator]
            _executar_menu(dados, nome_ator, menu)
        else:
            print("Opção inválida.")
