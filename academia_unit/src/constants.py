"""
Constantes do sistema: planos, modalidades e regras de negócio.
"""

# Planos com todas as regras exigidas pelo projeto
PLANOS = {
    "1": {
        "nome": "Mensal",
        "valor": 120.0,
        "meses": 1,
        "aulas_semana": 3,       # máximo de aulas coletivas por semana
        "pode_congelar": False,
        "multa_pct": 0.20,       # 20% do valor restante
    },
    "2": {
        "nome": "Semestral",
        "valor": 600.0,
        "meses": 6,
        "aulas_semana": 5,
        "pode_congelar": True,
        "multa_pct": 0.15,
    },
    "3": {
        "nome": "Anual",
        "valor": 1000.0,
        "meses": 12,
        "aulas_semana": 5,
        "pode_congelar": True,
        "multa_pct": 0.10,
    },
    "4": {
        "nome": "Estudante",
        "valor": 350.0,
        "meses": 6,
        "aulas_semana": 3,
        "pode_congelar": True,
        "multa_pct": 0.10,
    },
}

# Mapa nome → chave (para buscas rápidas)
PLANO_POR_NOME = {v["nome"]: k for k, v in PLANOS.items()}

MODALIDADES = [
    "Musculação Livre",
    "Funcional",
    "Yoga",
    "Spinning",
    "Natação",
]

VAGAS_POR_AULA = 20   # limite de vagas por turma
