# 🏋️ Sistema de Gestão de Academia Universitária

## 📖 Sobre o Projeto

Este projeto consiste no desenvolvimento de um **Sistema de Gestão de Academia Universitária**, capaz de gerenciar associados, planos de associação, aulas coletivas, frequência e pagamentos da academia situada no campus universitário.

O sistema foi desenvolvido como parte do **Projeto Semestral da disciplina de Engenharia de Software**, do curso de **Engenharia de Software do Centro Universitário Tiradentes de Pernambuco (UNIT-PE)**.

A aplicação foi implementada em **Python**, utilizando **Programação Estruturada com separação em camadas (services, utils, constants)** e persistência de dados em **arquivo JSON local**, eliminando a necessidade de instalação de banco de dados ou servidor externo.

> Projeto Semestral — Engenharia de Software | UNIT-PE | 2026.1
> Prof. Dr. David Barrientos

---

## 👥 Grupo 4 — Integrantes

- Cauã William
- João Ricardo
- Cauã Alves

---

## 🎯 Objetivo

O principal objetivo do sistema é automatizar o processo de gestão de uma academia universitária, garantindo:

- Controle eficiente dos associados e seus planos;
- Agendamento de aulas coletivas com controle de vagas;
- Limite de aulas por semana de acordo com o tipo de plano;
- Congelamento temporário de planos com prorrogação automática do vencimento;
- Cálculo automático de multas em caso de cancelamento antecipado;
- Registro de frequência e histórico individual de treinos;
- Relatórios gerenciais para o administrador.

---

## 👥 Atores do Sistema

O sistema foi desenvolvido considerando quatro tipos de usuários, cada um com seu próprio menu:

### Recepcionista
Responsável por cadastrar associados, gerenciar planos, agendar aulas e registrar pagamentos e presenças.

### Administrador
Responsável por relatórios gerenciais, controle de planos vencendo e gestão de instrutores.

### Instrutor
Responsável por criar, listar e cancelar turmas de aulas coletivas.

### Associado
Pode agendar e cancelar aulas, consultar seu histórico de treinos e extrato financeiro.

---

## ⚙️ Funcionalidades Implementadas

### Gestão de Associados

O sistema permite:

- Cadastrar associado com escolha de plano;
- Listar todos os associados;
- Renovar plano com cálculo automático do novo vencimento;
- Cancelar plano antecipado com **multa automática proporcional**;
- **Congelar** e **descongelar** plano (vencimento prorrogado pelos dias congelados).

---

### Controle de Planos

Cada plano possui regras distintas:

| Plano | Valor | Duração | Aulas/semana | Congelamento | Multa |
|---|---|---|---|---|---|
| Mensal | R$ 120,00 | 1 mês | 3 | ❌ | 20% |
| Semestral | R$ 600,00 | 6 meses | 5 | ✅ | 15% |
| Anual | R$ 1.000,00 | 12 meses | 5 | ✅ | 10% |
| Estudante | R$ 350,00 | 6 meses | 3 | ✅ | 10% |

---

### Controle de Vagas

Cada turma possui um número máximo de vagas cadastrado pelo instrutor. Caso a turma esteja lotada, o agendamento não é permitido.

**Exemplo:**

Turma de Yoga — 20 vagas

Vagas ocupadas: 20

**Resultado:**

Agendamento negado por falta de vagas.

---

### Limite Semanal de Aulas

O sistema verifica automaticamente quantas aulas o associado já possui confirmadas na semana da aula desejada, com base no plano ativo.

**Exemplo:**

Associado com plano Mensal (limite: 3 aulas/semana)

Aulas já agendadas na semana: 3

**Resultado:**

Agendamento negado — limite semanal atingido.

---

### Congelamento de Plano

Quando o plano é congelado, o sistema registra a data de início do congelamento. Ao descongelar, os dias congelados são calculados e o vencimento é prorrogado automaticamente.

**Exemplo:**

Vencimento original: 30/08/2026

Congelado por: 15 dias

**Resultado:**

Novo vencimento: 14/09/2026

---

### Multa por Cancelamento Antecipado

O sistema calcula automaticamente a multa proporcional ao tempo restante do plano no momento do cancelamento.

**Exemplo:**

Plano Semestral (R$ 600,00 / 6 meses) — 90 dias restantes

Multa (15%): R$ 45,00

---

### Registro de Frequência e Histórico

O sistema permite registrar a presença do associado nas aulas agendadas, com consulta do histórico individual de treinos por data e modalidade.

---

### Relatórios Gerenciais

O administrador tem acesso a:

- Número total de associados (ativos, congelados, cancelados);
- Turmas ativas e agendamentos confirmados;
- Total de presenças registradas;
- Receita total acumulada;
- Lista de associados com plano vencendo nos próximos 30 dias.

---

## 🗄️ Banco de Dados

Diferente de outros grupos, o Grupo 4 optou pela persistência de dados em **arquivo JSON local** (`data/dados.json`), funcionando de forma similar a um banco de dados, sem necessidade de servidor, instalação ou configuração adicional.

O arquivo **não precisa ser criado manualmente** — ele é gerado automaticamente na primeira execução do sistema, já com a estrutura correta.

### "Tabela": associados

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
| status | STRING (ativo / congelado / cancelado) |
| congelado_em | DATE \| null |
| dias_congelados | INT |

### "Tabela": aulas (turmas)

| Campo | Tipo |
|---|---|
| id | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |
| vagas | INT |
| status | STRING (ativa / cancelada) |

### "Tabela": agendamentos

| Campo | Tipo |
|---|---|
| aula_id | STRING |
| id_associado | STRING |
| nome | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |
| status | STRING (confirmado / cancelado / cancelado_turma) |

### "Tabela": frequencias

| Campo | Tipo |
|---|---|
| id_associado | STRING |
| nome | STRING |
| aula_id | STRING |
| modalidade | STRING |
| data | DATE |
| hora | TIME |

### "Tabela": pagamentos

| Campo | Tipo |
|---|---|
| id_associado | STRING |
| data | DATE |
| desc | STRING |
| valor | FLOAT |
| tipo | STRING (entrada / multa) |

### "Tabela": instrutores

| Campo | Tipo |
|---|---|
| id (chave) | STRING |
| nome | STRING |
| especialidade | STRING |

---

## 💻 Tecnologias Utilizadas

- Python 3.6+
- Módulo `json` (persistência de dados)
- Módulo `datetime` (manipulação de datas e cálculos)
- Módulo `os` (gerenciamento de arquivos)
- VS Code

---

## 🚀 Como Executar

### 1. Verificar o Python instalado

Abra o terminal e execute:

```bash
python --version
```

O projeto exige **Python 3.6 ou superior**. Não há necessidade de instalar nenhuma biblioteca adicional.

### 2. Clonar ou extrair o projeto

```bash
cd academia_unit
```

### 3. Executar o sistema

```bash
python main.py
```

O arquivo `data/dados.json` será criado automaticamente na primeira execução.

### 4. Escolher o ator no menu inicial

```
==========================================
   ACADEMIA UNIT-PE — SISTEMA DE GESTÃO
==========================================
  1. Entrar como Recepcionista
  2. Entrar como Administrador
  3. Entrar como Instrutor
  4. Entrar como Associado
  0. Sair
```

---

## 📁 Estrutura do Projeto

```
academia_unit/
├── main.py                          # Ponto de entrada do sistema
├── data/
│   └── dados.json                   # Gerado automaticamente na 1ª execução
├── src/
│   ├── constants.py                 # Planos, modalidades e regras de negócio
│   ├── menu.py                      # Menus separados por ator
│   ├── services/
│   │   ├── associados_service.py    # Cadastro, renovação, congelamento, multa
│   │   ├── aulas_service.py         # Turmas e agendamentos com controle de vagas
│   │   ├── frequencia_service.py    # Check-in e histórico de treinos
│   │   ├── pagamentos_service.py    # Registro, extrato e cálculo de mensalidade
│   │   └── admin_service.py         # Relatórios e gestão de instrutores
│   └── utils/
│       ├── storage.py               # Leitura e escrita do JSON
│       └── display.py               # Funções auxiliares de exibição
└── README.md
```

---

## 📚 Conceitos Aplicados

Durante o desenvolvimento foram utilizados conceitos importantes da Engenharia de Software e Programação:

- Programação Estruturada e Modularização em Funções;
- Separação em Camadas (services, utils, constants);
- Persistência de Dados em Arquivo JSON;
- Manipulação de Datas (vencimento, congelamento, semanas);
- CRUD (Create, Read, Update e Delete) aplicado a associados, turmas, agendamentos e pagamentos;
- Regras de Negócio (limite semanal, multa proporcional, congelamento com prorrogação);
- Controle de Vagas por Turma;
- Histórico Individual de Treinos;
- Relatórios Gerenciais;
- Tratamento de Entrada do Usuário.

---

## 📌 Considerações Finais

O Sistema de Gestão de Academia Universitária foi desenvolvido com o objetivo de simular um ambiente real de administração de academia, permitindo o controle eficiente de associados, planos, aulas coletivas e pagamentos.

O projeto demonstra a aplicação prática dos conceitos estudados ao longo da disciplina, integrando programação estruturada, persistência de dados e regras de negócio em uma solução funcional, sem necessidade de dependências externas.

---

📄 Projeto acadêmico — UNIT-PE 2026.1
