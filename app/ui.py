import streamlit as st
from app.core.engine import ShieldEngine
import time

# UI Header
st.set_page_config(page_title="Sentinel-Shield AI Proxy", layout="wide")
st.title("🛡️ Sentinel-Shield: AI Privacy Guardrail")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Settings")
# The mode selected here must be passed to the engine functions
mode = st.sidebar.selectbox("Anonymization Mode", ["replace", "redact", "hash"])
session_id = st.sidebar.text_input("Session ID", value="demo-user-123")
st.sidebar.markdown("---")

# Initialize the Engine
# Note: We initialize once, but we pass the 'mode' during the protect_prompt call
engine = ShieldEngine()

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("User Input")
    user_input = st.text_area("Type a message containing PII (names, emails, IDs):", 
                              placeholder="My name is John Doe and my project is PROJ-555.")
    
    if st.button("Protect & Process"):
        if user_input:
            start_time = time.perf_counter()
            
            # KEY FIX: Pass 'mode' into the function so the engine knows what to do
            masked_text = engine.protect_prompt(session_id, user_input, mode=mode)
            
            end_time = time.perf_counter() 
            latency = (end_time - start_time) * 1000 
            
            st.session_state['masked'] = masked_text
            st.sidebar.metric(label="Shield Latency", value=f"{latency:.2f} ms")
            
            # Step 2: Simulate LLM Response
            # We simulate the LLM replying using the masked text
            llm_sim = f"Acknowledged. I have recorded the details for {masked_text}."
            
            # Step 3: Rehydration (Only works effectively if mode is 'replace')
            if mode == "replace":
                final_output = engine.reconstruct_response(session_id, llm_sim)
            else:
                # For Redact/Hash, rehydration isn't possible by design
                final_output = llm_sim
                
            st.session_state['final'] = final_output

with col2:
    st.subheader("Sentinel-Shield Output")
    if 'masked' in st.session_state:
        st.info(f"**What the LLM sees (Anonymized):**\n\n{st.session_state['masked']}")
        
        if mode == "replace":
            st.success(f"**What the User sees (Rehydrated):**\n\n{st.session_state['final']}")
        else:
            st.warning(f"**Note:** Rehydration is disabled in '{mode}' mode. Data is permanently transformed.")
            st.success(f"**Final Output:**\n\n{st.session_state['final']}")

# Detailed Audit Log view for the Portfolio
if st.checkbox("Show Audit Log Details"):
    st.json({
        "session_id": session_id,
        "mode": mode,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Success"
    })