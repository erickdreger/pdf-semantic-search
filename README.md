# PDF Semantic Search

Projeto de IA para ingestão de PDF e busca semântica usando LangChain, PostgreSQL e pgVector.

## Funcionalidades

- Leitura e processamento de arquivos PDF
- Divisão do conteúdo em chunks otimizados (1000 caracteres, overlap de 150)
- Geração de embeddings com OpenAI (`text-embedding-3-small`) ou Gemini (`models/embedding-001`)
- Armazenamento vetorial no PostgreSQL com pgVector
- Busca semântica com similaridade vetorial
- Chat CLI para perguntas sobre o conteúdo do PDF
- Respostas restritas ao conteúdo do documento (sem invenção de informações)
- Suporte a múltiplos providers (OpenAI e Gemini) via variável de ambiente

## Tecnologias

- Python
- LangChain
- PostgreSQL + pgVector
- Docker / Docker Compose
- OpenAI (embeddings + LLM) ou Google Gemini

## Estrutura do Projeto

```
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   ├── chat.py
│   └── providers.py
├── tests/
│   ├── test_prompt.py
│   └── test_splitter.py
├── document.pdf
├── projetoPassoAPasso.md
└── README.md
```

## Instalação e Configuração

### 1. Criar e ativar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env` e configure o provider desejado:

```
# Para OpenAI:
OPENAI_API_KEY=sua-chave-aqui
LLM_PROVIDER=openai

# Para Gemini:
GOOGLE_API_KEY=sua-chave-aqui
LLM_PROVIDER=gemini

# Configurações do banco:
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/vectordb
COLLECTION_NAME=pdf_documents
PDF_PATH=document.pdf
```

### 4. Subir o banco de dados

```bash
docker compose up -d
```

Isso inicia o PostgreSQL com a extensão pgVector na porta 5432.

### 5. Adicionar o PDF

Coloque o arquivo PDF que deseja processar na raiz do projeto com o nome `document.pdf` (ou altere a variável `PDF_PATH` no `.env`).

### 6. Executar a ingestão

```bash
python src/ingest.py
```

Este comando lê o PDF, divide em chunks, gera embeddings e salva no PostgreSQL.

### 7. Rodar o chat

```bash
python src/chat.py
```

Faça perguntas sobre o conteúdo do PDF no terminal. Para sair, digite `exit`, `quit` ou `sair`.

### 8. Rodar os testes

```bash
pytest
```

## Comportamento Esperado

- Perguntas sobre o conteúdo do PDF retornam respostas baseadas no documento.
- Perguntas fora do contexto retornam:
  > "Não tenho informações necessárias para responder sua pergunta."

## Troca de Provider (OpenAI / Gemini)

O provider é controlado pela variável `LLM_PROVIDER` no `.env`:

- `LLM_PROVIDER=openai` (padrão): Usa OpenAI (`text-embedding-3-small` + `gpt-5-nano`)
- `LLM_PROVIDER=gemini`: Usa Google Gemini (`models/gemini-embedding-001` + `gemini-2.5-flash`)

A lógica de seleção está centralizada em `src/providers.py`.
