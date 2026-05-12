"""
Módulo de métricas customizadas para avaliação de prompts.

MÉTRICAS GERAIS (3):
1. F1-Score: Balanceamento entre Precision e Recall
2. Clarity: Clareza e estrutura da resposta
3. Precision: Informações corretas e relevantes

Suporta múltiplos providers:
- OpenAI (gpt-4o, gpt-4o-mini)
- Google Gemini (gemini-2.5-flash)
"""

import os
import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from utils import get_eval_llm

load_dotenv()


def get_evaluator_llm():
    return get_eval_llm(temperature=0)


def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """Extrai JSON de uma resposta de LLM que pode conter texto adicional."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end > start:
            try:
                json_str = response_text[start:end]
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        print(f"Nao foi possivel extrair JSON: {response_text[:200]}...")
        return {"score": 0.0, "reasoning": "Erro ao processar resposta"}


def evaluate_f1_score(question: str, answer: str, reference: str) -> Dict[str, Any]:
    """Calcula F1-Score usando LLM-as-Judge."""
    evaluator_prompt = f"""
Voce e um avaliador especializado em medir a qualidade de respostas geradas por IA.

Sua tarefa e calcular PRECISION e RECALL para determinar o F1-Score.

PERGUNTA DO USUARIO:
{question}

RESPOSTA ESPERADA (Ground Truth):
{reference}

RESPOSTA GERADA PELO MODELO:
{answer}

INSTRUCOES:

1. PRECISION (0.0 a 1.0):
   - Quantas informacoes na resposta gerada sao CORRETAS e RELEVANTES?
   - Penalizar informacoes incorretas, inventadas ou desnecessarias
   - 1.0 = todas informacoes sao corretas e relevantes

2. RECALL (0.0 a 1.0):
   - Quantas informacoes da resposta esperada estao PRESENTES na resposta gerada?
   - Penalizar informacoes importantes que foram omitidas
   - 1.0 = todas informacoes importantes estao presentes

3. RACIOCINIO: Explique brevemente sua avaliacao

IMPORTANTE: Retorne APENAS um objeto JSON valido no formato:
{{
  "precision": <valor entre 0.0 e 1.0>,
  "recall": <valor entre 0.0 e 1.0>,
  "reasoning": "<sua explicacao em ate 100 palavras>"
}}

NAO adicione nenhum texto antes ou depois do JSON.
"""
    try:
        llm = get_evaluator_llm()
        response = llm.invoke([HumanMessage(content=evaluator_prompt)])
        result = extract_json_from_response(response.content)

        precision = float(result.get("precision", 0.0))
        recall = float(result.get("recall", 0.0))

        if (precision + recall) > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0

        return {
            "score": round(f1_score, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "reasoning": result.get("reasoning", "")
        }
    except Exception as e:
        print(f"Erro ao avaliar F1-Score: {e}")
        return {"score": 0.0, "precision": 0.0, "recall": 0.0, "reasoning": str(e)}


def evaluate_clarity(question: str, answer: str, reference: str) -> Dict[str, Any]:
    """Avalia a clareza e estrutura da resposta usando LLM-as-Judge."""
    evaluator_prompt = f"""
Voce e um avaliador especializado em medir a CLAREZA de respostas geradas por IA.

PERGUNTA DO USUARIO:
{question}

RESPOSTA GERADA PELO MODELO:
{answer}

RESPOSTA ESPERADA (Referencia):
{reference}

INSTRUCOES:

Avalie a CLAREZA da resposta gerada com base nos criterios:

1. ORGANIZACAO (0.0 a 1.0): A resposta tem estrutura logica e bem organizada?
2. LINGUAGEM (0.0 a 1.0): Usa linguagem simples e direta? Facil de entender?
3. AUSENCIA DE AMBIGUIDADE (0.0 a 1.0): A resposta e clara e sem ambiguidades?
4. CONCISAO (0.0 a 1.0): E concisa sem ser curta demais?

Calcule a MEDIA dos 4 criterios para obter o score final.

IMPORTANTE: Retorne APENAS um objeto JSON valido no formato:
{{
  "score": <valor entre 0.0 e 1.0>,
  "reasoning": "<explicacao detalhada em ate 100 palavras>"
}}

NAO adicione nenhum texto antes ou depois do JSON.
"""
    try:
        llm = get_evaluator_llm()
        response = llm.invoke([HumanMessage(content=evaluator_prompt)])
        result = extract_json_from_response(response.content)
        score = float(result.get("score", 0.0))
        return {"score": round(score, 4), "reasoning": result.get("reasoning", "")}
    except Exception as e:
        print(f"Erro ao avaliar Clarity: {e}")
        return {"score": 0.0, "reasoning": str(e)}


def evaluate_precision(question: str, answer: str, reference: str) -> Dict[str, Any]:
    """Avalia a precisão da resposta usando LLM-as-Judge."""
    evaluator_prompt = f"""
Voce e um avaliador especializado em detectar PRECISAO e ALUCINACOES em respostas de IA.

PERGUNTA DO USUARIO:
{question}

RESPOSTA GERADA PELO MODELO:
{answer}

RESPOSTA ESPERADA (Ground Truth):
{reference}

INSTRUCOES:

Avalie a PRECISAO da resposta gerada:

1. AUSENCIA DE ALUCINACOES (0.0 a 1.0): A resposta contem informacoes INVENTADAS?
2. FOCO NA PERGUNTA (0.0 a 1.0): A resposta responde EXATAMENTE o que foi perguntado?
3. CORRECAO FACTUAL (0.0 a 1.0): As informacoes estao CORRETAS comparadas com a referencia?

Calcule a MEDIA dos 3 criterios para obter o score final.

IMPORTANTE: Retorne APENAS um objeto JSON valido no formato:
{{
  "score": <valor entre 0.0 e 1.0>,
  "reasoning": "<explicacao detalhada em ate 100 palavras, cite exemplos>"
}}

NAO adicione nenhum texto antes ou depois do JSON.
"""
    try:
        llm = get_evaluator_llm()
        response = llm.invoke([HumanMessage(content=evaluator_prompt)])
        result = extract_json_from_response(response.content)
        score = float(result.get("score", 0.0))
        return {"score": round(score, 4), "reasoning": result.get("reasoning", "")}
    except Exception as e:
        print(f"Erro ao avaliar Precision: {e}")
        return {"score": 0.0, "reasoning": str(e)}
