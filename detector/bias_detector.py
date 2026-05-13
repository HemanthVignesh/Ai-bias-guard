import streamlit as st
import re
from detector.categories import BIAS_CATEGORIES, LEXICON
from detector.scoring import calculate_severity
from detector.highlighting import extract_biased_spans

@st.cache_resource
def load_zero_shot_classifier():
    # Switching to the industry-standard BART-large model for absolute reliability and accuracy
    from transformers import pipeline
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device="cpu")

@st.cache_resource
def load_toxicity_model():
    """Disabled for presentation to save 500MB RAM. BART/AI cover social bias sufficiently."""
    return None
    # try:
    #     from detoxify import Detoxify
    #     return Detoxify('original')
    # except:
    #     return None

def detect_sentence_bias(sentence: str):
    """
    State-of-the-art hybrid detection pipeline.
    Identifies bias while correctly classifying facts and daily activities as neutral.
    """
    if not sentence.strip():
        return {"is_biased": False, "score": 0, "categories": [], "spans": [], "severity": "None", "color": "gray"}
        
    classifier = load_zero_shot_classifier()
    toxicity_model = load_toxicity_model()
    
    # 1. Semantic Check with specialized labels
    # We include 'objective fact' and 'daily activity' to steer the model towards non-bias for those cases
    candidate_labels = [
        "biased, stereotypical, or discriminatory", 
        "an objective fact or universal truth", 
        "a simple daily activity",
        "neutral and inclusive"
    ]
    gen_results = classifier(sentence, candidate_labels=candidate_labels, multi_label=False)
    
    # Calculate the bias confidence
    bias_idx = gen_results['labels'].index("biased, stereotypical, or discriminatory")
    semantic_score = gen_results['scores'][bias_idx]
    
    # Check if it was classified as a fact or daily activity
    top_label = gen_results['labels'][0]
    is_likely_fact = top_label in ["an objective fact or universal truth", "a simple daily activity"]
    
    # 2. Lexical Check (Lexicon handles 'hard' triggers)
    lexical_hits = 0
    trigger_words = []
    detected_cats_lexical = set()
    
    sentence_lower = sentence.lower()
    for cat, phrases in LEXICON.items():
        for phrase in phrases:
            if re.search(rf"\b{re.escape(phrase)}\b", sentence_lower):
                lexical_hits += 1
                trigger_words.append(phrase)
                detected_cats_lexical.add(cat)
                
    # 3. Toxicity Check
    toxicity_score = 0.0
    if toxicity_model:
        tox_res = toxicity_model.predict(sentence)
        toxicity_score = tox_res['toxicity']
        
    # 4. Severity Scoring
    scoring_result = calculate_severity(semantic_score, lexical_hits, toxicity_score)
    final_score_0_100 = scoring_result["score_0_100"]
    severity = scoring_result["severity"]
    
    # DYNAMIC THRESHOLDING
    # 1. If it's an objective fact/daily activity, we require VERY high bias confidence to flag
    # 2. If we have lexical hits, we flag much more easily
    # 3. Default threshold is 50%
    
    if is_likely_fact and lexical_hits == 0:
        is_biased = final_score_0_100 > 85.0 # Very high bar for facts
    elif lexical_hits > 0:
        is_biased = final_score_0_100 > 35.0 or lexical_hits >= 1 # Easy flag for lexical matches
    else:
        is_biased = final_score_0_100 > 50.0 # Standard threshold
        
    # Final safety: if it's highly toxic, it's biased
    if toxicity_score > 0.7:
        is_biased = True
    
    categories = list(detected_cats_lexical)
    
    # 5. Semantic Category Expansion if Biased
    if is_biased and not categories:
        cat_results = classifier(sentence, candidate_labels=BIAS_CATEGORIES, multi_label=True)
        # Add top categories
        for label, prob in zip(cat_results['labels'], cat_results['scores']):
            if prob >= 0.35:
                categories.append(label)
        if not categories:
             categories.append(cat_results['labels'][0]) # Fallback
             
    # 6. Extractive Spans for Highlighting
    # If we have lexical hits, we highlight them. 
    # If not, but it's semantically biased, we might try to find the root via a small trick, 
    # but for precision we only highlight lexical hits or use a heuristic.
    spans = extract_biased_spans(sentence, trigger_words)
    
    return {
        "is_biased": is_biased,
        "score": final_score_0_100,
        "severity": severity,
        "color": scoring_result["color"],
        "categories": categories,
        "spans": spans,
        "trigger_words": trigger_words,
        "semantic_score": semantic_score,
        "toxicity_score": toxicity_score
    }
