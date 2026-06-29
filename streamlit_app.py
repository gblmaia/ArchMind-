import streamlit as st
from app.rag import ask_archmind

st.set_page_config(page_title="ArchMind", page_icon="🦊")
st.title("🦊 ArchMind - Assistente Técnico")

st.markdown("Faça perguntas sobre a documentação técnica do projeto.")

# Histórico de conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta..."):
    # Adiciona mensagem do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chama o ArchMind
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resultado = ask_archmind(prompt)
            resposta = resultado["answer"]
            fontes = resultado["sources"]

            # Monta a resposta final
            resposta_completa = resposta
            if fontes:
                resposta_completa += "\n\n**Fontes:**\n" + "\n".join([f"- {f}" for f in fontes])

            st.markdown(resposta_completa)

    # Adiciona resposta do assistente no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta_completa})