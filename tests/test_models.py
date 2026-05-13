import os
import sys

# Ensure protobuf implementation is set correctly (as in app.py)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

print("Starting model load tests...", flush=True)

try:
    print("\n--- Testing SentenceTransformers ---", flush=True)
    from sentence_transformers import SentenceTransformer
    print("Imported SentenceTransformer.", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Loaded all-MiniLM-L6-v2 successfully.", flush=True)
except Exception as e:
    print(f"Failed SentenceTransformer: {e}", flush=True)

try:
    print("\n--- Testing FLAN-T5 ---", flush=True)
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    print("Imported transformers.", flush=True)
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    print("Loaded FLAN-T5 tokenizer.", flush=True)
    model2 = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    print("Loaded FLAN-T5 model successfully.", flush=True)
except Exception as e:
    print(f"Failed FLAN-T5: {e}", flush=True)

try:
    print("\n--- Testing BART ---", flush=True)
    from transformers import pipeline
    print("Imported pipeline.", flush=True)
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device="cpu")
    print("Loaded BART successfully.", flush=True)
except Exception as e:
    print(f"Failed BART: {e}", flush=True)

try:
    print("\n--- Testing Detoxify ---", flush=True)
    from detoxify import Detoxify
    print("Imported Detoxify.", flush=True)
    detox = Detoxify('original')
    print("Loaded Detoxify successfully.", flush=True)
except Exception as e:
    print(f"Failed Detoxify: {e}", flush=True)

print("\nAll tests completed.", flush=True)
