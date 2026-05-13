import streamlit as st
import time
import os

# Removed PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION workaround as it degrades performance
# on macOS arm64 when parsing large models.
from detector.mitigation import process_paragraph
from detector.ai_engine import get_active_provider

# ── Page Config (must be first Streamlit call) ──────────────────────────
st.set_page_config(
    page_title="AI Bias Guard",
    page_icon="🛡️",
    layout="wide"
)

# ── Load Custom CSS ─────────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── Session State ───────────────────────────────────────────────────────
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "inference_time" not in st.session_state:
    st.session_state.inference_time = 0.0
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ── Hide Sidebar Button (Presentation Mode) ─────────────────────────────
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid='stSidebarNav'] {display: none;} [data-testid='stSidebar'] {display: none;} .st-emotion-cache-1vq4p4l {display: none;}</style>", unsafe_allow_html=True)


# ── Header ──────────────────────────────────────────────────────────────
st.markdown("<h1>🛡️ BiasGuard AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Enterprise-grade semantic bias detection &amp; automated neutral rewriting</div>",
    unsafe_allow_html=True,
)

# ── Input Area ──────────────────────────────────────────────────────────
user_input = st.text_area(
    "Enter text for bias analysis:",
    value=st.session_state.input_text,
    height=180,
    key="text_area_input",
    placeholder="Paste a sentence or paragraph here…",
)

# ── Presentation Sample Inputs ──────────────────────────────────────────
with st.expander("💡 Presentation Samples (Click to use)"):
    samples = {
        "Gender Bias": "Women are too emotional to be leaders in high-stakes environments.",
        "Age Bias": "Older employees usually struggle with modern technology and are less adaptable.",
        "Nationality Bias": "People from that country are always rude and dishonest in business dealings.",
        "Disability Bias": "Disabled workers cannot handle high-pressure jobs because of their limitations.",
        "Socioeconomic Bias": "Poor people are usually lazy and uneducated, which is why they stay poor."
    }
    cols = st.columns(len(samples))
    for i, (label, text) in enumerate(samples.items()):
        if cols[i].button(label, use_container_width=True):
            st.session_state.input_text = text
            st.rerun()

col_btn, _ = st.columns([2, 8])
with col_btn:
    analyze_btn = st.button("✨  Analyze & Mitigate", use_container_width=True)

# ── Analysis ────────────────────────────────────────────────────────────
text_to_analyze = user_input.strip() if user_input else ""

if analyze_btn and text_to_analyze:
    with st.spinner("🔬 Running hybrid detection pipeline & generating mitigation…"):
        t0 = time.time()
        st.session_state.analysis_result = process_paragraph(text_to_analyze)
        st.session_state.inference_time = time.time() - t0

# ── Results ─────────────────────────────────────────────────────────────
if st.session_state.analysis_result:
    res = st.session_state.analysis_result

    st.markdown("<br><hr style='border-color:rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Bias Score</div>
            <div class="metric-value" style="color:{res['color']};">{res['max_score']:.1f}%</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Severity</div>
            <div class="metric-value" style="color:{res['color']};">{res['severity']}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        badges = "".join(f"<span class='badge'>{c}</span>" for c in res["categories"]) or "<span class='badge'>None</span>"
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Categories</div>
            <div style="margin-top:10px;">{badges}</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        engine_label = get_active_provider() or "Local"
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">Inference ({engine_label})</div>
            <div class="metric-value" style="font-size:2rem;">{st.session_state.inference_time:.2f}s</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Detailed results ────────────────────────────────────────────────
    if res["is_biased"]:
        left, right = st.columns(2)

        with left:
            st.markdown("### 🔍 Original (Highlighted)")
            st.markdown(
                f"<div class='original-text-box'>{res['original_highlighted_html']}</div>",
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🧠 AI Reasoning")
            reasoning_items = ""
            for edit in res["edits"]:
                cats = ", ".join(edit["categories"]) if edit["categories"] else "Social"
                reason = edit.get("reasoning", "Rewritten to remove exclusionary language.")
                reasoning_items += (
                    f"<li><strong>{cats}</strong> (confidence {edit['score']:.1f}%) — "
                    f"&quot;<em>{edit['original']}</em>&quot; → {reason}</li>"
                )
            st.markdown(f"<ul class='reasoning-list'>{reasoning_items}</ul>", unsafe_allow_html=True)

        with right:
            st.markdown("### ✨ Mitigated Output")
            st.markdown(
                f"<div class='mitigated-text'>{res['mitigated_paragraph']}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
            engine = get_active_provider()
            if engine:
                st.info(
                    f"💡 Powered by **{engine}** AI engine with structured few-shot prompting "
                    f"for maximum rewrite quality. Local FLAN-T5 available as fallback."
                )
            else:
                st.info(
                    "💡 Generated by a locally-hosted Seq2Seq transformer with constrained "
                    "beam search. Add an API key to `.env` for AI-powered rewrites."
                )
            
            # ── Export Feature ──────────────────────────────────────────
            report_text = f"""
AI BIAS GUARD ANALYSIS REPORT
----------------------------
Original: {text_to_analyze}
Mitigated: {res['mitigated_paragraph']}
Bias Score: {res['max_score']:.1f}%
Severity: {res['severity']}
Categories: {', '.join(res['categories'])}
Engine: {engine or 'Local (FLAN-T5)'}
            """
            st.download_button(
                label="📥 Download Analysis Report",
                data=report_text,
                file_name="bias_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:40px;">
            <h2 style="color:#10b981 !important;">✅ No Significant Bias Detected</h2>
            <p>The text appears neutral, professional, and inclusive.</p>
        </div>""", unsafe_allow_html=True)