import streamlit as st
from app.rag import ask_archmind
import time
import requests
from datetime import datetime

st.set_page_config(
    page_title="ArchMind • Enterprise RAG",
    page_icon="assets/icons/archmind_icon_1024x1024.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================== CSS PROFISSIONAL ====================
st.markdown("""
<style>
    /* ==================================================== */
    /* === TÁTICA NUCLEAR CONTRA O MENU DO STREAMLIT === */
    /* ==================================================== */

    /* Garante o fundo cobrindo tudo */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b1120 !important;
    }

    /* Fundo do cabeçalho invisível para não dar faixa feia */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Esconde as ações do topo direito (Deploy, Menu, Github) */
    [data-testid="stHeaderActions"], 
    [data-testid="stHeaderActionElements"], 
    [data-testid="stAppDeployButton"], 
    .stAppDeployButton,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    /* Some com o rodapé */
    footer { 
        display: none !important;
        visibility: hidden !important; 
    }

    /* ==================================================== */

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
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }

    section[data-testid="stSidebar"] {
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
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
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        return resp.status_code == 200
    except Exception:
        return False


# ==================== SIDEBAR ====================
with st.sidebar:
    # =====================================================
    # === ÍCONE DO TOPO DA SIDEBAR ===
    # =====================================================
    st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)
    col_esq, col_centro, col_dir = st.columns([1, 1.2, 1])
    with col_centro:
        st.image("assets/icons/archmind_icon_1024x1024.png", width=120)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span style="font-size: 0.82rem; font-weight: 600; color: #64748b;">Enterprise RAG</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # === PERFIL DO GABRIEL ===
    st.markdown("""
    <div style="background-color: #0f172a; padding: 13px 15px; border-radius: 16px; 
                border: 1px solid #334155; margin-bottom: 1.1rem; 
                box-shadow: 0 10px 10px -3px rgb(0 0 0 / 0.1);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 50px; height: 50px; background: #f97316; 
                        border-radius: 9999px; display: flex; align-items: center; justify-content: center; 
                        font-size: 1.55rem; box-shadow: 0 0 0 5px rgba(249, 115, 22, 0.2); flex-shrink: 0;">
                💻
            </div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-weight: 700; color: #f1f5f9; font-size: 1.05rem; line-height: 1.15;">Gabriel Alves</div>
                <div style="font-size: 0.77rem; color: #94a3b8; margin-top: 2px;">Software Engineer JR</div>
                <div style="font-size: 0.70rem; color: #64748b; margin-top: 1px;">Engenharia de Software • FIAP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === SOBRE ===
    st.markdown("### Sobre")
    st.markdown("""
    <span style="color:#cbd5e1; font-size:0.89rem; line-height:1.55;">
        Sistema RAG empresarial para consultas técnicas com respostas verificadas 
        e rastreabilidade de fontes.
    </span>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 0.3rem'></div>", unsafe_allow_html=True)

    # === STACK ===
    with st.expander("Stack Tecnológico"):
        st.markdown("""
        - **FastAPI** + LangChain  
        - **ChromaDB** (vector store)  
        - **Ollama** - **Streamlit** - **Docker**
        """)

    st.divider()


    # === STATUS ===
    @st.fragment(run_every="8s")
    def status_panel():
        current_ok = check_ollama_health()

        if "last_ollama_status" not in st.session_state:
            st.session_state.last_ollama_status = None

        status_changed = current_ok != st.session_state.last_ollama_status

        if status_changed:
            st.session_state.last_ollama_status = current_ok
            if current_ok:
                st.toast("Conexão com Ollama restaurada", icon="🟢")
            else:
                st.toast("Conexão com Ollama perdida", icon="🔴")

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

# ==================== CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

has_conversation = len(st.session_state.messages) > 0

if has_conversation:
    col_icon, col_title = st.columns([0.12, 0.88], vertical_alignment="center")
    with col_icon:
        st.image("assets/icons/archmind_icon_1024x1024.png", width=42)
    with col_title:
        st.markdown("""
        <div style="margin-top: 4px;">
            <h1 style="margin: 0; line-height: 1;">ArchMind</h1>
            <p style="margin: 0; color: #475569; font-size: 0.82rem;">Enterprise RAG • Fontes verificadas</p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()

if not has_conversation:
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # =====================================================
    # === ÍCONE GRANDE DA TELA DE BOAS-VINDAS ===
    # =====================================================
    col1, col2, col3 = st.columns([1, 0.45, 1])
    with col2:
        st.image("assets/icons/archmind_icon_1024x1024.png", width=160)

    st.markdown("""
    <div style="text-align: center; padding-top: 0.8rem;">
        <h2 style="color: #f1f5f9; margin-bottom: 0.35rem;">Bem-vindo ao ArchMind</h2>
        <p style="color: #94a3b8; max-width: 460px; margin: 0 auto 2.2rem; line-height: 1.55;">
            Assistente técnico com RAG para consultas sobre arquitetura, 
            modelagem de dados, sistemas de alerta e resiliência.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Perguntas sugeridas**")
    col1, col2 = st.columns(2)

    suggestions = [
        "Como modelar eventos de desastre com suporte eficiente a consultas geoespaciais?",
        "Quais estratégias de rate limiting e backpressure usar em sistemas de alerta em tempo real?",
        "Como garantir idempotência e tratamento confiável de falhas em webhooks?",
        "Quais padrões de observabilidade são mais eficazes em sistemas distribuídos de alerta?"
    ]

    col1, col2 = st.columns(2)

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

        if st.button(suggestions[3], use_container_width=True, key="sug4"):
            st.session_state.messages.append({"role": "user", "content": suggestions[3]})
            st.rerun()

# ==================== RENDERIZAÇÃO DO HISTÓRICO ====================
for idx, message in enumerate(st.session_state.messages):
    avatar = "🧑‍💻" if message["role"] == "user" else "🦊"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

        # Se for uma resposta do assistente, renderiza os metadados salvos
        if message["role"] == "assistant" and "elapsed" in message:
            st.caption(f"Respondido em {message['elapsed']:.2f}s • {len(message['sources'])} fonte(s) consultadas")

            if message["sources"]:
                with st.expander("Fontes consultadas", expanded=False):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong style="color:#f97316;">[{i}]</strong> 
                            <code style="color:#e2e8f0; font-size: 0.9rem;">{source}</code>
                        </div>
                        """, unsafe_allow_html=True)

            fb1, fb2, _ = st.columns([0.7, 0.7, 5])
            with fb1:
                if st.button("👍", key=f"hist_like_{idx}"):
                    st.toast("Feedback registrado.")
            with fb2:
                if st.button("👎", key=f"hist_dislike_{idx}"):
                    st.toast("Feedback registrado.")

# ==================== NOVA CONSULTA ====================
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

        # O índice para os botões da nova mensagem é o tamanho atual da lista
        current_idx = len(st.session_state.messages)
        fb1, fb2, _ = st.columns([0.7, 0.7, 5])
        with fb1:
            if st.button("👍", key=f"hist_like_{current_idx}"):
                st.toast("Feedback registrado.")
        with fb2:
            if st.button("👎", key=f"hist_dislike_{current_idx}"):
                st.toast("Feedback registrado.")

    # Salva todos os detalhes na memória da sessão para não sumirem no recarregamento
    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta,
        "elapsed": elapsed,
        "sources": sources
    })