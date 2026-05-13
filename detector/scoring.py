def calculate_severity(semantic_score: float, lexical_hits: int, toxicity_score: float = 0.0) -> dict:
    """
    Calculates overall bias score (0-100) and severity level based on a hybrid approach.
    """
    # Base score is primarily driven by semantic classification confidence
    base_score = semantic_score * 100
    
    # Lexical boosting: specific slurs or known stereotypes increase the score
    lexical_boost = min(lexical_hits * 15, 30) # Max 30 points boost
    
    # Toxicity boosting: if it's toxic, it's more severe
    toxicity_boost = toxicity_score * 20
    
    # Final composite score
    final_score = min(base_score + lexical_boost + toxicity_boost, 100.0)
    
    # Severity categorization
    if final_score < 30:
        severity = "Low"
        color = "#10b981" # Green
    elif final_score < 60:
        severity = "Moderate"
        color = "#f59e0b" # Yellow/Orange
    elif final_score < 85:
        severity = "High"
        color = "#ef4444" # Red
    else:
        severity = "Severe"
        color = "#991b1b" # Dark Red
        
    return {
        "score_0_100": round(final_score, 1),
        "score_normalized": round(final_score / 100.0, 4),
        "severity": severity,
        "color": color
    }
