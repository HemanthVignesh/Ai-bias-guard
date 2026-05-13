from streamlit.testing.v1 import AppTest
import time

print("Starting AppTest...", flush=True)

# Initialize the test with app.py
at = AppTest.from_file("app.py", default_timeout=30)

print("Running the app...", flush=True)
at.run()

print("App loaded. Finding text area...", flush=True)
# Find the text area and set the value
# The user's app likely has a text_area. Let's find it.
text_areas = at.text_area
if len(text_areas) > 0:
    text_areas[0].input("Women are too emotional to be leaders.")
    print("Entered text into text area.", flush=True)
else:
    print("Could not find text area.", flush=True)

print("Finding button...", flush=True)
# Find the analyze button
buttons = at.button
analyze_btn = None
for btn in buttons:
    if "Analyze" in btn.label or "Mitigate" in btn.label:
        analyze_btn = btn
        break

if analyze_btn:
    print(f"Clicking button: {analyze_btn.label}", flush=True)
    analyze_btn.click().run()
    print("Processing complete!", flush=True)
    
    # Print the resulting text or markdown
    for md in at.markdown:
        if len(md.value) > 10:
            print(f"MARKDOWN OUTPUT: {md.value[:100]}...", flush=True)
    for w in at.warning:
        print(f"WARNING: {w.value}", flush=True)
    for e in at.error:
        print(f"ERROR: {e.value}", flush=True)
else:
    print("Could not find Analyze button.", flush=True)

print("Test complete.", flush=True)
