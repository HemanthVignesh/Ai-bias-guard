import sys
import os
# Add the root directory to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.mitigate import mitigate_bias

def test_unified_mitigation():
    sentences = [
        "Women are weak leaders.",
        "Middle Eastern people shouldn't be trusted.",
        "Seniors are clueless about modern tools.",
        "Poor people are dangerous.",
        "Math is a universal language."
    ]
    
    print("\nLocal Pipeline Analysis (BART + T5):")
    print("-" * 50)
    for s in sentences:
        result = mitigate_bias(s)
        
        score = result["bias_score"]
        is_biased = result["is_biased"]
        bias_type = result["bias_type"]
        corrected = result["mitigated_sentence"]
        
        print(f"Original: {s}")
        print(f"Bias Score: {score:.2f} ({'Biased' if is_biased else 'Neutral'})")
        if is_biased:
            print(f"Mitigated: {corrected}")
            print(f"Detected Type: {bias_type}")
        print("-" * 50)

if __name__ == "__main__":
    test_unified_mitigation()
