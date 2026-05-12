# 📋 Planejamento de Entrega — Desafio 3: Skill de Auditoria e Refatoração Arquitetural

## Visão Geral

| Item | Detalhe |
|------|---------|
| **Objetivo** | Criar uma Skill que analisa, audita e refatora projetos para MVC |
| **Ferramenta** | Claude Code, Gemini CLI ou OpenAI Codex (escolher uma) |
| **Projetos-alvo** | 3 projetos legados (2 Python/Flask + 1 Node.js/Express) |
| **Entregável** | Repositório GitHub com Skill, código refatorado e relatórios |

---

## Fase 0 — Preparação do Ambiente (Estimativa: 30 min)

- [ ] **0.1** Fazer fork do repositório base (template do desafio)
- [ ] **0.2** Clonar o repositório localmente
- [ ] **0.3** Decidir qual ferramenta usar:
  - Claude Code (`claude`)
  - Gemini CLI
  - OpenAI Codex
- [ ] **0.4** Instalar a ferramenta escolhida (se não tiver)
- [ ] **0.5** Configurar a API Key da ferramenta escolhida
- [ ] **0.6** Verificar que os 3 projetos estão no repositório:
  - `code-smells-project/` (Python/Flask)
  - `ecommerce-api-legacy/` (Node.js/Express)
  - `task-manager-api/` (Python/Flask)
- [ ] **0.7** Instalar dependências de cada projeto para testar que funcionam:
  - Projeto 1: `cd code-smells-project && pip install -r requirements.txt`
  - Projeto 2: `cd ecommerce-api-legacy && npm install`
  - Projeto 3: `cd task-manager-api && pip install -r requirements.txt`
- [ ] **0.8** Testar que cada projeto roda (antes da refatoração)

> 🔧 **Intervenção necessária:** Instalar a ferramenta de agente (Claude Code / Gemini CLI / Codex) e configurar a API Key correspondente.

---

## Fase 1 — Análise Manual dos 3 Projetos (Estimativa: 2-3h)

> ⚠️ Esta fase é ANTES de criar a Skill. Você precisa entender os problemas para criar uma Skill que os detecte.

### Projeto 1: `code-smells-project/` (Python/Flask — E-commerce)

- [ ] **1.1** Ler todos os arquivos-fonte (`app.py`, `models.py`, `controllers.py`, `database.py`)
- [ ] **1.2** Identificar e documentar no mínimo 5 problemas:
  - [ ] ≥ 1 CRITICAL ou HIGH
  - [ ] ≥ 2 MEDIUM
  - [ ] ≥ 2 LOW
- [ ] **1.3** Para cada problema, anotar:
  - Arquivo e linha(s) exata(s)
  - Severidade
  - O que está errado
  - Qual o impacto
  - Como deveria ser

### Projeto 2: `ecommerce-api-legacy/` (Node.js/Express — LMS/Checkout)

- [ ] **1.4** Ler todos os arquivos-fonte (`app.js`, `GodManager.js`, `utils.js`)
- [ ] **1.5** Identificar e documentar no mínimo 5 problemas:
  - [ ] ≥ 1 CRITICAL ou HIGH
  - [ ] ≥ 2 MEDIUM
  - [ ] ≥ 2 LOW
- [ ] **1.6** Documentar com arquivo, linhas, severidade, descrição, impacto

### Projeto 3: `task-manager-api/` (Python/Flask — Task Manager)

- [ ] **1.7** Ler todos os arquivos-fonte (`app.py`, `database.py`, `models/`, `routes/`, `services/`, `utils/`)
- [ ] **1.8** Identificar e documentar no mínimo 5 problemas:
  - [ ] ≥ 1 CRITICAL ou HIGH
  - [ ] ≥ 2 MEDIUM
  - [ ] ≥ 2 LOW
- [ ] **1.9** Documentar com arquivo, linhas, severidade, descrição, impacto

### Documentar no README

- [ ] **1.10** Escrever a seção "Análise Manual" no `README.md` com todos os achados

---

## Fase 2 — Criação da Skill (Estimativa: 3-4h)

### 2A — Estrutura de Diretórios

- [ ] **2A.1** Criar a pasta: `code-smells-project/.claude/skills/refactor-arch/`
- [ ] **2A.2** Criar os arquivos necessários dentro dela

### 2B — SKILL.md (prompt principal)

- [ ] **2B.1** Escrever o cabeçalho com trigger (`/refactor-arch`)
- [ ] **2B.2** Escrever instruções da **Fase 1 — Análise**:
  - Como detectar linguagem (extensões de arquivo)
  - Como detectar framework (requirements.txt, package.json)
  - Como mapear domínio da aplicação
  - Formato de saída do resumo
- [ ] **2B.3** Escrever instruções da **Fase 2 — Auditoria**:
  - Referência ao catálogo de anti-patterns
  - Como gerar cada finding (arquivo, linha, severidade, descrição, impacto, recomendação)
  - Referência ao template de relatório
  - **Instrução explícita para PAUSAR e pedir confirmação**
- [ ] **2B.4** Escrever instruções da **Fase 3 — Refatoração**:
  - Referência ao playbook de refatoração
  - Referência às guidelines de MVC
  - Instruções de validação (boot + endpoints)
  - Formato de saída do resultado
- [ ] **2B.5** Revisar que é agnóstico de tecnologia (sem hardcoded Python ou Node)

### 2C — Catálogo de Anti-Patterns (≥ 8 patterns)

- [ ] **2C.1** Criar `anti-patterns.md`
- [ ] **2C.2** Documentar ≥ 8 anti-patterns distribuídos por severidade:
  - ≥ 2 CRITICAL (ex: God Class, Hardcoded Credentials, SQL Injection)
  - ≥ 2 HIGH (ex: Business Logic in Controller, Tight Coupling)
  - ≥ 2 MEDIUM (ex: N+1 Queries, Missing Validation, Code Duplication)
  - ≥ 2 LOW (ex: Magic Numbers, Poor Naming, Missing Error Handling)
- [ ] **2C.3** Para cada anti-pattern:
  - Nome e severidade
  - Sinais de detecção (como identificar no código)
  - Exemplo de código problemático
  - Impacto
- [ ] **2C.4** Incluir **detecção de APIs deprecated** (requisito obrigatório)

### 2D — Template de Relatório de Auditoria

- [ ] **2D.1** Criar `audit-template.md`
- [ ] **2D.2** Definir formato padronizado:
  - Header com info do projeto
  - Tabela de resumo por severidade
  - Lista de findings ordenada por severidade (CRITICAL → LOW)
  - Cada finding com arquivo:linhas, descrição, impacto, recomendação

### 2E — Guidelines de Arquitetura MVC

- [ ] **2E.1** Criar `mvc-guidelines.md`
- [ ] **2E.2** Definir:
  - Estrutura de diretórios MVC padrão
  - O que vai em cada camada (Models, Views/Routes, Controllers)
  - Regras de separação de responsabilidades
  - Config extraída para módulo separado
  - Error handling centralizado
  - Entry point claro

### 2F — Playbook de Refatoração (≥ 8 transformações)

- [ ] **2F.1** Criar `refactoring-playbook.md`
- [ ] **2F.2** Documentar ≥ 8 padrões de transformação:
  - Cada um com exemplo de código **antes** (problemático)
  - E código **depois** (correto)
  - Incluir exemplos em Python E JavaScript (para ser agnóstico)
- [ ] **2F.3** Exemplos:
  - God Class → separar em Model + Controller
  - Hardcoded credentials → variáveis de ambiente
  - SQL inline → Model com queries encapsuladas
  - Rota com lógica → Controller separado
  - etc.

### 2G — Heurísticas de Análise

- [ ] **2G.1** Criar `analysis-heuristics.md`
- [ ] **2G.2** Documentar como detectar:
  - Linguagem (extensões: `.py`, `.js`, `.ts`)
  - Framework (Flask: imports/app patterns, Express: require/app.listen)
  - Banco de dados (SQLAlchemy patterns, pg/mysql imports)
  - Domínio (análise de entidades/modelos/rotas)

---

## Fase 3 — Execução da Skill nos 3 Projetos (Estimativa: 2-3h)

### Projeto 1: `code-smells-project/`

- [ ] **3.1** Executar a Skill:
  ```bash
  cd code-smells-project
  claude "/refactor-arch"
  ```
- [ ] **3.2** Verificar Fase 1: stack detectada corretamente (Python + Flask)
- [ ] **3.3** Verificar Fase 2: ≥ 5 findings, ≥ 1 CRITICAL ou HIGH
- [ ] **3.4** Revisar o relatório de auditoria
- [ ] **3.5** Confirmar execução da Fase 3 (responder "y")
- [ ] **3.6** Verificar que a aplicação inicia sem erros
- [ ] **3.7** Verificar que os endpoints originais funcionam
- [ ] **3.8** Salvar relatório em `reports/audit-project-1.md`
- [ ] **3.9** Commitar o código refatorado

### Projeto 2: `ecommerce-api-legacy/`

- [ ] **3.10** Copiar a pasta `.claude/skills/refactor-arch/` para dentro do projeto
- [ ] **3.11** Executar a Skill:
  ```bash
  cd ecommerce-api-legacy
  claude "/refactor-arch"
  ```
- [ ] **3.12** Verificar Fase 1: detecta Node.js + Express
- [ ] **3.13** Verificar Fase 2: ≥ 5 findings, ≥ 1 CRITICAL ou HIGH
- [ ] **3.14** Confirmar Fase 3
- [ ] **3.15** Verificar que aplicação roda e endpoints funcionam
- [ ] **3.16** Salvar relatório em `reports/audit-project-2.md`
- [ ] **3.17** Commitar o código refatorado

### Projeto 3: `task-manager-api/`

- [ ] **3.18** Copiar a pasta `.claude/skills/refactor-arch/` para dentro do projeto
- [ ] **3.19** Executar a Skill:
  ```bash
  cd task-manager-api
  claude "/refactor-arch"
  ```
- [ ] **3.20** Verificar Fase 1: detecta Python + Flask + domínio Task Manager
- [ ] **3.21** Verificar Fase 2: ≥ 5 findings (mesmo parcialmente organizado)
- [ ] **3.22** Confirmar Fase 3
- [ ] **3.23** Verificar que aplicação funciona sem quebrar
- [ ] **3.24** Salvar relatório em `reports/audit-project-3.md`
- [ ] **3.25** Commitar o código refatorado

---

## Fase 4 — Iteração e Ajustes (Estimativa: 1-2h)

> O enunciado diz que são normais 2-4 iterações.

- [ ] **4.1** Se algum projeto não atingiu os critérios, analisar o que falhou:
  - Stack não detectada? → ajustar `analysis-heuristics.md`
  - Poucos findings? → expandir `anti-patterns.md`
  - Aplicação quebrou? → melhorar instruções de validação no SKILL.md
  - Relatório malformatado? → ajustar `audit-template.md`
- [ ] **4.2** Editar os arquivos de referência da Skill
- [ ] **4.3** Re-executar nos projetos que falharam
- [ ] **4.4** Repetir até todos os critérios serem atingidos em TODOS os 3 projetos

---

## Fase 5 — Documentação e Entrega (Estimativa: 1h30min)

### README.md

- [ ] **5.1** Seção "Análise Manual":
  - Lista de problemas identificados nos 3 projetos
  - Classificação por severidade
  - Justificativa de por que cada problema é relevante
- [ ] **5.2** Seção "Construção da Skill":
  - Decisões de design
  - Quais anti-patterns incluiu e por quê
  - Como garantiu que é agnóstica de tecnologia
  - Desafios encontrados durante o desenvolvimento
- [ ] **5.3** Seção "Resultados":
  - Resumo dos 3 relatórios de auditoria
  - Comparação antes/depois de cada projeto
  - Checklist de validação preenchido
  - Screenshots ou logs das aplicações rodando após refatoração
- [ ] **5.4** Seção "Como Executar":
  - Pré-requisitos (ferramenta de agente, API Key)
  - Comandos para cada projeto
  - Como validar que a refatoração funcionou

### Estrutura Final do Repositório

- [ ] **5.5** Verificar que a estrutura está conforme o exigido:
  ```
  desafio-skills/
  ├── README.md
  ├── code-smells-project/
  │   ├── .claude/skills/refactor-arch/
  │   │   ├── SKILL.md
  │   │   └── (arquivos de referência)
  │   └── (código refatorado)
  ├── ecommerce-api-legacy/
  │   ├── .claude/skills/refactor-arch/
  │   └── (código refatorado)
  ├── task-manager-api/
  │   ├── .claude/skills/refactor-arch/
  │   └── (código refatorado)
  └── reports/
      ├── audit-project-1.md
      ├── audit-project-2.md
      └── audit-project-3.md
  ```
- [ ] **5.6** Commit e push para GitHub
- [ ] **5.7** Verificar que o repositório é público

---

## Resumo de Estimativas

| Fase | Descrição | Tempo Estimado |
|------|-----------|---------------|
| 0 | Preparação do ambiente | 30 min |
| 1 | Análise manual dos 3 projetos | 2-3h |
| 2 | Criação da Skill (SKILL.md + 5 arquivos de referência) | 3-4h |
| 3 | Execução nos 3 projetos | 2-3h |
| 4 | Iteração e ajustes | 1-2h |
| 5 | Documentação e entrega | 1h30 |
| **Total** | | **~10-14h** |

---

## Checklist Final de Entrega

### Skill
- [ ] `SKILL.md` completo com 3 fases
- [ ] Catálogo de anti-patterns com ≥ 8 patterns
- [ ] Catálogo inclui detecção de APIs deprecated
- [ ] Template de relatório de auditoria
- [ ] Guidelines de arquitetura MVC
- [ ] Playbook de refatoração com ≥ 8 transformações (antes/depois)
- [ ] Heurísticas de análise de projeto
- [ ] Skill copiada para os 3 projetos

### Execução — Projeto 1 (code-smells-project)
- [ ] Fase 1: Stack detectada corretamente
- [ ] Fase 2: ≥ 5 findings
- [ ] Fase 2: ≥ 1 CRITICAL ou HIGH
- [ ] Fase 3: Aplicação funciona após refatoração
- [ ] Relatório salvo em `reports/audit-project-1.md`
- [ ] Código refatorado commitado

### Execução — Projeto 2 (ecommerce-api-legacy)
- [ ] Fase 1: Stack detectada corretamente
- [ ] Fase 2: ≥ 5 findings
- [ ] Fase 2: ≥ 1 CRITICAL ou HIGH
- [ ] Fase 3: Aplicação funciona após refatoração
- [ ] Relatório salvo em `reports/audit-project-2.md`
- [ ] Código refatorado commitado

### Execução — Projeto 3 (task-manager-api)
- [ ] Fase 1: Stack detectada corretamente
- [ ] Fase 2: ≥ 5 findings
- [ ] Fase 2: ≥ 1 CRITICAL ou HIGH
- [ ] Fase 3: Aplicação funciona após refatoração
- [ ] Relatório salvo em `reports/audit-project-3.md`
- [ ] Código refatorado commitado

### Documentação
- [ ] README.md — Seção "Análise Manual"
- [ ] README.md — Seção "Construção da Skill"
- [ ] README.md — Seção "Resultados" (screenshots/logs)
- [ ] README.md — Seção "Como Executar"

### Repositório
- [ ] Fork do repositório base
- [ ] Repositório público no GitHub

---

## Dependências Externas / Itens que Requerem Sua Ação

| Item | O que fazer | Quando |
|------|------------|--------|
| **Ferramenta de Agente** | Instalar Claude Code, Gemini CLI ou OpenAI Codex | Fase 0 |
| **API Key** | Gerar chave para a ferramenta escolhida | Fase 0 |
| **Confirmação Fase 2** | Você deve revisar o relatório e confirmar antes da Fase 3 | Fase 3 (cada projeto) |
| **Screenshots** | Capturar telas das aplicações rodando após refatoração | Fase 5 |
| **Validação manual** | Testar endpoints manualmente após refatoração de cada projeto | Fase 3 |

---

## Ordem de Execução Recomendada

```
1. Fork + clone + setup do ambiente [Fase 0]
          ↓
2. Ler e analisar os 3 projetos manualmente [Fase 1]
          ↓
3. Criar SKILL.md + todos os arquivos de referência [Fase 2]
          ↓
4. Executar no Projeto 1 (code-smells-project) [Fase 3]
   → Se falhou → ajustar Skill [Fase 4] → re-executar
          ↓
5. Copiar Skill e executar no Projeto 2 (ecommerce-api-legacy) [Fase 3]
   → Se falhou → ajustar Skill → re-executar
          ↓
6. Copiar Skill e executar no Projeto 3 (task-manager-api) [Fase 3]
   → Se falhou → ajustar Skill → re-executar
          ↓
7. Documentar tudo no README.md [Fase 5]
          ↓
8. Commit final + push + verificar que repositório é público [Fase 5]
```
