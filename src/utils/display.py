"""
Funções utilitárias de exibição no terminal.
"""


def titulo(texto):
    print(f"\n{'=' * 45}")
    print(f"   {texto}")
    print("=" * 45)


def linha():
    print("-" * 45)


def pausar():
    input("\n[ENTER para continuar]")
