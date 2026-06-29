import streamlit as st
from app.rag import ask_archmind

st.set_page_config(page_title="ArchMind", page_icon="🦊", layout="centered")

# ==================== CSS CUSTOMIZADO ====================
st.markdown("""
<style>
    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    .stChatInputContainer {
        padding-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("🦊 ArchMind")
    st.markdown("**Assistente Técnico Inteligente**")
    st.divider()

    st.markdown("### 📌 Sobre o Projeto")
    st.markdown("""
    ArchMind é um assistente baseado em **RAG (Retrieval-Augmented Generation)** 
    que responde perguntas utilizando a documentação técnica do projeto.
    """)

    st.divider()
    st.markdown("### 🛠️ Tecnologias")
    st.markdown("- Python + FastAPI\n- LangChain + Chroma\n- Ollama (Llama 3.1)\n- Streamlit")

    st.divider()
    st.caption("Desenvolvido por Gabriel Alves • 2026")

# ==================== CABEÇALHO ====================
st.title("🦊 ArchMind")
st.markdown("**Assistente Técnico com Memória de Conversa**")
st.caption("Faça perguntas sobre arquitetura, deploy, segurança e tecnologias do projeto.")

st.divider()

# ==================== HISTÓRICO ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🦊"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ==================== INPUT ====================
if prompt := st.chat_input("Digite sua pergunta técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🦊"):
        with st.spinner("Consultando base de conhecimento..."):
            resultado = ask_archmind(prompt)
            answer = resultado["answer"]
            sources = resultado.get("sources", [])

            resposta = answer
            if sources:
                resposta += "\n\n**📚 Fontes consultadas:**\n"
                for s in sources:
                    resposta += f"- `{s}`\n"

            st.markdown(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})