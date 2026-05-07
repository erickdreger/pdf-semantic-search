"""Módulo de configuração de providers (OpenAI / Gemini)."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_provider() -> str:
    """Retorna o provider configurado (openai ou gemini)."""
    return os.getenv("LLM_PROVIDER", "openai").lower()


def create_embeddings():
    """Cria a instância de embeddings de acordo com o provider configurado."""
    provider = get_provider()

    if provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model="text-embedding-3-small")


def create_llm():
    """Cria a instância da LLM de acordo com o provider configurado."""
    provider = get_provider()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model="gpt-5-nano")
