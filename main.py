import streamlit as st
from src.database import initialize_knowledge_base
from src.agent import generate_adaptive_response

st.set_page_config(page_title="Persona-Adaptive Support Agent", layout="wide")
st.title("🤖 Persona-Adaptive Customer Support Agent")

if "db_initialized" not in st.session_state:
    initialize_knowledge_base()
    st.session_state.db_initialized = True

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Agent Controls")
    if st.button("Reset Chat Session"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Type your support request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        result = generate_adaptive_response(user_input, st.session_state.messages)
        st.markdown(result["response"])
        st.caption(f"**Detected Persona:** {result['persona']} | **Sources:** {', '.join(result['sources'] if result['sources'] else ['None'])}")
        
        if result["escalated"]:
            st.code(result["handoff"], language="json")
            
        st.session_state.messages.append({"role": "assistant", "content": result["response"]})