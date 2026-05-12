"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt leonanluppi/bug_to_user_story_v1
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt base (v1) do LangSmith Hub e salva localmente.
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"

    print(f"Buscando prompt: {prompt_name}")

    try:
        prompt = hub.pull(prompt_name)
        print(f"   Prompt carregado com sucesso!")

        # Extrair as mensagens do prompt
        messages = []
        for msg in prompt.messages:
            role = msg.__class__.__name__.replace("MessagePromptTemplate", "").lower()
            if role == "human":
                role = "human"
            elif role == "system":
                role = "system"
            else:
                role = "human"

            # Extrair o template de texto
            if hasattr(msg, 'prompt'):
                content = msg.prompt.template
            elif hasattr(msg, 'content'):
                content = msg.content
            else:
                content = str(msg)

            messages.append({"role": role, "content": content})

        prompt_data = {
            "name": "bug_to_user_story_v1",
            "version": "1.0",
            "description": "Prompt inicial de baixa qualidade para converter bug reports em user stories",
            "source": prompt_name,
            "system_prompt": next(
                (m["content"] for m in messages if m["role"] == "system"),
                messages[0]["content"] if messages else ""
            ),
            "messages": messages,
        }

        Path("prompts").mkdir(exist_ok=True)
        if save_yaml(prompt_data, output_path):
            print(f"   Salvo em: {output_path}")
        else:
            print(f"   Erro ao salvar o arquivo.")

        return prompt_data

    except Exception as e:
        print(f"   Erro ao fazer pull: {e}")
        print("\n   Salvando estrutura do prompt v1 manualmente...")

        # Se não conseguir fazer pull, cria a estrutura do prompt ruim manualmente
        # baseado no que conhecemos do boilerplate
        prompt_data = {
            "name": "bug_to_user_story_v1",
            "version": "1.0",
            "description": "Prompt inicial de baixa qualidade",
            "source": prompt_name,
            "system_prompt": "Converta o bug report em uma user story.",
            "messages": [
                {"role": "system", "content": "Converta o bug report em uma user story."},
                {"role": "human", "content": "{bug_report}"},
            ],
        }
        Path("prompts").mkdir(exist_ok=True)
        save_yaml(prompt_data, output_path)
        print(f"   Estrutura base salva em: {output_path}")
        return prompt_data


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER"]
    if not check_env_vars(required_vars):
        return 1

    result = pull_prompts_from_langsmith()

    if result:
        print("\nPróximos passos:")
        print("1. Analise o prompt em prompts/bug_to_user_story_v1.yml")
        print("2. Crie seu prompt otimizado em prompts/bug_to_user_story_v2.yml")
        print("3. Execute: python src/push_prompts.py")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
