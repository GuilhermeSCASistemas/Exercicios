"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple:
    """
    Valida estrutura básica de um prompt.

    Returns:
        (is_valid, errors)
    """
    errors = []

    if not prompt_data.get('system_prompt', '').strip():
        errors.append("system_prompt esta vazio ou ausente")

    if 'TODO' in prompt_data.get('system_prompt', ''):
        errors.append("system_prompt ainda contem [TODO]")

    techniques = prompt_data.get('techniques_applied', [])
    if len(techniques) < 2:
        errors.append(f"Minimo 2 tecnicas requeridas. Encontradas: {len(techniques)}")

    if not prompt_data.get('description', '').strip():
        errors.append("description esta vazio")

    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (ex: GuilhermeSCASistemas/bug_to_user_story_v2)
        prompt_data: Dados do prompt lidos do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get('system_prompt', '')
        human_template = prompt_data.get('human_template', '{bug_report}')

        # Montar o ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_template),
        ])

        tags = prompt_data.get('techniques_applied', []) + ['bug-to-user-story', 'optimized']
        description = prompt_data.get('description', '')

        print(f"   Fazendo push para: {prompt_name}")
        print(f"   Tags: {', '.join(tags)}")

        try:
            # Tenta push público primeiro
            hub.push(
                prompt_name,
                prompt_template,
                new_repo_is_public=True,
                new_repo_description=description,
            )
        except Exception as pub_err:
            if "handle" in str(pub_err).lower():
                print("   Aviso: Hub handle publico nao configurado.")
                print("   ACAO NECESSARIA: Acesse https://smith.langchain.com/prompts")
                print("   e crie um prompt publico para gerar seu handle de Hub.")
                print("   Tentando push privado como alternativa...")
                # Tenta push privado (sem new_repo_is_public)
                hub.push(
                    prompt_name,
                    prompt_template,
                    new_repo_description=description,
                )
                print("   Push privado realizado! Torne publico no dashboard.")
            else:
                raise pub_err

        print(f"   Push realizado com sucesso!")
        return True

    except Exception as e:
        print(f"   Erro no push: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    yaml_path = "prompts/bug_to_user_story_v2.yml"

    print(f"Carregando prompt otimizado: {yaml_path}")
    prompt_data = load_yaml(yaml_path)

    if not prompt_data:
        print(f"Erro: nao foi possivel carregar {yaml_path}")
        print("Certifique-se de que o arquivo existe antes de fazer push.")
        return 1

    # Validar
    print("\nValidando prompt...")
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("Prompt invalido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("   Prompt valido!")

    # Push do v2 sem prefixo de username
    prompt_name = "bug_to_user_story_v2"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)

    if success:
        print(f"\nPrompt publicado com sucesso!")
        print(f"   Acesse seu LangSmith Hub para conferir.")
        print(f"\nProximos passos:")
        print(f"   python src/evaluate.py")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
