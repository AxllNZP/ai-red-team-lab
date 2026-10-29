import streamlit as st
from ollama_client import ask_ollama, SYSTEM_PROMPT

st.set_page_config(page_title="TechStore Assistant", page_icon="💬")
st.title("💬 TechStore - Asistente de Atención al Cliente")

# Inicializar historial de conversación (solo una vez por sesión)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Mostrar historial (sin mostrar el mensaje de sistema al usuario)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Input del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Agregar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Pedir respuesta al modelo y mostrarla
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = ask_ollama(st.session_state.messages)
        st.write(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})