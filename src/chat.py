"""Chat CLI para busca semântica no conteúdo do PDF."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

from src.providers import create_llm
from src.search import build_prompt, format_context, search_documents

load_dotenv()

EXIT_COMMANDS = {"exit", "quit", "sair"}


def ask(question: str, llm) -> str:
    """Processa uma pergunta do usuário.

    Args:
        question: Pergunta do usuário.
        llm: Instância da LLM.

    Returns:
        Resposta da LLM baseada no contexto do PDF.
    """
    results = search_documents(question)

    if not results:
        return "Não tenho informações necessárias para responder sua pergunta."

    context = format_context(results)
    prompt = build_prompt(context, question)
    response = llm.invoke(prompt)
    return response.content


def main():
    """Loop principal do chat CLI."""
    print("=" * 60)
    print("  Chat - Busca Semântica em PDF")
    print("  Digite 'exit', 'quit' ou 'sair' para encerrar.")
    print("=" * 60)
    print()

    llm = create_llm()

    while True:
        try:
            question = input("Faça sua pergunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if not question:
            continue

        if question.lower() in EXIT_COMMANDS:
            print("Encerrando. Até logo!")
            break

        print("\nBuscando resposta...\n")
        answer = ask(question, llm)
        print(f"Resposta: {answer}\n")


if __name__ == "__main__":
    main()
