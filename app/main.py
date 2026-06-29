from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.logging_config import setup_logging
from app.rag import ask_archmind

logger = setup_logging()

app = FastAPI(title="ArchMind API", version="1.0")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
    error: bool = False


@app.get("/")
def root():
    return {"message": "ArchMind API está rodando!"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"Nova pergunta recebida: {request.question}")

    try:
        resultado = ask_archmind(request.question)

        return ChatResponse(
            answer=resultado["answer"],
            sources=resultado.get("sources", []),
            error=False
        )

    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {str(e)}")

        return ChatResponse(
            answer="Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente mais tarde.",
            sources=[],
            error=True
        )