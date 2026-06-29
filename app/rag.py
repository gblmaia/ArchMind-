from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# ==================== CONFIGURAÇÕES ====================
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = OllamaLLM(model="llama3.1", temperature=0)

vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# ==================== PROMPT  ====================
prompt = ChatPromptTemplate.from_template("""
Você é um engenheiro de software sênior com vasta experiência em arquitetura e boas práticas.
Responda à pergunta do usuário **usando apenas o contexto fornecido**.

Regras importantes:
- Se a informação estiver em tabela, leia a tabela completa e extraia os dados de forma precisa.
- NÃO invente nem infira informações que não estejam explicitamente no contexto.
- Se não souber a resposta com base no contexto, diga claramente que não encontrou a informação.
- Seja técnico, direto e objetivo.

CONTEXTO:
{context}

PERGUNSA: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
qa_chain = create_retrieval_chain(retriever, document_chain)


# ==================== FUNÇÃO PRINCIPAL ====================
def ask_archmind(question: str) -> dict:
    """
    Função que recebe uma pergunta e retorna a resposta do RAG
    com fontes limpas e sem duplicatas.
    """
    resposta = qa_chain.invoke({"input": question})

    # Extrai as fontes e remove duplicatas
    fontes_unicas = set()

    if "context" in resposta:
        for doc in resposta["context"]:
            # Pega o nome do arquivo (source) do metadata
            source = doc.metadata.get("source", "desconhecido")

            # Extrai só o nome do arquivo (sem o caminho completo)
            nome_arquivo = source.split("/")[-1] if "/" in source else source.split("\\")[-1]

            fontes_unicas.add(nome_arquivo)

    return {
        "answer": resposta["answer"],
        "sources": list(fontes_unicas)  # Converte de set para lista
    }