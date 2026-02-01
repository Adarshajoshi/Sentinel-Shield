import streamlit as st
from app.core.engine import ShieldEngine

# UI Header
st.set_page_config(page_title="Sentinel-Shield AI Proxy", layout="wide")
st.title("🛡️ Sentinel-Shield: AI Privacy Guardrail")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Settings")
mode = st.sidebar.selectbox("Anonymization Mode", ["replace", "redact", "hash"])
session_id = st.sidebar.text_input("Session ID", value="demo-user-123")
st.sidebar.markdown("---")
st.sidebar.subheader("Live Shield Stats")
st.sidebar.metric(label="Privacy Violations Blocked", value="12", delta="+2 today")

# Initialize the Engine
engine = ShieldEngine(mode=mode)

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("User Input")
    user_input = st.text_area("Type a message containing PII (names, emails, IDs):", 
                              placeholder="My name is John Doe and my project is PROJ-555.")
    
    if st.button("Protect & Process"):
        if user_input:
            # Step 1: Masking (Week 1 & 2 Logic)
            masked_text = engine.protect_prompt(session_id, user_input)
            st.session_state['masked'] = masked_text
            
            # Step 2: Simulate LLM Response (Week 2, Day 2)
            # In a real app, this would call OpenAI/Mistral
            llm_sim = f"Acknowledged. I have recorded the details for {masked_text}."
            
            # Step 3: Rehydration (Week 2, Day 2)
            final_output = engine.reconstruct_response(session_id, llm_sim)
            st.session_state['final'] = final_output

with col2:
    st.subheader("Sentinel-Shield Output")
    if 'masked' in st.session_state:
        st.info(f"**What the LLM sees:**\n\n{st.session_state['masked']}")
        st.success(f"**What the User sees (Rehydrated):**\n\n{st.session_state['final']}")