"""Testes para a montagem do prompt e resposta fora de contexto."""

from src.search import build_prompt, format_context

from langchain_core.documents import Document


def test_build_prompt_contains_context():
    """Verifica que o prompt contém o contexto fornecido."""
    context = "A empresa XYZ foi fundada em 2010."
    question = "Quando a empresa foi fundada?"
    prompt = build_prompt(context, question)
    assert "A empresa XYZ foi fundada em 2010." in prompt
    assert "Quando a empresa foi fundada?" in prompt


def test_build_prompt_contains_rules():
    """Verifica que o prompt contém as regras restritivas."""
    prompt = build_prompt("contexto", "pergunta")
    assert "CONTEXTO:" in prompt
    assert "REGRAS:" in prompt
    assert "Responda somente com base no CONTEXTO" in prompt
    assert "Não tenho informações necessárias para responder sua pergunta." in prompt
    assert "Nunca invente ou use conhecimento externo" in prompt


def test_build_prompt_contains_examples():
    """Verifica que o prompt contém exemplos de perguntas fora do contexto."""
    prompt = build_prompt("contexto", "pergunta")
    assert "Qual é a capital da França?" in prompt
    assert "PERGUNTA DO USUÁRIO:" in prompt
    assert "RESPONDA A" in prompt


def test_build_prompt_out_of_context_instruction():
    """Verifica instrução para perguntas fora de contexto."""
    prompt = build_prompt("contexto qualquer", "pergunta qualquer")
    expected = "Não tenho informações necessárias para responder sua pergunta."
    assert expected in prompt


def test_format_context_concatenates_documents():
    """Verifica que o contexto é formado pela concatenação dos documentos."""
    results = [
        (Document(page_content="Texto do chunk 1"), 0.9),
        (Document(page_content="Texto do chunk 2"), 0.8),
        (Document(page_content="Texto do chunk 3"), 0.7),
    ]
    context = format_context(results)
    assert "Texto do chunk 1" in context
    assert "Texto do chunk 2" in context
    assert "Texto do chunk 3" in context


def test_format_context_empty_results():
    """Verifica que contexto vazio retorna string vazia."""
    context = format_context([])
    assert context == ""


def test_build_prompt_structure():
    """Verifica a estrutura completa do prompt."""
    context = "Informação relevante."
    question = "Qual a informação?"
    prompt = build_prompt(context, question)

    sections = ["CONTEXTO:", "REGRAS:", "EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:", "PERGUNTA DO USUÁRIO:"]
    for section in sections:
        assert section in prompt
