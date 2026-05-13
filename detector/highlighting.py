"""Span extraction and HTML highlighting for biased phrases."""

import re


def extract_biased_spans(sentence: str, trigger_phrases: list) -> list:
    """
    Given a sentence and a list of potentially biased phrases/words,
    returns a list of (start_char, end_char, label) tuples for highlighting.
    """
    spans = []
    if not trigger_phrases:
        return spans

    # Sort phrases by length descending to match longest first
    trigger_phrases = sorted(trigger_phrases, key=len, reverse=True)

    matched_indices: set = set()

    for phrase in trigger_phrases:
        if not phrase.strip():
            continue

        # Find all occurrences (case-insensitive)
        for match in re.finditer(re.escape(phrase.lower()), sentence.lower()):
            start, end = match.span()

            # Skip if overlapping with an already-matched span
            if any(i in matched_indices for i in range(start, end)):
                continue

            spans.append((start, end, "BIAS"))
            matched_indices.update(range(start, end))

    return spans


def generate_highlighted_html(sentence: str, spans: list) -> str:
    """
    Takes a sentence and list of (start, end, label) spans,
    returns an HTML string with biased spans highlighted.
    """
    if not spans:
        return sentence

    # Sort spans by start index
    spans = sorted(spans, key=lambda x: x[0])

    html_parts = []
    last_idx = 0

    for start, end, label in spans:
        # Text before the span
        if start > last_idx:
            html_parts.append(sentence[last_idx:start])

        # Highlighted span
        html_parts.append(
            f'<span class="bias-highlight" title="{label}">{sentence[start:end]}</span>'
        )
        last_idx = end

    # Remaining text
    if last_idx < len(sentence):
        html_parts.append(sentence[last_idx:])

    return "".join(html_parts)
