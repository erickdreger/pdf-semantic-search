# Projeto IA - Ingestão e Busca Semântica

## Fase 1 - Ambiente
- [x] Criar estrutura inicial do projeto
- [ ] Criar ambiente virtual
- [x] Configurar requirements.txt
- [x] Configurar .env.example
- [ ] Subir PostgreSQL com pgVector via Docker Compose
- [ ] Validar conexão com o banco

## Fase 2 - Primeira feature rodando
- [ ] Criar script mínimo de ingestão
- [ ] Ler PDF com PyPDFLoader
- [ ] Dividir texto com RecursiveCharacterTextSplitter
- [ ] Gerar embeddings
- [ ] Salvar embeddings no pgVector

## Fase 3 - Busca
- [ ] Criar script search.py
- [ ] Implementar similarity_search_with_score(query, k=10)
- [ ] Montar contexto com os documentos recuperados
- [ ] Criar prompt restritivo
- [ ] Chamar LLM
- [ ] Retornar resposta ao usuário

## Fase 4 - CLI
- [ ] Criar chat.py
- [ ] Permitir perguntas em loop no terminal
- [ ] Permitir sair com "exit", "quit" ou "sair"
- [ ] Exibir resposta final no terminal

## Fase 5 - Testes
- [ ] Criar testes unitários básicos
- [ ] Testar split de documentos
- [ ] Testar montagem do prompt
- [ ] Testar resposta fora de contexto
- [ ] Documentar execução dos testes
