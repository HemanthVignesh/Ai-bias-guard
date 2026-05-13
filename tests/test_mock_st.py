import sys
from unittest.mock import MagicMock

# Mock Streamlit completely so we don't import it
mock_st = MagicMock()
def mock_cache_resource(func):
    # simple cache
    cache = {}
    def wrapper(*args, **kwargs):
        if func.__name__ not in cache:
            cache[func.__name__] = func(*args, **kwargs)
        return cache[func.__name__]
    return wrapper

mock_st.cache_resource = mock_cache_resource
sys.modules['streamlit'] = mock_st

from detector.mitigation import process_paragraph

print("Testing process_paragraph...", flush=True)
res = process_paragraph("Women are too emotional to be leaders.")
print(res)
print("SUCCESS!")
