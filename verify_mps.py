import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

print(f"MPS available: {torch.backends.mps.is_available()}")

print("Loading bart...")
# Simulate the pipeline load that happened just before
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print("Bart loaded.")

print("Loading t5...")
try:
    tokenizer = AutoTokenizer.from_pretrained("models/t5_mitigator")
    model = AutoModelForSeq2SeqLM.from_pretrained("models/t5_mitigator")
    print("T5 loaded.")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Failed to load mitigator: {e}")
