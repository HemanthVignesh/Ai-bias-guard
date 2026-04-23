import os
import re
from typing import Dict, Any
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import warnings

# Suppress deprecation warnings locally
warnings.filterwarnings("ignore", category=FutureWarning)

# Global variables to hold the lazily loaded pipeline
_classifier = None
_mitigator_model = None
_mitigator_tokenizer = None

def get_classifier():
    """Lazily load the zero-shot classifier to avoid blocking startup."""
    global _classifier
    if _classifier is None:
        print("Loading zero-shot classifier (facebook/bart-large-mnli)... This might take a bit on first run.")
        _classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _classifier

def get_mitigator():
    """Lazily load the T5 mitigator model directly."""
    global _mitigator_model, _mitigator_tokenizer
    if _mitigator_model is None:
        print("Loading local T5 mitigation model...")
        model_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "t5_mitigator"))
        
        try:
            print("Importing traceback...")
            import traceback
            print("Loading tokenizer...")
            _mitigator_tokenizer = AutoTokenizer.from_pretrained(model_path)
            print("Loading model...")
            _mitigator_model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            print("Successfully loaded T5 mitigator.")
        except Exception as e:
            print(f"Failed to load mitigator: {e}")
            traceback.print_exc()
            _mitigator_model = None
            _mitigator_tokenizer = None
    return _mitigator_model, _mitigator_tokenizer

def detect_bias(sentence: str) -> Dict[str, Any]:
    """
    Detects bias in a given sentence using zero-shot classification and rule-based boosting.
    """
    classifier = get_classifier()
    
    # Base classification
    result = classifier(sentence, candidate_labels=["biased", "unbiased"])
    
    # Extract the probability for "biased"
    score = 0.0
    for label, prob in zip(result['labels'], result['scores']):
        if label == "biased":
            score = prob
            break
            
    # Lexical boosting based on stereotype dictionary
    gender_bias_words = ["men", "women", "male", "female", "usually men", "usually women"]
    
    # We look for exact word boundaries to avoid matching sub-words, except for phrases
    penalty = 0.0
    lower_sentence = sentence.lower()
    for word in gender_bias_words:
        if re.search(rf"\b{re.escape(word)}\b", lower_sentence):
            penalty = 0.15
            break
            
    final_score = min(score + penalty, 1.0)
    
    # Based on user's threshold definition
    is_biased = final_score >= 0.3
    
    # Determine Bias Type if biased
    bias_type = "None"
    if is_biased:
        type_result = classifier(sentence, candidate_labels=["gender bias", "racial bias", "age bias", "religious or class bias"])
        top_label = type_result['labels'][0]
        if top_label == "gender bias":
            bias_type = "Gender"
        elif top_label == "racial bias":
            bias_type = "Race"
        elif top_label == "age bias":
            bias_type = "Age"
        else:
            bias_type = "Religion_and_Class"
            
    return {
        "score": final_score,
        "is_biased": is_biased,
        "bias_type": bias_type
    }

def mitigate_bias(sentence: str) -> Dict[str, Any]:
    """
    Analyzes a sentence for social bias and provides a result dictionary
    using entirely local NLP models (BART for detection, T5 for mitigation).
    """
    score = 0.0
    is_biased = False
    try:
        detection = detect_bias(sentence)
        score = detection["score"]
        is_biased = detection["is_biased"]
        bias_type = detection["bias_type"]
        
        if not is_biased:
            return {
                "input_sentence": sentence,
                "bias_score": float(round(score, 4)),
                "is_biased": False,
                "bias_type": "None",
                "mitigated_sentence": sentence
            }
            
        model, tokenizer = get_mitigator()
        if not model:
            return {
                "input_sentence": sentence,
                "bias_score": float(round(score, 4)),
                "is_biased": True,
                "bias_type": "Model Error",
                "mitigated_sentence": f"[Mitigation Model Missing] {sentence}"
            }

        # Use Local T5 for mitigation with bias_type prefix
        prompt = f"mitigate {bias_type} bias: {sentence}"
        inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)
        outputs = model.generate(
            **inputs, 
            max_new_tokens=128,
            num_beams=4,
            repetition_penalty=1.2,
            early_stopping=True
        )
        rewritten = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        return {
            "input_sentence": sentence,
            "bias_score": float(round(score, 4)),
            "is_biased": True,
            "bias_type": bias_type,
            "mitigated_sentence": rewritten
        }

    except Exception as e:
        print(f"Error in deeply local analysis: {e}")
        return {
            "input_sentence": sentence,
            "bias_score": float(round(score, 4)) if score else 0.0,
            "is_biased": is_biased,
            "bias_type": f"Mitigation Error ({type(e).__name__})",
            "mitigated_sentence": f"[Mitigation Failed] {sentence}" if is_biased else sentence
        }