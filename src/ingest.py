"""Módulo de ingestão de PDF para o banco vetorial."""

import os
import sys

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.providers import create_embeddings

load_dotenv()


def load_pdf(pdf_path: str):
    """Carrega o conteúdo de um arquivo PDF."""
    if not os.path.exists(pdf_path):
        print(f"Erro: arquivo '{pdf_path}' não encontrado.")
        sys.exit(1)
    loader = PyPDFLoader(pdf_path)
    return loader.load()


def split_documents(documents):
    """Divide os documentos em chunks menores."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    return splitter.split_documents(documents)


def create_vector_store(embeddings):
    """Cria a instância do PGVector conectada ao banco."""
    database_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("COLLECTION_NAME", "pdf_documents")
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )


def ingest():
    """Executa o pipeline completo de ingestão."""
    pdf_path = os.getenv("PDF_PATH", "document.pdf")

    print(f"Carregando PDF: {pdf_path}")
    documents = load_pdf(pdf_path)
    print(f"Páginas carregadas: {len(documents)}")

    print("Dividindo em chunks...")
    chunks = split_documents(documents)
    print(f"Chunks gerados: {len(chunks)}")

    print("Configurando embeddings...")
    embeddings = create_embeddings()

    print("Conectando ao banco de dados...")
    vector_store = create_vector_store(embeddings)

    print("Salvando embeddings no banco...")
    vector_store.add_documents(chunks)

    print("Ingestão concluída com sucesso!")


if __name__ == "__main__":
    ingest()
