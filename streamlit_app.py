import streamlit as st
from app.rag import ask_archmind
import time
import requests
from datetime import datetime


st.set_page_config(
    page_title="ArchMind • Enterprise RAG",
    page_icon="🦊",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==================== CSS PROFISSIONAL ====================
st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }

    .main .block-container {
        max-width: 820px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    h1 {
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        letter-spacing: -0.025em;
    }

    .stCaption {
        color: #64748b !important;
    }

    .stSidebar {
        background-color: #020617;
        border-right: 1px solid #334155;
    }

    .stChatMessage {
        border-radius: 18px !important;
        padding: 18px 22px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.15), 
                    0 4px 6px -4px rgb(0 0 0 / 0.15);
        border: 1px solid #334155;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stChatMessage:hover {
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.15), 
                    0 8px 10px -6px rgb(0 0 0 / 0.15);
        transform: translateY(-1px);
    }

    .stChatInputContainer {
        border-radius: 9999px !important;
        border: 1px solid #475569 !important;
        background-color: #1e2937 !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);
    }

    .stChatInputContainer:focus-within {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.12);
    }

    .stMarkdown strong {
        color: #f97316;
    }

    .streamlit-expanderHeader {
        background-color: #1e2937 !important;
        border-radius: 10px !important;
    }

    .source-card {
        background-color: #1e2937;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 3px solid #f97316;
        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-left-color: #fb923c;
        background-color: #334155;
    }
</style>
""", unsafe_allow_html=True)


# ==================== HEALTH CHECK ====================
def check_ollama_health() -> bool:
    """Verifica conexão com Ollama"""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        return resp.status_code == 200
    except Exception:
        return False


# ==================== SIDEBAR ====================
with st.sidebar:
    # Perfil
    st.markdown("""
    <div style="background-color: #020617; padding: 1rem; border-radius: 14px; border: 1px solid #334155; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 52px; height: 52px; background: linear-gradient(135deg, #f97316, #ea580c); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.2);">
                👨‍💻
            </div>
            <div>
                <div style="font-weight: 700; color: #f1f5f9; font-size: 1.05rem;">Gabriel Alves</div>
                <div style="font-size: 0.78rem; color: #94a3b8;">Backend Júnior • Delfia</div>
                <div style="font-size: 0.72rem; color: #64748b;">Engenharia de Software • FIAP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.title("🦊 ArchMind")
    st.caption("Enterprise Technical RAG")

    st.divider()

    st.markdown("### Sobre")
    st.markdown(
        "Sistema RAG empresarial para consultas técnicas com respostas "
        "verificadas e rastreabilidade de fontes."
    )

    with st.expander("Stack Tecnológico"):
        st.markdown("""
        - FastAPI + LangChain  
        - ChromaDB (vector store)  
        - Ollama  
        - Streamlit  
        - Docker
        """)

    st.divider()

    # ==================== STATUS (atualiza sozinho) ====================
    @st.fragment(run_every="8s")  # aumentei um pouco pra 8s (fica mais leve)
    def status_panel():
        current_ok = check_ollama_health()

        # Inicializa o estado anterior
        if "last_ollama_status" not in st.session_state:
            st.session_state.last_ollama_status = None

        # Só atualiza o visual se o status mudou
        status_changed = current_ok != st.session_state.last_ollama_status

        if status_changed:
            st.session_state.last_ollama_status = current_ok

            # Notificação discreta (opcional, mas fica profissional)
            if current_ok:
                st.toast("Conexão com Ollama restaurada", icon="🟢")
            else:
                st.toast("Conexão com Ollama perdida", icon="🔴")

        # Renderiza o status atual
        if st.session_state.last_ollama_status:
            st.success("🟢 Operacional", icon="✅")
        else:
            st.error("🔴 Ollama Offline", icon="❌")

        st.caption(f"Última verificação: {datetime.now().strftime('%H:%M:%S')}")

    status_panel()

    st.divider()

    if st.button("Limpar conversa", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()


# ==================== HEADER ====================
st.markdown("""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.5rem;">
    <div style="font-size: 2.4rem;">🦊</div>
    <div>
        <h1 style="margin: 0; line-height: 1;">ArchMind</h1>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">Enterprise RAG • Fontes verificadas</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==================== CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Boas-vindas
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 1rem 0.5rem;">
        <h3 style="color: #f1f5f9; margin-bottom: 0.3rem;">Bem-vindo</h3>
        <p style="color: #94a3b8; max-width: 420px; margin: 0 auto;">
            Assistente técnico com RAG. Faça suas perguntas sobre documentação, 
            arquitetura, segurança ou boas práticas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Perguntas sugeridas**")
    col1, col2 = st.columns(2)

    suggestions = [
        "Quais são as melhores práticas de autenticação e autorização em APIs REST?",
        "Como implementar rate limiting e proteção contra brute force de forma segura?",
        "Explique o padrão Circuit Breaker com exemplos práticos em Python."
    ]

    with col1:
        if st.button(suggestions[0], use_container_width=True, key="sug1"):
            st.session_state.messages.append({"role": "user", "content": suggestions[0]})
            st.rerun()
        if st.button(suggestions[2], use_container_width=True, key="sug3"):
            st.session_state.messages.append({"role": "user", "content": suggestions[2]})
            st.rerun()

    with col2:
        if st.button(suggestions[1], use_container_width=True, key="sug2"):
            st.session_state.messages.append({"role": "user", "content": suggestions[1]})
            st.rerun()


# Histórico de mensagens
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🦊"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# Input do usuário
if prompt := st.chat_input("Pergunte sobre a documentação técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🦊"):
        thinking = st.empty()
        with thinking.container():
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; color: #94a3b8;">
                <span style="font-size: 1.3rem;">🦊</span>
                <span>Consultando base de conhecimento...</span>
            </div>
            """, unsafe_allow_html=True)

        start_time = time.time()
        resultado = ask_archmind(prompt)
        elapsed = time.time() - start_time
        thinking.empty()

        resposta = resultado["answer"]
        sources = resultado.get("sources", [])

        st.markdown(resposta)
        st.caption(f"Respondido em {elapsed:.2f}s • {len(sources)} fonte(s) consultadas")

        if sources:
            with st.expander("Fontes consultadas", expanded=False):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <strong style="color:#f97316;">[{i}]</strong> 
                        <code style="color:#e2e8f0; font-size: 0.9rem;">{source}</code>
                    </div>
                    """, unsafe_allow_html=True)

        # Feedback
        fb1, fb2, _ = st.columns([0.7, 0.7, 5])
        with fb1:
            if st.button("👍", key=f"like_{len(st.session_state.messages)}"):
                st.toast("Feedback registrado.")
        with fb2:
            if st.button("👎", key=f"dislike_{len(st.session_state.messages)}"):
                st.toast("Feedback registrado.")

    resposta_hist = resposta
    if sources:
        resposta_hist += f"\n\n({len(sources)} fonte(s) consultadas)"

    st.session_state.messages.append({"role": "assistant", "content": resposta_hist})