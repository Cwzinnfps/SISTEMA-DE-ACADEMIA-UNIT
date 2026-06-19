"""
Camada de persistência: carrega e salva os dados do sistema em
data/dados.json (criado automaticamente na 1ª execução).
"""

import json
import os

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARQUIVO = os.path.join(_RAIZ, "data", "dados.json")

ESTRUTURA_INICIAL = {
    "associados": {},       # id -> dict
    "aulas": [],            # turmas cadastradas pelo instrutor
    "agendamentos": [],     # reservas de associados em turmas
    "pagamentos": [],       # histórico financeiro
    "frequencias": [],      # check-in de presença
    "instrutores": {},      # id -> dict
    "proximo_id": 1,
    "proximo_id_instrutor": 1,
    "proximo_id_aula": 1,
}


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        # garante chaves novas em dados antigos
        for chave, valor in ESTRUTURA_INICIAL.items():
            if chave not in dados:
                dados[chave] = valor
        return dados
    return dict(ESTRUTURA_INICIAL)


def salvar(dados):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
