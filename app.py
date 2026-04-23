import streamlit as st
import time
from src.mitigate import mitigate_bias

# Page Config
st.set_page_config(page_title="AI Bias Guard", page_icon="🛡️", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
    }
    .bias-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .highlight {
        color: #e74c3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ AI Bias Guard")
st.markdown("### Responsible AI: Detect and Mitigate Bias with Unified GenAI.")
st.divider()

# Input area
with st.container():
    sentence = st.text_input("Analyze sentence for potential social bias:", placeholder="e.g., Doctors are usually men.")
    analyze_btn = st.button("Analyze & Mitigate")

if analyze_btn and sentence:
    with st.spinner("Analyzing..."):
        start_time = time.time()
        result = mitigate_bias(sentence)
        gen_time = time.time() - start_time
        
        score = result.get("bias_score", 0.0)
        is_biased = result.get("is_biased", False)
        bias_type = result.get("bias_type", "None")
        corrected = result.get("mitigated_sentence", sentence)
    
    # Results Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Bias Confidence", f"{score*100:.1f}%")
        if is_biased:
            st.error("⚠️ Bias Detected")
        else:
            st.success("✅ Looks Neutral")

    with col2:
        if is_biased:
            st.markdown(f"**Detected Gaps:** {bias_type}")
            
            with st.expander("✨ Mitigated Result", expanded=True):
                st.info(corrected)
                st.caption(f"Processed in {gen_time:.2f}s using Local Pipeline.")
            
            st.divider()
            st.markdown("**AI Reasoning:**")
            st.write("This sentence contains patterns that reflect historical or social biases based on zero-shot classification and lexical matching. The mitigated version uses a locally trained T5 model to provide an inclusive alternative.")
        else:
            st.info("The algorithm did not find significant stereotypical patterns (Score < 30%). It appears broadly neutral and inclusive. No mitigation applied.")

st.sidebar.title("About the System")
st.sidebar.info(f"""
**Architecture (Fully Local):**
- **Detection:** `facebook/bart-large-mnli` (Zero-shot NLP) + Lexical rules for accurate scoring.
- **Mitigation:** Fine-tuned `t5-small` model rewrites strictly when bias is detected.
- **Workflow:** Real-time scoring and offline robust contextual rewriting without API dependency.

**Project Goal:**
Provide a powerful, production-ready pipeline that guarantees accurate detection scores (preventing false negatives on known stereotypes) and cleans biased logic using offline AI.
""")

st.sidebar.success("✅ This system operates entirely locally and requires no API keys.")