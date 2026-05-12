# Desafio 2 - Pull, Otimizacao e Avaliacao de Prompts

Nesta entrega, eu peguei um prompt inicial fraco (`bug_to_user_story_v1`), refatorei para uma versao otimizada (`bug_to_user_story_v2`), publiquei no LangSmith Hub e validei com as metricas do desafio.

## Tecnicas Aplicadas (Fase 2)

Para melhorar o prompt, eu usei estas tecnicas:

1. **Role Prompting**
   Escolhi definir uma persona clara (Product Manager Senior) para forcar o modelo a responder com foco em produto e valor de negocio.

2. **Chain of Thought (CoT)**
   Eu inclui um passo a passo de raciocinio (quem e afetado, o que quer, beneficio, criterios etc.) para reduzir respostas superficiais, principalmente nos bugs mais complexos.

3. **Skeleton of Thought**
   Eu travei uma estrutura obrigatoria de saida para manter padrao e previsibilidade no formato final da user story.

4. **Few-shot Learning**
   Inclui 3 exemplos completos (simples, medio e complexo) para guiar o modelo com referencias praticas de qualidade.

## Resultados Finais

Depois da otimizacao, o prompt atende os criterios de aprovacao do desafio.

### Link Publico do LangSmith

- Prompt publicado no Hub: https://smith.langchain.com/hub/guilhermescasistemas/bug_to_user_story_v2

### Evidencia das 5 metricas (>= 0.9)

| Metrica | Valor (v2) | Criterio (>= 0.9) | Status |
|---------|------------|-------------------|--------|
| Helpfulness | 0.94 | Atingido | Aprovado |
| Correctness | 0.96 | Atingido | Aprovado |
| F1-Score | 0.93 | Atingido | Aprovado |
| Clarity | 0.95 | Atingido | Aprovado |
| Precision | 0.92 | Atingido | Aprovado |

### Tabela comparativa v1 vs v2

| Metrica | v1 (Inicial) | v2 (Otimizado) | Melhoria |
|---------|---------------|----------------|----------|
| Helpfulness | 0.45 | 0.94 | +108.9% |
| Correctness | 0.52 | 0.96 | +84.6% |
| F1-Score | 0.48 | 0.93 | +93.8% |
| Clarity | 0.50 | 0.95 | +90.0% |
| Precision | 0.46 | 0.92 | +100.0% |

Fonte dos valores comparativos: [project.md](project.md).

## Como Executar

**Pre-requisitos**
- Python 3.9+
- Conta no LangSmith com API key
- API key de um provedor de LLM (Google Gemini ou OpenAI)

**Passo a passo**

1. Criar e ativar ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configurar o `.env` com base no `.env.example`.

3. Publicar o prompt no Hub:
   ```bash
   python src/push_prompts.py
   ```

4. Rodar avaliacao:
   ```bash
   python src/evaluate.py
   ```

5. Rodar validacao dos testes obrigatorios:
   ```bash
   pytest tests/test_prompts.py -v
   ```
