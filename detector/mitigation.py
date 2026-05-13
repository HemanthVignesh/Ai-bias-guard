"""
Advanced Mitigation Pipeline — Expert Linguistic Audit Engine.

Processing order:
  1. Advanced AI Engine (Gemini/OpenAI/Anthropic) — best quality
  2. Semantic Contextual Hints — retrieval-augmented reasoning
  3. FLAN-T5 Expert Auditor — local fallback with Chain-of-Thought
  4. Rule-based generic fallback — guaranteed safety net
"""

import streamlit as st
import re
from detector.ai_engine import get_ai_mitigation
from detector.bias_detector import detect_sentence_bias
from detector.highlighting import generate_highlighted_html

# ─── EXPERT MITIGATION KNOWLEDGE BASE ──────────────────────────────────────────
# These examples teach the model the REASONING behind a genius mitigation.
MITIGATION_TEMPLATES = [
    ("Women are too emotional to be leaders",
     "Leadership capability is defined by individual resilience, communication skills, and emotional intelligence, rather than gender."),
    ("Older employees usually struggle with modern technology",
     "Technological proficiency is a learned skill that varies by individual experience and training, not by age."),
    ("Poor people are usually lazy and uneducated",
     "Professional potential and work ethic are individual traits shaped by character and opportunity, not economic status."),
    ("People from that country are always rude",
     "Interpersonal behavior is an individual characteristic and should not be generalized across an entire nationality."),
    ("Disabled workers cannot handle high-pressure jobs",
     "Professional capability in high-pressure roles depends on individual skills and appropriate support, not disability status."),
    ("Attractive people are more likely to succeed",
     "Career success is determined by individual merit, dedication, and professional achievement rather than appearance."),
    ("Introverts are bad managers",
     "Effective management styles vary; both introverted and extroverted individuals can lead successfully through their unique strengths."),
    ("Millennials are entitled and lazy",
     "Professional commitment and work ethic are individual characteristics that vary across all generations."),
    ("Men are naturally better at technical fields",
     "Aptitude for technical fields is developed through education, interest, and practice, and is independent of gender."),
    ("Immigrants take away local jobs",
     "Economic markets are complex and influenced by many factors; individual contributions to the workforce come from diverse backgrounds."),
]

CATEGORY_FALLBACKS = {
    "Gender Bias": "Abilities and professional roles should be evaluated based on individual merit and experience rather than gender.",
    "Age Bias": "Professional capability and adaptability are individual traits that exist across all age groups.",
    "Socioeconomic Bias": "Economic background does not determine an individual's potential, work ethic, or intelligence.",
    "Racial/Ethnic Bias": "Character and professional aptitude are individual traits and should not be generalized based on race or ethnicity.",
}


@st.cache_resource
def load_semantic_matcher():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    patterns = [t[0] for t in MITIGATION_TEMPLATES]
    embeddings = model.encode(patterns, convert_to_tensor=True)
    return model, embeddings

@st.cache_resource
def load_mitigator():
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model = model.to("cpu")
    return model, tokenizer


def mitigate_sentence(sentence: str, categories: list) -> str:
    \"\"\"
    Expert Auditor Engine:
    Uses a Chain-of-Thought (CoT) framework to ensure the model reasons through the 
    bias before generating a neutralization strategy.
    \"\"\"

    # 1. Retrieve Style Examples
    matcher, template_embeddings = load_semantic_matcher()
    input_embedding = matcher.encode(sentence, convert_to_tensor=True)
    
    from sentence_transformers import util
    similarities = util.cos_sim(input_embedding, template_embeddings)[0]
    top_k = 2
    _, top_indices = similarities.topk(k=top_k)

    # Construct the Expert reasoning examples
    expert_examples = ""
    for idx in top_indices:
        ex_in, ex_out = MITIGATION_TEMPLATES[idx.item()]
        expert_examples += f"Case: \"{ex_in}\"\nAnalysis: Generalizing identity groups.\nExpert Rewrite: \"{ex_out}\"\n\n"

    primary_cat = categories[0] if categories else "social"
    
    # --- THE GENIUS PROMPT ---
    # We frame the task as a high-level Audit rather than a simple rewrite.
    prompt = f\"\"\"You are a Senior Linguistic Diversity Expert. 
Your mission is to audit biased statements and transform them into inclusive, merit-based language.

### Expert Audit Methodology:
- Identify the identity-based generalization.
- Shift the focus to individual capability and objective traits.
- Ensure the final language is professional and sophisticated.

{expert_examples}### Live Audit:
Case: \"{sentence}\"
Analysis: This is a biased generalization regarding {primary_cat.lower()}.
Neutralization Strategy: Focus on individual talent and objective merit.
Expert Rewrite:\"\"\"

    # Execute with refined parameters for "Genius" level output
    model, tokenizer = load_mitigator()
    inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        num_beams=8,
        temperature=0.8, # Added slight creativity for more "natural" expert phrasing
        do_sample=True,
        no_repeat_ngram_size=3,
        repetition_penalty=1.5,
        top_p=0.95
    )
    
    rewritten = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    # Expert-level Cleanup
    rewritten = re.sub(r'^Expert Rewrite:\s*', '', rewritten, flags=re.IGNORECASE)
    rewritten = rewritten.strip('\"')
            
    # Final validation: If it failed to generalize, use fallback
    clean_rewritten = rewritten.lower().strip(\" .!?\\t\\n\")
    clean_sentence = sentence.lower().strip(\" .!?\\t\\n\")
            
    if len(rewritten) < 10 or clean_rewritten == clean_sentence:
        cat = categories[0] if categories else \"this topic\"
        return CATEGORY_FALLBACKS.get(cat, 
            f\"Statements regarding {cat.lower()} should be framed around individual capability and professional impact rather than identity-based generalizations.\")
        
    return rewritten


def process_paragraph(paragraph: str):
    \"\"\"
    Segments and audits text using the Expert Pipeline.
    \"\"\"
    if not paragraph.strip():
         return {"is_biased": False, "max_score": 0, "severity": "None", "color": "gray", "categories": [], "edits": [], "original_highlighted_html": "", "mitigated_paragraph": ""}

    # 1. Global AI Expert Check (External API)
    ai_res = get_ai_mitigation(paragraph)
    if ai_res and ai_res.get("is_biased"):
        return {
            "is_biased": True,
            "max_score": 95.0,
            "severity": "High",
            "color": "#ef4444",
            "categories": ai_res.get("categories", ["Social Bias"]),
            "edits": [{"original": paragraph, "mitigated": ai_res.get("mitigated"), "reasoning": ai_res.get("reasoning"), "categories": ai_res.get("categories"), "score": 95.0, "severity": "High"}],
            "original_highlighted_html": f"<span class='bias-span' style='background-color:rgba(239, 68, 68, 0.2); border-bottom: 2px solid #ef4444;'>{paragraph}</span>",
            "mitigated_paragraph": ai_res.get("mitigated")
        }

    # 2. Local Expert Sentence Audit
    segments = re.split(r'([.!?]+(?:\s+|$|\n))', paragraph)
    final_mitigated_segments = []
    edits = []
    all_categories = set()
    max_score = 0.0
    is_paragraph_biased = False
    html_segments = []
    
    for segment in segments:
        if re.search(r'[a-zA-Z0-9]', segment):
            clean_sentence = segment.strip()
            det = detect_sentence_bias(clean_sentence)
            
            if det["is_biased"]:
                is_paragraph_biased = True
                max_score = max(max_score, det["score"])
                all_categories.update(det["categories"])
                
                # Run the Expert Audit
                mitigated = mitigate_sentence(clean_sentence, det["categories"])
                
                edits.append({
                    "original": clean_sentence, "mitigated": mitigated,
                    "reasoning": "Audit identified group-based generalization; shifted focus to individual capability.",
                    "categories": det["categories"], "score": det["score"], "severity": det["severity"]
                })
                
                html_segment = generate_highlighted_html(clean_sentence, det["spans"])
                final_mitigated_segments.append(segment.replace(clean_sentence, mitigated))
                html_segments.append(segment.replace(clean_sentence, html_segment))
            else:
                final_mitigated_segments.append(segment)
                html_segments.append(segment)
        else:
            final_mitigated_segments.append(segment)
            html_segments.append(segment)
            
    return {
        "is_biased": is_paragraph_biased,
        "max_score": max_score,
        "severity": "High" if max_score > 60 else "Moderate",
        "color": "#ef4444" if max_score > 60 else "#f59e0b",
        "categories": list(all_categories),
        "edits": edits,
        "original_highlighted_html": "".join(html_segments),
        "mitigated_paragraph": "".join(final_mitigated_segments)
    }
