# 🦊 ArchMind

**Assistente Técnico Inteligente com RAG**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📑 Índice

- [O que o projeto faz](#-o-que-o-projeto-faz)
- [Arquitetura](#-arquitetura)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Como executar o projeto](#-como-executar-o-projeto)
- [Configuração](#-configuração)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Docker](#-docker)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autor](#-autor)

## ✨ O que o projeto faz

ArchMind permite que usuários façam perguntas em linguagem natural sobre documentação técnica e recebam respostas precisas com as fontes consultadas.

### Principais funcionalidades:

- **RAG (Retrieval-Augmented Generation)**: Recupera informações relevantes dos documentos e gera respostas contextualizadas.
- **Memória de Conversa**: Mantém o contexto entre perguntas para conversas mais naturais.
- **API RESTful**: Endpoint `/chat` para integração com outros sistemas.
- **Interface Web**: Chat interativo via Streamlit.
- **Logs estruturados**: Observabilidade básica para debug e monitoramento.
- **Configuração centralizada**: Gerenciamento de configurações via Pydantic Settings.
- **Dockerizado**: Pronto para execução em ambientes containerizados.

## 🏗️ Arquitetura

O ArchMind segue uma arquitetura modular e bem definida, separando responsabilidades entre diferentes componentes:


    ┌─────────────────────┐
    │   Streamlit (UI)    │
    └──────────┬──────────┘
    │
    ▼
    ┌─────────────────────┐
    │   FastAPI (Backend) │
    └──────────┬──────────┘
    │
    ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │   RAG Pipeline      │──────▶│   Vector Database   │
    │   (LangChain)       │       │   (ChromaDB)        │
    └──────────┬──────────┘       └─────────────────────┘
    │
    ▼
    ┌─────────────────────┐
    │   LLM (Ollama)      │
    └─────────────────────┘



### Componentes principais:

- **Streamlit**: Interface de chat amigável para interação com o assistente.
- **FastAPI**: Camada de API REST que expõe o endpoint `/chat`.
- **RAG Pipeline**: Orquestra recuperação de documentos relevantes + geração de respostas usando LangChain.
- **Vector Database (ChromaDB)**: Armazena os embeddings dos documentos para busca semântica.
- **LLM (Ollama + Llama 3.1)**: Modelo de linguagem responsável por gerar as respostas finais.

## 🛠️ Tecnologias utilizadas

### Backend & API
- **Python 3.11**
- **FastAPI** — Framework web moderno e de alta performance
- **Uvicorn** — Servidor ASGI

### Inteligência Artificial & RAG
- **LangChain** — Framework para construção de aplicações com LLMs
- **Ollama (Llama 3.1)** — Modelo de linguagem executado localmente
- **Hugging Face Embeddings** — Geração de embeddings
- **ChromaDB** — Banco de dados vetorial

### Interface
- **Streamlit** — Interface web interativa para chat

### Infraestrutura & DevOps
- **Docker** + **Docker Compose**
- **Pydantic Settings** — Gerenciamento centralizado de configurações

### Qualidade & Testes
- **Pytest** — Framework de testes
- **Logging estruturado** — Observabilidade básica



## 🚀 Como executar o projeto

### Pré-requisitos

- Python 3.11+
- Docker (opcional, mas recomendado)
- Ollama instalado e rodando com o modelo `llama3.1`

### Instalação

1. Clone o repositório:

 ```bash
git clone https://github.com/seu-usuario/archmind.git
cd archmind 
 ```

2. Crie e ative o ambiente virtual:

 ```
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
 ```
3. Instale as dependências:
```
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

### Executando a aplicação

```bash
Opção 1: Rodar com Python (desenvolvimento)
Bash
```
Opção 2: Rodar com Docker (recomendado)
```bash
docker compose up --build
```

A API estará disponível em: http://localhost:8000
A documentação da API (Swagger) estará em: http://localhost:8000/docs
O Streamlit estará disponível em: http://localhost:8501

## ⚙️ Configuração

O ArchMind utiliza **Pydantic Settings** para gerenciamento centralizado de configurações.

### Variáveis de ambiente disponíveis

| Variável              | Descrição                              | Valor padrão                     |
|-----------------------|----------------------------------------|----------------------------------|
| `LLM_MODEL`           | Nome do modelo utilizado               | `llama3.1`                       |
| `LLM_TEMPERATURE`     | Temperatura do modelo                  | `0.0`                            |
| `OLLAMA_BASE_URL`     | URL base do Ollama                     | `http://localhost:11434`         |
| `CHUNK_SIZE`          | Tamanho dos chunks de texto            | `1000`                           |
| `CHUNK_OVERLAP`       | Sobreposição entre chunks              | `150`                            |
| `EMBEDDING_MODEL`     | Modelo de embeddings                   | `sentence-transformers/all-MiniLM-L6-v2` |
| `DATA_DIRECTORY`      | Diretório dos documentos PDF           | `data/docs`                      |
| `PERSIST_DIRECTORY`   | Diretório do banco vetorial            | `chroma_db`                      |

### Como configurar

1. Crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`, se existir).
2. Defina as variáveis conforme sua necessidade.
3. O sistema carregará automaticamente as configurações.

> **Nota**: Nunca versionar o arquivo `.env` no Git (ele já está no `.gitignore`).

## 📁 Estrutura do projeto

    archmind/
    ├── app/
    │   ├── init.py
    │   ├── main.py                 # FastAPI application
    │   ├── rag.py                  # RAG pipeline logic
    │   ├── ingestion.py            # Document ingestion pipeline
    │   └── logging_config.py       # Logging configuration
    ├── config.py                   # Centralized settings (Pydantic)
    ├── streamlit_app.py            # Streamlit chat interface
    ├── tests/
    │   ├── init.py
    │   ├── test_config.py
    │   └── test_api.py
    ├── data/
    │   └── docs/                   # PDF documents to be ingested
    ├── chroma_db/                  # Vector database (generated)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── .env                        # Environment variables (not committed)
    ├── .gitignore
    └── README.md

## 🧪 Testes

O projeto possui uma suíte de testes automatizados utilizando **Pytest**.

### Executando os testes

```bash
python -m pytest tests/ -v
```

Testes disponíveis

* test_config.py: Valida o carregamento correto das configurações.
* test_api.py: Testa os endpoints da API (/ e /chat).

### Cobertura atual
Os testes cobrem:

* Carregamento de configurações
* Endpoint raiz
* Endpoint de chat (com e sem erros)

Nota: Recomenda-se expandir a cobertura de testes conforme o projeto evolui (especialmente para o pipeline de RAG).

## 🐳 Docker

O projeto está containerizado e pronto para execução via Docker.

### Executar com Docker Compose

```bash
docker compose up --build
```

### Build da imagem

```bash
docker compose build
```

### Estrutura do Dockerfile
O projeto utiliza multi-stage build para gerar uma imagem final menor e mais segura:

* Estágio builder: Instala as dependências
* Estágio runtime: Imagem final otimizada com usuário não-root

### .dockerignore
O arquivo .dockerignore está configurado para evitar copiar arquivos desnecessários durante o build (como venv, __pycache__, chroma_db, etc).

## 🤝 Contribuindo

Contribuições são bem-vindas!

### Como contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrão de commits

Este projeto segue o padrão **Conventional Commits**:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `refactor:` Refatoração de código
- `test:` Adição ou modificação de testes
- `chore:` Tarefas de manutenção

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Gabriel Alves**

- LinkedIn: [linkedin.com/in/gblmaia](https://www.linkedin.com/in/gblmaia)
- GitHub: [github.com/gblmaia](https://github.com/gblmaia)
- Email: gbi.alves556@gmail.com