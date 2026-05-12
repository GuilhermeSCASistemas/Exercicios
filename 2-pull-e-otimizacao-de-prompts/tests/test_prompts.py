"""
Testes automatizados para validação do prompt otimizado v2.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_V2_PATH = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")


def load_prompt(file_path: str = PROMPT_V2_PATH):
    """Carrega prompt do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e nao esta vazio."""
        data = load_prompt()
        assert "system_prompt" in data, "Campo 'system_prompt' nao encontrado no YAML"
        assert data["system_prompt"].strip() != "", "system_prompt esta vazio"
        assert len(data["system_prompt"]) > 100, "system_prompt parece muito curto"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (Role Prompting)."""
        data = load_prompt()
        system_prompt = data.get("system_prompt", "")
        role_keywords = [
            "voce e um", "você é um", "voce é um", "você e um",
            "product manager", "especialista", "senior", "especializado"
        ]
        found = any(kw.lower() in system_prompt.lower() for kw in role_keywords)
        assert found, (
            "O prompt nao define uma persona clara. "
            "Use Role Prompting (ex: 'Voce e um Product Manager Senior...')"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato de User Story ou Markdown."""
        data = load_prompt()
        system_prompt = data.get("system_prompt", "")
        format_keywords = [
            "como um", "eu quero", "para que",
            "criterios de aceitacao", "given", "when", "then",
            "dado que", "quando", "entao", "markdown", "user story"
        ]
        count = sum(1 for kw in format_keywords if kw.lower() in system_prompt.lower())
        assert count >= 3, (
            f"O prompt menciona apenas {count} elementos de formato. "
            "Deve exigir o formato padrao de User Story (Como um... Eu quero... Para que...)"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contem exemplos de entrada/saida (Few-shot Learning)."""
        data = load_prompt()
        system_prompt = data.get("system_prompt", "")
        few_shot_indicators = [
            "exemplo", "example", "bug report:", "user story correta",
            "---", "entrada:", "saida:"
        ]
        count = sum(1 for kw in few_shot_indicators if kw.lower() in system_prompt.lower())
        assert count >= 2, (
            "O prompt nao parece conter exemplos Few-shot. "
            "Inclua pelo menos 2-3 exemplos de entrada/saida."
        )

    def test_prompt_no_todos(self):
        """Garante que nao ha [TODO] esquecido no prompt."""
        data = load_prompt()
        system_prompt = data.get("system_prompt", "")
        human_template = data.get("human_template", "")
        assert "[TODO]" not in system_prompt, "system_prompt ainda contem [TODO]"
        assert "TODO" not in system_prompt, "system_prompt ainda contem TODO"
        assert "[TODO]" not in human_template, "human_template ainda contem [TODO]"

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 tecnicas foram declaradas nos metadados do YAML."""
        data = load_prompt()
        techniques = data.get("techniques_applied", [])
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, (
            f"Minimo de 2 tecnicas requeridas. Encontradas: {len(techniques)}. "
            f"Tecnicas: {techniques}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
