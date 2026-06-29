import logging
from datetime import datetime
from pathlib import Path
import os
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ============================================================
# CONFIGURAÇÃO CENTRAL
# ============================================================
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 150
PERSIST_DIRECTORY: str = "./chroma_db"
DATA_DIRECTORY: Path = Path(os.getcwd()) / "data" / "docs"
# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ArchMind.Ingestion")


def get_embedding_model() -> HuggingFaceEmbeddings:
    """Inicializa o modelo de embeddings de forma controlada."""
    logger.info(f"Carregando modelo de embedding: {EMBEDDING_MODEL_NAME}")
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def ingest_single_pdf(file_path: Path, vectorstore: Optional[Chroma] = None) -> int:
    """
    Processa um único arquivo PDF e o ingere no vector store.
    Retorna a quantidade de chunks processados.
    """
    if not file_path.exists() or not file_path.is_file():
        logger.error(f"Arquivo não encontrado: {file_path}")
        return 0

    logger.info(f"Iniciando ingestão de: {file_path.name}")

    try:
        # 1. Carregamento do documento
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        # 2. Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            add_start_index=True,           # rastreabilidade
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)

        # 3. Enriquecimento de metadados
        ingestion_timestamp = datetime.utcnow().isoformat()
        for chunk in chunks:
            chunk.metadata.update({
                "source": file_path.name,
                "ingested_at": ingestion_timestamp,
                "pipeline_version": "1.0.0-enterprise"
            })

        # 4. Persistência no Chroma
        if vectorstore is None:
            embedding_model = get_embedding_model()
            vectorstore = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=embedding_model
            )

        vectorstore.add_documents(chunks)
        logger.info(f"✓ {len(chunks)} chunks ingeridos com sucesso de {file_path.name}")
        return len(chunks)

    except Exception as e:
        logger.exception(f"Erro crítico ao processar {file_path.name}: {e}")
        return 0


def ingest_directory(directory: Path = DATA_DIRECTORY) -> None:
    """
    Ingere todos os PDFs de um diretório.
    """
    if not directory.exists():
        logger.error(f"Diretório de dados não encontrado: {directory}")
        return

    pdf_files: List[Path] = sorted(directory.glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"Nenhum arquivo PDF encontrado em {directory}")
        return

    logger.info(f"=== Iniciando ingestão em lote | {len(pdf_files)} PDFs encontrados ===")

    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

    total_chunks = 0
    for pdf_file in pdf_files:
        total_chunks += ingest_single_pdf(pdf_file, vectorstore)

    logger.info(f"=== Ingestão concluída | Total de chunks: {total_chunks} ===")
    logger.info(f"Banco vetorial salvo em: {PERSIST_DIRECTORY}")


if __name__ == "__main__":
    logger.info("=== ArchMind Enterprise Ingestion Pipeline ===")
    ingest_directory()