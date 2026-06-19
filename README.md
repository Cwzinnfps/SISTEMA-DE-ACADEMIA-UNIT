# 🏋️ Sistema de Gestão de Academia Universitária

Sistema em Python para gestão de associados, planos, aulas coletivas, frequência e pagamentos de uma academia universitária.
👥 Grupo 4
Integrantes:

Cauã William
João Ricardo
Cauã Alves

> Projeto Semestral — Engenharia de Software | UNIT-PE | 2026.1  
> Prof. Dr. David Barrientos

---

## 👥 Atores do Sistema

| Ator | Responsabilidades |
|---|---|
| **Recepcionista** | Cadastrar/renovar/cancelar associados e planos, agendar aulas, registrar presenças e pagamentos |
| **Administrador** | Relatórios gerenciais, controle de planos vencendo, gestão de instrutores |
| **Instrutor** | Criar e gerenciar turmas de aulas coletivas |
| **Associado** | Agendar/cancelar aulas, consultar histórico de treinos e extrato financeiro |

---

## 📁 Estrutura do projeto

```
academia_unit/
├── main.py
├── data/
│   └── dados.json                    # Gerado automaticamente
├── src/
│   ├── constants.py                  # Planos, modalidades e regras
│   ├── menu.py                       # Menus separados por ator
│   ├── services/
│   │   ├── associados_service.py     # Cadastro, renovação, congelamento, multa
│   │   ├── aulas_service.py          # Turmas + agendamentos com controle de vagas
│   │   ├── frequencia_service.py     # Check-in e histórico de treinos
│   │   ├── pagamentos_service.py     # Registro, extrato, cálculo de mensalidade
│   │   └── admin_service.py          # Relatórios e gestão de instrutores
│   └── utils/
│       ├── storage.py                # Persistência em JSON
│       └── display.py                # Funções auxiliares de exibição
└── README.md
```

---

## ⚙️ Como executar

Requisitos: **Python 3.6+** (sem dependências externas)

```bash
cd academia_unit
python main.py
```

---

## 💳 Planos disponíveis

| Plano | Valor | Duração | Aulas/semana | Congelamento | Multa cancelamento |
|---|---|---|---|---|---|
| Mensal | R$ 120,00 | 1 mês | 3 | ❌ | 20% |
| Semestral | R$ 600,00 | 6 meses | 5 | ✅ | 15% |
| Anual | R$ 1.000,00 | 12 meses | 5 | ✅ | 10% |
| Estudante | R$ 350,00 | 6 meses | 3 | ✅ | 10% |

---

## 🏃 Modalidades de aula

- Musculação Livre
- Funcional
- Yoga
- Spinning
- Natação

---

## 🗂️ Funcionalidades implementadas

### Recepcionista
- Cadastrar associado com escolha de plano
- Listar associados
- Renovar plano (com cálculo automático de novo vencimento)
- Cancelar plano antecipado com **multa automática**
- **Congelar** e **descongelar** plano (prorroga vencimento pelos dias congelados)
- Agendar aula para associado (com verificação de vagas e limite semanal do plano)
- Cancelar agendamento
- Registrar presença (check-in)
- Registrar pagamento
- Ver extrato

### Administrador
- Relatório geral (associados, turmas, frequências, receita total)
- Listar associados com plano vencendo nos próximos 30 dias
- Extrato geral de pagamentos
- Cadastrar e listar instrutores

### Instrutor
- Criar turma (modalidade, data, hora, vagas)
- Listar turmas com vagas disponíveis
- Cancelar turma (remove agendamentos vinculados)

### Associado
- Ver aulas agendadas
- Agendar / cancelar aula
- Consultar histórico de treinos (frequência)
- Ver extrato financeiro
- Calcular mensalidade equivalente do plano

---

## 🗄️ Persistência de Dados (JSON)

### associados
| Campo | Tipo |
|---|---|
| id (chave) | STRING |
| nome | STRING |
| cpf | STRING |
| email | STRING |
| plano | STRING |
| plano_key | STRING |
| inicio | DATE |
| vencimento | DATE |
| status | STRING (ativo/congelado/cancelado) |
| congelado_em | DATE \| null |
| dias_congelados | INT |

### aulas (turmas)
| Campo | Tipo |
|---|---|
| id | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |
| vagas | INT |
| status | STRING (ativa/cancelada) |

### agendamentos
| Campo | Tipo |
|---|---|
| aula_id | STRING |
| id_associado | STRING |
| nome | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |
| status | STRING (confirmado/cancelado/cancelado_turma) |

### frequencias
| Campo | Tipo |
|---|---|
| id_associado | STRING |
| nome | STRING |
| aula_id | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |

### pagamentos
| Campo | Tipo |
|---|---|
| id_associado | STRING |
| data | DATE |
| desc | STRING |
| valor | FLOAT |
| tipo | STRING (entrada/multa) |

### instrutores
| Campo | Tipo |
|---|---|
| id (chave) | STRING |
| nome | STRING |
| especialidade | STRING |

---

## 📚 Conceitos Aplicados

- Programação estruturada e modularização em funções
- Separação em camadas (services, utils, constants)
- Persistência de dados em arquivo JSON
- Manipulação de datas (vencimento, congelamento, semanas)
- CRUD completo: associados, turmas, agendamentos, pagamentos
- Regras de negócio: limite de aulas por semana, multa proporcional, congelamento com prorrogação
- Controle de vagas por turma
- Histórico individual de treinos
- Relatórios gerenciais

---

## 📄 Licença

Projeto acadêmico — UNIT-PE 2026.1
