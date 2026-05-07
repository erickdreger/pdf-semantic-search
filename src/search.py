"""Módulo de busca semântica no banco vetorial."""

import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()


def get_vector_store():
    """Retorna a instância do PGVector conectada ao banco."""
    database_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("COLLECTION_NAME", "pdf_documents")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )


def search_documents(query: str):
    """Busca os documentos mais relevantes para a query.

    Args:
        query: Pergunta do usuário.

    Returns:
        Lista de tuplas (documento, score) ordenadas por relevância.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=10)
    return results


def format_context(results):
    """Formata os resultados da busca em texto de contexto.

    Args:
        results: Lista de tuplas (documento, score).

    Returns:
        String com o conteúdo dos documentos concatenados.
    """
    context_parts = []
    for doc, score in results:
        context_parts.append(doc.page_content)
    return "\n\n".join(context_parts)


def build_prompt(context: str, question: str) -> str:
    """Monta o prompt restritivo com contexto e pergunta.

    Args:
        context: Texto de contexto recuperado do banco.
        question: Pergunta do usuário.

    Returns:
        Prompt formatado para a LLM.
    """
    return f"""CONTEXTO:
{context}

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
{question}

RESPONDA A "PERGUNTA DO USUÁRIO\""""


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python src/search.py 'sua pergunta aqui'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = search_documents(query)

    print(f"\nResultados encontrados: {len(results)}\n")
    for i, (doc, score) in enumerate(results, 1):
        print(f"--- Resultado {i} (score: {score:.4f}) ---")
        print(doc.page_content[:200])
        print()
