"""
Script COMPLETO para avaliar prompts otimizados.

Este script:
1. Carrega dataset de avaliação de arquivo .jsonl
2. Cria/atualiza dataset no LangSmith
3. Puxa prompts otimizados do LangSmith Hub
4. Executa prompts contra o dataset
5. Calcula 5 métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
6. Exibe resumo no terminal
"""

import os
import sys
import json
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, format_score, print_section_header, get_llm as get_configured_llm
from metrics import evaluate_f1_score, evaluate_clarity, evaluate_precision

load_dotenv()


def get_llm():
    return get_configured_llm(temperature=0)


def load_dataset_from_jsonl(jsonl_path: str) -> List[Dict[str, Any]]:
    examples = []
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    example = json.loads(line)
                    examples.append(example)
        return examples
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {jsonl_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao parsear JSONL: {e}")
        return []


def create_evaluation_dataset(client: Client, dataset_name: str, jsonl_path: str) -> str:
    print(f"Criando dataset de avaliacao: {dataset_name}...")
    examples = load_dataset_from_jsonl(jsonl_path)

    if not examples:
        print("Nenhum exemplo carregado do arquivo .jsonl")
        return dataset_name

    print(f"   {len(examples)} exemplos carregados de {jsonl_path}")

    try:
        datasets = client.list_datasets(dataset_name=dataset_name)
        existing_dataset = None
        for ds in datasets:
            if ds.name == dataset_name:
                existing_dataset = ds
                break

        if existing_dataset:
            print(f"   Dataset '{dataset_name}' ja existe, usando existente")
            return dataset_name
        else:
            dataset = client.create_dataset(dataset_name=dataset_name)
            for example in examples:
                client.create_example(
                    dataset_id=dataset.id,
                    inputs=example["inputs"],
                    outputs=example["outputs"]
                )
            print(f"   Dataset criado com {len(examples)} exemplos")
            return dataset_name

    except Exception as e:
        print(f"   Aviso ao criar dataset: {e}")
        return dataset_name


def pull_prompt_from_langsmith(prompt_name: str) -> ChatPromptTemplate:
    try:
        print(f"   Puxando prompt do LangSmith Hub: {prompt_name}")
        prompt = hub.pull(prompt_name)
        print(f"   Prompt carregado com sucesso")
        return prompt
    except Exception as e:
        print(f"\nERRO: Nao foi possivel carregar o prompt '{prompt_name}'")
        print("ACOES NECESSARIAS:")
        print("1. Verifique se voce ja fez push: python src/push_prompts.py")
        print(f"2. Confirme em: https://smith.langchain.com/prompts")
        raise


def evaluate_prompt_on_example(
    prompt_template: ChatPromptTemplate,
    example: Any,
    llm: Any
) -> Dict[str, Any]:
    try:
        inputs = example.inputs if hasattr(example, 'inputs') else {}
        outputs = example.outputs if hasattr(example, 'outputs') else {}

        chain = prompt_template | llm
        response = chain.invoke(inputs)
        answer = response.content

        reference = outputs.get("reference", "") if isinstance(outputs, dict) else ""

        if isinstance(inputs, dict):
            question = inputs.get("question", inputs.get("bug_report", inputs.get("pr_title", "N/A")))
        else:
            question = "N/A"

        return {"answer": answer, "reference": reference, "question": question}

    except Exception as e:
        print(f"      Aviso ao avaliar exemplo: {e}")
        return {"answer": "", "reference": "", "question": ""}


def evaluate_prompt(
    prompt_name: str,
    dataset_name: str,
    client: Client
) -> Dict[str, float]:
    print(f"\nAvaliando: {prompt_name}")

    try:
        prompt_template = pull_prompt_from_langsmith(prompt_name)
        examples = list(client.list_examples(dataset_name=dataset_name))
        print(f"   Dataset: {len(examples)} exemplos")

        llm = get_llm()

        f1_scores = []
        clarity_scores = []
        precision_scores = []

        print("   Avaliando exemplos...")

        for i, example in enumerate(examples, 1):
            result = evaluate_prompt_on_example(prompt_template, example, llm)

            if result["answer"]:
                f1 = evaluate_f1_score(result["question"], result["answer"], result["reference"])
                clarity = evaluate_clarity(result["question"], result["answer"], result["reference"])
                precision = evaluate_precision(result["question"], result["answer"], result["reference"])

                f1_scores.append(f1["score"])
                clarity_scores.append(clarity["score"])
                precision_scores.append(precision["score"])

                print(f"      [{i}/{len(examples)}] F1:{f1['score']:.2f} Clarity:{clarity['score']:.2f} Precision:{precision['score']:.2f}")

        avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
        avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.0
        avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0.0

        avg_helpfulness = (avg_clarity + avg_precision) / 2
        avg_correctness = (avg_f1 + avg_precision) / 2

        return {
            "helpfulness": round(avg_helpfulness, 4),
            "correctness": round(avg_correctness, 4),
            "f1_score": round(avg_f1, 4),
            "clarity": round(avg_clarity, 4),
            "precision": round(avg_precision, 4)
        }

    except Exception as e:
        print(f"   Erro na avaliacao: {e}")
        return {
            "helpfulness": 0.0,
            "correctness": 0.0,
            "f1_score": 0.0,
            "clarity": 0.0,
            "precision": 0.0
        }


def display_results(prompt_name: str, scores: Dict[str, float]) -> bool:
    print("\n" + "=" * 50)
    print(f"Prompt: {prompt_name}")
    print("=" * 50)

    print("\nMetricas Derivadas:")
    print(f"  - Helpfulness: {format_score(scores['helpfulness'], threshold=0.9)}")
    print(f"  - Correctness: {format_score(scores['correctness'], threshold=0.9)}")

    print("\nMetricas Base:")
    print(f"  - F1-Score: {format_score(scores['f1_score'], threshold=0.9)}")
    print(f"  - Clarity: {format_score(scores['clarity'], threshold=0.9)}")
    print(f"  - Precision: {format_score(scores['precision'], threshold=0.9)}")

    average_score = sum(scores.values()) / len(scores)

    print("\n" + "-" * 50)
    print(f"MEDIA GERAL: {average_score:.4f}")
    print("-" * 50)

    all_above_threshold = all(score >= 0.9 for score in scores.values())
    passed = all_above_threshold and average_score >= 0.9

    if passed:
        print(f"\nSTATUS: APROVADO - Todas as metricas >= 0.9")
    else:
        print(f"\nSTATUS: REPROVADO")
        failed_metrics = [name for name, score in scores.items() if score < 0.9]
        if failed_metrics:
            print(f"  Metricas abaixo de 0.9: {', '.join(failed_metrics)}")
        print(f"  Media atual: {average_score:.4f} | Necessario: 0.9000")

    return passed


def main():
    print_section_header("AVALIACAO DE PROMPTS OTIMIZADOS")

    provider = os.getenv("LLM_PROVIDER", "openai")
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    eval_model = os.getenv("EVAL_MODEL", "gpt-4o")

    print(f"Provider: {provider}")
    print(f"Modelo Principal: {llm_model}")
    print(f"Modelo de Avaliacao: {eval_model}\n")

    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER"]
    if provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    elif provider in ["google", "gemini"]:
        required_vars.append("GOOGLE_API_KEY")

    if not check_env_vars(required_vars):
        return 1

    client = Client()
    project_name = os.getenv("LANGSMITH_PROJECT", "prompt-optimization-challenge-resolved")

    jsonl_path = "datasets/bug_to_user_story.jsonl"

    if not Path(jsonl_path).exists():
        print(f"Arquivo de dataset nao encontrado: {jsonl_path}")
        return 1

    dataset_name = f"{project_name}-eval"
    create_evaluation_dataset(client, dataset_name, jsonl_path)

    prompts_to_evaluate = [
        "bug_to_user_story_v2",
    ]

    all_passed = True
    results_summary = []

    for prompt_name in prompts_to_evaluate:
        try:
            scores = evaluate_prompt(prompt_name, dataset_name, client)
            passed = display_results(prompt_name, scores)
            all_passed = all_passed and passed
            results_summary.append({"prompt": prompt_name, "scores": scores, "passed": passed})
        except Exception as e:
            print(f"\nFalha ao avaliar '{prompt_name}': {e}")
            all_passed = False
            results_summary.append({
                "prompt": prompt_name,
                "scores": {"helpfulness": 0.0, "correctness": 0.0, "f1_score": 0.0, "clarity": 0.0, "precision": 0.0},
                "passed": False
            })

    print("\n" + "=" * 50)
    print("RESUMO FINAL")
    print("=" * 50 + "\n")
    print(f"Prompts avaliados: {len(results_summary)}")
    print(f"Aprovados: {sum(1 for r in results_summary if r['passed'])}")
    print(f"Reprovados: {sum(1 for r in results_summary if not r['passed'])}\n")

    if all_passed:
        print("Todos os prompts atingiram todas as metricas >= 0.9!")
        print(f"\nConfira em: https://smith.langchain.com/projects/{project_name}")
        return 0
    else:
        print("Alguns prompts nao atingiram todas as metricas >= 0.9")
        print("\nProximos passos:")
        print("1. Refatore os prompts com score baixo")
        print("2. Faca push: python src/push_prompts.py")
        print("3. Execute: python src/evaluate.py novamente")
        return 1


if __name__ == "__main__":
    sys.exit(main())
