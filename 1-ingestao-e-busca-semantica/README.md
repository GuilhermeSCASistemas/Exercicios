# 📄 Ingestão e Busca Semântica com LangChain e PostgreSQL (pgVector)

Sistema de perguntas e respostas sobre documentos PDF usando o padrão **RAG (Retrieval-Augmented Generation)** com LangChain, Gemini e PostgreSQL + pgVector.

---

## 🏗️ Arquitetura

```
PDF → PyPDFLoader → Chunks (1000/150) → Embeddings (Gemini) → pgVector (PostgreSQL)
                                                                        ↓
Pergunta → Embedding → similarity_search (k=10) → Prompt + Regras → Gemini LLM → Resposta
```

---

## 🛠️ Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- API Key do Google AI Studio (Gemini)

---

## ⚙️ Configuração

### 1. Clone o repositório e entre na pasta

```bash
git clone <url-do-repositorio>
cd 1-ingestao-e-busca-semantica
```

### 2. Crie e ative o ambiente virtual Python

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env e adicione sua GOOGLE_API_KEY
```

---

## 🚀 Ordem de Execução

### Passo 1 — Subir o banco de dados

```bash
docker compose up -d
```

> O banco PostgreSQL com extensão pgVector estará disponível em `localhost:5432`.

### Passo 2 — (Opcional) Gerar um PDF de teste

Se não tiver um PDF, gere o de exemplo:

```bash
pip install fpdf2
python generate_pdf.py
```

Isso cria `document.pdf` com dados fictícios da empresa **SuperTechIABrazil**.

### Passo 3 — Executar a ingestão do PDF

```bash
python src/ingest.py
```

Output esperado:
```
============================================================
  INGESTÃO DE PDF — LangChain + pgVector + Gemini
============================================================

📄 Carregando PDF: document.pdf
   ✅ 3 página(s) carregada(s)

✂️  Dividindo em chunks (tamanho=1000, overlap=150)...
   ✅ 12 chunk(s) gerado(s)

🧠 Configurando embeddings com Gemini (models/embedding-001)...

💾 Salvando vetores no banco de dados (coleção: 'pdf_documents')...

✅ Ingestão concluída! 12 chunk(s) salvos no banco de dados.
```

### Passo 4 — Rodar o chat

```bash
python src/chat.py
```

---

## 💬 Exemplo de Uso

```
============================================================
  CHAT COM PDF — LangChain + pgVector + Gemini
  (Digite 'sair' para encerrar)
============================================================

Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA: O faturamento foi de 10 milhões de reais.

------------------------------------------------------------

Faça sua pergunta:

PERGUNTA: Quantos clientes temos em 2024?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

---

## 📁 Estrutura do Projeto

```
1-ingestao-e-busca-semantica/
├── docker-compose.yml        # PostgreSQL + pgVector
├── requirements.txt          # Dependências Python
├── .env.example              # Template das variáveis de ambiente
├── .env                      # Suas credenciais (NÃO commitar)
├── .gitignore                # Protege o .env e outros arquivos
├── generate_pdf.py           # Script para gerar PDF de teste
├── document.pdf              # PDF para ingestão
├── src/
│   ├── ingest.py             # Script de ingestão do PDF
│   ├── search.py             # Módulo de busca por similaridade
│   └── chat.py               # CLI para interação com usuário
└── README.md
```

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Uso |
|-----------|-----|
| Python 3.10+ | Linguagem principal |
| LangChain | Framework de orquestração |
| Gemini (`models/embedding-001`) | Geração de embeddings |
| Gemini (`gemini-2.0-flash-lite`) | LLM para respostas |
| PostgreSQL 16 + pgVector | Banco de dados vetorial |
| Docker Compose | Execução do banco de dados |

---

## ❓ Troubleshooting

| Erro | Solução |
|------|---------|
| `Connection refused` | Execute `docker compose up -d` |
| `Invalid API Key` | Verifique a `GOOGLE_API_KEY` no `.env` |
| `document.pdf não encontrado` | Execute `python generate_pdf.py` primeiro |
| Respostas inventadas | O prompt de grounding garante respostas apenas pelo contexto |
