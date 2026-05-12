"""
chat.py — CLI de Interação com o Usuário

Responsável por:
1. Receber pergunta do usuário via terminal
2. Buscar os 10 chunks mais relevantes no banco vetorial
3. Montar o prompt com contexto e regras
4. Chamar o Gemini (LLM) para gerar a resposta
5. Exibir a resposta formatada
"""

import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Garantir que o módulo search é encontrado (quando executado da raiz)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search import buscar, formatar_contexto

load_dotenv()

# ── Configurações ──────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY não encontrada. Verifique o arquivo .env")

# ── Configurar LLM Gemini ──────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,  # Respostas determinísticas (sem criatividade)
)


def montar_prompt(contexto: str, pergunta: str) -> str:
    """
    Monta o prompt completo com contexto, regras e pergunta do usuário.
    Segue o template exato definido no enunciado do projeto.
    """
    return f"""CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO":"""


def responder(pergunta: str) -> str:
    """
    Pipeline completo: busca → monta prompt → chama LLM → retorna resposta.
    """
    # 1. Buscar os 10 chunks mais relevantes
    resultados = buscar(pergunta, k=10)

    # 2. Formatar o contexto
    contexto = formatar_contexto(resultados)

    # 3. Montar o prompt
    prompt = montar_prompt(contexto, pergunta)

    # 4. Chamar o Gemini
    mensagem = HumanMessage(content=prompt)
    resposta = llm.invoke([mensagem])

    return resposta.content


def main():
    print("=" * 60)
    print("  CHAT COM PDF — LangChain + pgVector + Gemini")
    print("  (Digite 'sair' para encerrar)")
    print("=" * 60)
    print()

    while True:
        print("Faça sua pergunta:")
        print()

        try:
            pergunta = input("PERGUNTA: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Encerrando o chat. Até logo!")
            break

        if not pergunta:
            print("⚠️  Digite uma pergunta válida.\n")
            continue

        if pergunta.lower() in ("sair", "exit", "quit"):
            print("\n👋 Encerrando o chat. Até logo!")
            break

        print()
        print("🔍 Buscando informações relevantes...")

        try:
            resposta = responder(pergunta)
            print(f"\nRESPOSTA: {resposta}")
        except Exception as e:
            print(f"\n❌ Erro ao processar sua pergunta: {e}")
            print("   Verifique se o banco está rodando e o PDF foi ingerido.")

        print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
