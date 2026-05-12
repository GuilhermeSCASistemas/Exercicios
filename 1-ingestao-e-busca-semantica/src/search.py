"""
search.py — Script de Busca por Similaridade

Responsável por:
1. Conectar ao banco pgVector
2. Vetorizar a query do usuário com Gemini
3. Buscar os k=10 chunks mais relevantes
4. Retornar os resultados com seus scores
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# ── Configurações ──────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_documents")

# ── Instanciar embeddings e vector store ──────────────────────────────────────
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
)


def buscar(query: str, k: int = 10) -> list[tuple]:
    """
    Busca os k chunks mais similares à query no banco vetorial.

    Args:
        query: Pergunta ou texto de busca do usuário
        k: Número de resultados a retornar (padrão: 10)

    Returns:
        Lista de tuplas (Document, score) ordenadas por relevância
    """
    resultados = vector_store.similarity_search_with_score(query, k=k)
    return resultados


def formatar_contexto(resultados: list[tuple]) -> str:
    """
    Converte os resultados da busca em uma string de contexto
    para ser injetada no prompt da LLM.

    Args:
        resultados: Lista de tuplas (Document, score)

    Returns:
        String com os conteúdos concatenados
    """
    trechos = []
    for doc, score in resultados:
        trechos.append(doc.page_content)

    return "\n\n---\n\n".join(trechos)


if __name__ == "__main__":
    # Teste rápido
    query_teste = "Qual o faturamento da empresa?"
    print(f"🔍 Testando busca com query: '{query_teste}'")
    resultados = buscar(query_teste)
    print(f"   ✅ {len(resultados)} resultado(s) encontrado(s)")
    for i, (doc, score) in enumerate(resultados, 1):
        print(f"\n[Resultado {i}] Score: {score:.4f}")
        print(f"   {doc.page_content[:200]}...")
