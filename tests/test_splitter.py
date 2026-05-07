"""Testes para o módulo de divisão de documentos."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingest import split_documents


def test_split_documents_creates_chunks():
    """Verifica que documentos são divididos em chunks."""
    long_text = "A " * 600  # 1200 caracteres
    documents = [Document(page_content=long_text, metadata={"page": 0})]
    chunks = split_documents(documents)
    assert len(chunks) > 1


def test_split_documents_preserves_metadata():
    """Verifica que metadados são preservados nos chunks."""
    long_text = "Texto de teste. " * 100
    documents = [Document(page_content=long_text, metadata={"page": 0, "source": "test.pdf"})]
    chunks = split_documents(documents)
    for chunk in chunks:
        assert "page" in chunk.metadata
        assert "source" in chunk.metadata


def test_split_documents_chunk_size():
    """Verifica que chunks respeitam o tamanho máximo."""
    long_text = "Palavra " * 500
    documents = [Document(page_content=long_text, metadata={"page": 0})]
    chunks = split_documents(documents)
    for chunk in chunks:
        assert len(chunk.page_content) <= 1000


def test_split_documents_short_text_no_split():
    """Verifica que textos curtos não são divididos."""
    short_text = "Texto curto."
    documents = [Document(page_content=short_text, metadata={"page": 0})]
    chunks = split_documents(documents)
    assert len(chunks) == 1
    assert chunks[0].page_content == short_text


def test_splitter_configuration():
    """Verifica a configuração do splitter (chunk_size e overlap)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    assert splitter._chunk_size == 1000
    assert splitter._chunk_overlap == 150
