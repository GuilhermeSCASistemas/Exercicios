# 📚 Explicação Completa — Desafio 3: Skill de Auditoria e Refatoração Arquitetural

## O que é este projeto?

Este é o desafio mais complexo. Você vai criar uma **Skill** — basicamente um "manual de instruções" que ensina uma IA (Claude Code, Gemini CLI ou OpenAI Codex) a **analisar, auditar e refatorar** projetos de software automaticamente para o padrão MVC.

Imagine: você herda 3 projetos legados bagunçados. Ao invés de gastar dias revisando e reestruturando manualmente, você cria uma Skill que faz isso automaticamente. A IA lê o projeto, identifica problemas, gera um relatório e refatora tudo para a arquitetura MVC correta.

---

## Conceitos Fundamentais

### 1. O que é uma Skill?

Uma Skill é um **conjunto de arquivos Markdown** que instrui um agente de IA sobre como executar uma tarefa especializada. É como criar um "manual de especialista" que o agente segue.

Estrutura típica de uma Skill:
```
.claude/skills/refactor-arch/
├── SKILL.md              # O "prompt principal" — instrui o agente
├── anti-patterns.md      # Catálogo de problemas conhecidos
├── mvc-guidelines.md     # Regras da arquitetura MVC
├── audit-template.md     # Template do relatório
├── refactoring-playbook.md  # Guia de como transformar código
└── analysis-heuristics.md   # Como detectar linguagem/framework
```

**O `SKILL.md` é o coração** — é um prompt que diz ao agente: "Ao receber o comando `/refactor-arch`, faça isso passo a passo..."

### 2. O que é o Padrão MVC?

MVC = **Model-View-Controller**. É um padrão de arquitetura que separa o código em 3 camadas:

| Camada | Responsabilidade | Exemplos |
|--------|-----------------|----------|
| **Model** | Dados e lógica de negócio | Classes de entidade, validações, regras de negócio |
| **View** | Apresentação e rotas | Rotas/endpoints da API, templates, formatação de resposta |
| **Controller** | Coordenação do fluxo | Recebe requisição, chama model, retorna response |

```
Cliente → [View/Routes] → [Controller] → [Model] → [Banco de Dados]
                                ↑              ↓
                            Retorna ←──── Dados
```

**Problema em projetos legados:** Tudo misturado num único arquivo — rotas, lógica de negócio, queries SQL, validação... É o que chamamos de **"God Class"** ou **"God Method"**.

### 3. O que são Anti-Patterns e Code Smells?

**Anti-patterns** são soluções comuns que parecem boas mas causam problemas. **Code smells** são indicadores de que algo está errado no código.

Os que você precisa conhecer (e detectar):

#### Severidade CRITICAL

| Anti-Pattern | O que é | Sinal de Detecção |
|-------------|---------|-------------------|
| **God Class** | Uma classe que faz tudo | Arquivo com > 200 linhas e múltiplas responsabilidades |
| **Hardcoded Credentials** | Senhas/chaves diretamente no código | `SECRET_KEY = "abc123"`, `password = "admin"` |
| **SQL Injection** | Queries SQL construídas com concatenação de strings | `f"SELECT * FROM users WHERE id = {user_id}"` |
| **God Method** | Um método/função enorme que faz tudo | Função com > 50 linhas e múltiplos `if/else` aninhados |

#### Severidade HIGH

| Anti-Pattern | O que é | Sinal de Detecção |
|-------------|---------|-------------------|
| **Business Logic in Controller** | Lógica de negócio pesada nas rotas | Cálculos, validações complexas dentro de `@app.route` |
| **Tight Coupling** | Componentes fortemente dependentes | Import direto de módulos internos, sem injeção de dependência |
| **Global Mutable State** | Variáveis globais que mudam em runtime | `users = []` no escopo global, modificado por funções |

#### Severidade MEDIUM

| Anti-Pattern | O que é | Sinal de Detecção |
|-------------|---------|-------------------|
| **N+1 Queries** | Uma query no loop gera N queries adicionais | `for user in users: db.query(user.orders)` |
| **Missing Validation** | Endpoints sem validação de input | `request.json["email"]` sem verificar se existe |
| **Code Duplication** | Código repetido em múltiplos lugares | Mesma lógica copy-paste em vários endpoints |

#### Severidade LOW

| Anti-Pattern | O que é | Sinal de Detecção |
|-------------|---------|-------------------|
| **Magic Numbers** | Números sem significado contextual | `if status == 3:` ao invés de `if status == Status.COMPLETED:` |
| **Poor Naming** | Variáveis com nomes ruins | `x`, `tmp`, `data2`, `process_stuff()` |
| **Missing Error Handling** | Sem tratamento de erros | Ausência de `try/except` ou `try/catch` |

### 4. Os 3 Projetos-Alvo

Sua Skill deve funcionar em **3 projetos diferentes** (fornecidos no repositório base):

| # | Projeto | Stack | Domínio | Nível de Bagunça |
|---|---------|-------|---------|-----------------|
| 1 | `code-smells-project/` | Python + Flask | E-commerce (produtos, pedidos, usuários) | Muito bagunçado — tudo em ~4 arquivos |
| 2 | `ecommerce-api-legacy/` | Node.js + Express | LMS com checkout | Bagunçado — "GodManager.js" |
| 3 | `task-manager-api/` | Python + Flask | Task Manager | Parcialmente organizado — já tem separação |

A Skill deve ser **agnóstica de tecnologia** — o mesmo SKILL.md deve funcionar em Python/Flask E Node.js/Express.

### 5. As 3 Fases da Skill

A Skill opera em 3 fases sequenciais:

#### Fase 1 — Análise do Projeto
O agente examina o projeto e imprime um resumo:
- Linguagem detectada (Python, JavaScript, etc.)
- Framework (Flask, Express, etc.)
- Dependências
- Domínio da aplicação (e-commerce, task manager, etc.)
- Arquitetura atual
- Quantidade de arquivos analisados
- Tabelas do banco de dados

#### Fase 2 — Auditoria
O agente cruza o código contra o catálogo de anti-patterns e gera um relatório detalhado:
- Cada problema encontrado (**finding**) tem:
  - Severidade (CRITICAL, HIGH, MEDIUM, LOW)
  - Arquivo e linhas exatas
  - Descrição do problema
  - Impacto
  - Recomendação de correção
- Mínimo de 5 findings por projeto
- Pelo menos 1 CRITICAL ou HIGH

**⚠️ A Skill DEVE pausar aqui e pedir confirmação do usuário antes de prosseguir para a Fase 3.**

#### Fase 3 — Refatoração
O agente reestrutura o projeto para MVC:
- Cria a estrutura de diretórios MVC
- Separa Models, Views/Routes e Controllers
- Extrai configurações para módulo de config
- Centraliza error handling
- Cria entry point claro
- **Valida** que a aplicação inicia sem erros e endpoints funcionam

---

## O que é SKILL.md na prática?

O `SKILL.md` é um **prompt longo e detalhado** que instrui o agente. Veja a estrutura:

```markdown
# /refactor-arch

## Descrição
Skill para auditoria e refatoração arquitetural de projetos para padrão MVC.

## Trigger
Quando o usuário executar `/refactor-arch`

## Fase 1 — Análise
1. Identifique a linguagem (procure por extensões .py, .js, .ts, etc.)
2. Identifique o framework (leia requirements.txt ou package.json)
3. Mapeie a arquitetura atual
4. Imprima o resumo no formato:
   ```
   PHASE 1: PROJECT ANALYSIS
   Language:      [linguagem]
   Framework:     [framework]
   ...
   ```

## Fase 2 — Auditoria
1. Leia todos os arquivos de código-fonte
2. Para cada arquivo, verifique contra o catálogo de anti-patterns (ver anti-patterns.md)
3. Para cada problema encontrado, registre:
   - Severidade
   - Arquivo e linhas
   - Descrição
   - Impacto
   - Recomendação
4. Gere o relatório no formato do template (ver audit-template.md)
5. PARE e peça confirmação: "Proceed with refactoring? [y/n]"

## Fase 3 — Refatoração
1. Crie a estrutura MVC conforme guidelines (ver mvc-guidelines.md)
2. Para cada anti-pattern encontrado, aplique a transformação do playbook (ver refactoring-playbook.md)
3. Valide:
   - Aplicação inicia sem erros
   - Endpoints respondem corretamente
```

### Os Arquivos de Referência

São documentos Markdown que fornecem **conhecimento de domínio** ao agente:

| Arquivo | Conteúdo |
|---------|----------|
| `anti-patterns.md` | Catálogo com ≥ 8 anti-patterns, cada um com: nome, severidade, sinais de detecção, exemplos de código |
| `mvc-guidelines.md` | Regras da arquitetura MVC: quais camadas existem, o que vai em cada uma |
| `audit-template.md` | Formato exato do relatório de auditoria da Fase 2 |
| `refactoring-playbook.md` | ≥ 8 padrões de transformação com exemplos antes/depois |
| `analysis-heuristics.md` | Como detectar linguagem, framework e banco de dados |

---

## A Importância de Ser Agnóstico de Tecnologia

A Skill deve funcionar para Python/Flask E Node.js/Express. Para isso:

- **Anti-patterns devem ser genéricos**: "God Class" existe em qualquer linguagem
- **Sinais de detecção adaptáveis**: "Arquivo > 200 linhas" funciona em qualquer linguagem
- **Playbook com exemplos em múltiplas linguagens**: Mostre o "antes/depois" em Python E JavaScript
- **Heurísticas de detecção flexíveis**:
  - Python → `requirements.txt`, extensão `.py`
  - Node.js → `package.json`, extensão `.js`

---

## O Relatório de Auditoria

Cada execução gera um relatório salvo em `reports/`:

```markdown
# Architecture Audit Report

## Project Info
- **Project:** code-smells-project
- **Stack:** Python + Flask
- **Files Analyzed:** 4
- **Lines of Code:** ~800

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH | 5 |
| MEDIUM | 2 |
| LOW | 3 |

## Findings

### [CRITICAL] God Class / God Method
- **File:** models.py:1-350
- **Description:** Arquivo único contém toda lógica de negócio...
- **Impact:** Impossível testar em isolamento...
- **Recommendation:** Separar em models e controllers por domínio

### [CRITICAL] Hardcoded Credentials
- **File:** app.py:8
- **Description:** SECRET_KEY hardcoded...
...
```

---

## Ferramentas Aceitas

Você deve usar **UMA** das seguintes ferramentas:

| Ferramenta | Skills Location | Invocação |
|-----------|----------------|-----------|
| **Claude Code** | `.claude/skills/refactor-arch/` | `claude "/refactor-arch"` |
| **Gemini CLI** | Equivalente na Gemini | Adaptar comando |
| **OpenAI Codex** | Equivalente na Codex | Adaptar comando |

> Se usar Gemini CLI ou Codex, a estrutura interna (SKILL.md + arquivos de referência) é a mesma, só muda a pasta e o comando de invocação.

---

## Critérios de Aceite (OBRIGATÓRIOS em todos os 3 projetos)

| Critério | Obrigatório |
|----------|-------------|
| Fase 1 detecta stack corretamente | ✅ 3/3 projetos |
| Fase 2 encontra ≥ 5 findings | ✅ 3/3 projetos |
| Fase 2 inclui ≥ 1 CRITICAL ou HIGH | ✅ 3/3 projetos |
| Fase 3 aplicação funciona após refatoração | ✅ 3/3 projetos |

---

## Possíveis Dificuldades e Como Resolver

| Problema | Causa | Solução |
|---------|-------|---------|
| Skill detecta linguagem errada | Heurísticas genéricas demais | Adicionar mais sinais de detecção (extensões, dependency files) |
| Poucos findings (< 5) | Catálogo de anti-patterns incompleto | Adicionar mais anti-patterns ao catálogo |
| Skill não funciona em Node.js | Referências específicas demais para Python | Usar exemplos multi-linguagem no playbook |
| Aplicação quebra após refatoração | Refatoração incompleta | Adicionar mais validações na Fase 3, instruir a manter funcionalidade |
| Skill não pausa na Fase 2 | Faltou instrução no SKILL.md | Adicionar explicitamente: "PARE aqui e peça confirmação" |
| Relatório sem linhas exatas | SKILL.md não instrui a citar linhas | Instruir: "Sempre cite arquivo:linha(s)" |
