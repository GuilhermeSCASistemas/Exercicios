"""
ingest.py — Script de Ingestão de PDF

Responsável por:
1. Carregar o PDF (document.pdf)
2. Dividir em chunks (1000 chars, overlap 150)
3. Gerar embeddings com Gemini
4. Salvar os vetores no PostgreSQL com pgVector
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

# Carregar variáveis de ambiente do .env
load_dotenv()

# ── Configurações ──────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_documents")
PDF_PATH = "document.pdf"

# ── Validações iniciais ────────────────────────────────────────────────────────
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY não encontrada. Verifique o arquivo .env")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"❌ Arquivo '{PDF_PATH}' não encontrado na raiz do projeto.")


def main():
    print("=" * 60)
    print("  INGESTÃO DE PDF — LangChain + pgVector + Gemini")
    print("=" * 60)

    # ── Passo 1: Carregar o PDF ────────────────────────────────────────────────
    print(f"\n📄 Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"   ✅ {len(documents)} página(s) carregada(s)")

    # ── Passo 2: Dividir em chunks ─────────────────────────────────────────────
    print("\n✂️  Dividindo em chunks (tamanho=1000, overlap=150)...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documents)
    print(f"   ✅ {len(chunks)} chunk(s) gerado(s)")

    # ── Passo 3: Configurar embeddings com Gemini ─────────────────────────────
    print("\n🧠 Configurando embeddings com Gemini (models/embedding-001)...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    # ── Passo 4: Salvar vetores no PostgreSQL + pgVector ──────────────────────
    print(f"\n💾 Salvando vetores no banco de dados (coleção: '{COLLECTION_NAME}')...")
    print("   (isso pode levar alguns segundos...)")

    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,  # Limpa dados antigos antes de reingerir
    )

    print(f"\n✅ Ingestão concluída! {len(chunks)} chunk(s) salvos no banco de dados.")
    print("   Agora você pode executar: python src/chat.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
