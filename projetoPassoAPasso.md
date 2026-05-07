# Projeto IA - Ingestão e Busca Semântica

## Fase 1 - Ambiente
- [x] Criar estrutura inicial do projeto
- [x] Criar ambiente virtual
- [x] Configurar requirements.txt
- [x] Configurar .env.example
- [x] Subir PostgreSQL com pgVector via Docker Compose
- [ ] Validar conexão com o banco

## Fase 2 - Primeira feature rodando
- [x] Criar script mínimo de ingestão
- [x] Ler PDF com PyPDFLoader
- [x] Dividir texto com RecursiveCharacterTextSplitter
- [x] Gerar embeddings
- [x] Salvar embeddings no pgVector

## Fase 3 - Busca
- [x] Criar script search.py
- [x] Implementar similarity_search_with_score(query, k=10)
- [x] Montar contexto com os documentos recuperados
- [x] Criar prompt restritivo
- [x] Chamar LLM
- [x] Retornar resposta ao usuário

## Fase 4 - CLI
- [x] Criar chat.py
- [x] Permitir perguntas em loop no terminal
- [x] Permitir sair com "exit", "quit" ou "sair"
- [x] Exibir resposta final no terminal

## Fase 5 - Testes
- [x] Criar testes unitários básicos
- [x] Testar split de documentos
- [x] Testar montagem do prompt
- [x] Testar resposta fora de contexto
- [x] Documentar execução dos testes
