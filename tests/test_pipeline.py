import os
import time

print("Starting test...", flush=True)

try:
    print("Importing mitigation...", flush=True)
    t0 = time.time()
    from detector.mitigation import process_paragraph
    print(f"Import successful in {time.time() - t0:.2f}s", flush=True)
    
    test_text = "Women are too emotional to be leaders in high-stakes environments."
    print("Testing pipeline with text:", test_text, flush=True)
    
    result = process_paragraph(test_text)
    
    print("\n--- Result ---", flush=True)
    print("Is Biased:", result["is_biased"], flush=True)
    print("Max Score:", result["max_score"], flush=True)
    print("Severity:", result["severity"], flush=True)
    print("Categories:", result["categories"], flush=True)
    print("Mitigated:", result["mitigated_paragraph"], flush=True)
    print("Finished processing successfully.", flush=True)
except Exception as e:
    print(f"Error occurred: {e}", flush=True)
