from transformers import pipeline
import time

print("Loading BART model...", flush=True)
t0 = time.time()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device="cpu")
print(f"BART loaded in {time.time()-t0:.2f}s", flush=True)

sentence = "Women are too emotional to be leaders."
candidate_labels = ["biased", "neutral"]
print(f"Testing sentence: {sentence}", flush=True)
res = classifier(sentence, candidate_labels=candidate_labels)
print("Result:", res, flush=True)
print("SUCCESS!", flush=True)
