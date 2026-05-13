import os
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer

print("Downloading/Caching SentenceTransformer...", flush=True)
SentenceTransformer('all-MiniLM-L6-v2')
print("Done.", flush=True)

print("Downloading/Caching BART-large...", flush=True)
pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device="cpu")
print("Done.", flush=True)

print("Downloading/Caching FLAN-T5-base...", flush=True)
AutoTokenizer.from_pretrained("google/flan-t5-base")
AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
print("Done.", flush=True)

print("All models successfully cached locally!", flush=True)
