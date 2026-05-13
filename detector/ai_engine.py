"""
Advanced AI Mitigation Engine — Multi-provider with persistent API key support.

API keys are loaded ONCE from:
  1. .env file in the project root (recommended — paste once, use forever)
  2. Environment variables (if .env not present)
  3. Streamlit sidebar input (runtime fallback, saved to .env automatically)

Provider priority: Gemini → OpenAI → Anthropic
"""

import os
import json
import re

from pathlib import Path

# ── Load .env file on import ────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(_env_path)
except ImportError:
    # python-dotenv not installed — fall back to os.environ
    pass

# Optional provider SDKs
try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:
    genai = None
    genai_types = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None


# ── System prompt (shared across providers) ─────────────────────────────
SYSTEM_PROMPT = """You are an expert linguistic bias analyst specializing in fair, inclusive language.

Your task is to:
1. Detect if a sentence contains social bias (gender, age, racial, religious, socioeconomic, disability, nationality, appearance, political, workplace stereotypes).
2. Explain WHY the bias exists using professional, precise reasoning.
3. Rewrite the sentence to be neutral, inclusive, and professional. The rewrite MUST:
   - Focus on individual merit, not group identity.
   - Generalize to all people rather than inverting the stereotype.
   - Maintain the core subject/topic while removing discriminatory framing.
   - Sound natural and professional — as if written by an editor at a major publication.
   - NOT just state the opposite of the bias, but provide a balanced perspective.
   - NOT be overly verbose or preachy. Be concise and direct.

IMPORTANT: Respond ONLY with a valid JSON object. No markdown, no code fences, no explanation outside JSON."""


def _build_prompt(sentence: str) -> str:
    """Constructs a structured few-shot prompt for maximum mitigation quality."""
    return f"""Analyze this sentence for social bias and provide a neutral rewrite.

### Few-Shot Examples ###

Input: "Women are too emotional to be leaders."
Output: {{"is_biased": true, "reasoning": "This statement stereotypes women by attributing emotional instability to their entire gender and falsely links emotional expression with leadership incompetence.", "mitigated": "Leadership effectiveness depends on individual skills, emotional intelligence, and experience rather than gender.", "categories": ["Gender Bias"]}}

Input: "Older employees usually struggle with modern technology."
Output: {{"is_biased": true, "reasoning": "This generalizes all older employees as technologically incompetent, ignoring individual capability and willingness to learn.", "mitigated": "Employees of all age groups can learn and adapt to new technologies with proper training and support.", "categories": ["Age Bias"]}}

Input: "Poor people are usually lazy and uneducated."
Output: {{"is_biased": true, "reasoning": "This falsely equates economic status with work ethic and intelligence, ignoring systemic factors and individual circumstances.", "mitigated": "Economic circumstances do not determine a person's work ethic, intelligence, or potential.", "categories": ["Socioeconomic Bias"]}}

Input: "People from that country are always rude and dishonest."
Output: {{"is_biased": true, "reasoning": "This broadly stereotypes an entire nationality with negative traits, which constitutes harmful xenophobia.", "mitigated": "Behavior and character vary between individuals and should not be generalized based on nationality.", "categories": ["Nationality Bias"]}}

Input: "Disabled workers cannot handle high-pressure jobs."
Output: {{"is_biased": true, "reasoning": "This assumes that disability inherently limits professional capability, which is both inaccurate and exclusionary.", "mitigated": "People with disabilities can perform high-pressure roles effectively when provided with appropriate support and accessibility.", "categories": ["Disability Bias"]}}

Input: "The sun rises in the east."
Output: {{"is_biased": false, "reasoning": "This is an objective astronomical fact with no social bias.", "mitigated": "The sun rises in the east.", "categories": []}}

Input: "I went to the store to buy groceries."
Output: {{"is_biased": false, "reasoning": "This is a neutral daily activity with no social bias.", "mitigated": "I went to the store to buy groceries.", "categories": []}}

### Your Task ###

Input: "{sentence}"
Output:"""


def _parse_json_response(text: str) -> dict | None:
    """Robustly parses JSON from LLM output, handling markdown fences and quirks."""
    if not text:
        return None
    # Strip markdown code fences if present
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    
    try:
        result = json.loads(text)
        # Validate required fields
        if isinstance(result, dict) and "is_biased" in result:
            # Normalize fields
            result.setdefault("reasoning", "")
            result.setdefault("mitigated", "")
            result.setdefault("categories", [])
            return result
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
        if match:
            try:
                result = json.loads(match.group())
                if isinstance(result, dict) and "is_biased" in result:
                    result.setdefault("reasoning", "")
                    result.setdefault("mitigated", "")
                    result.setdefault("categories", [])
                    return result
            except json.JSONDecodeError:
                pass
    return None


def _save_key_to_env(key_name: str, key_value: str):
    """Persists a new API key to the .env file so the user never has to enter it again."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    
    lines = []
    key_found = False
    
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={key_value}\n")
            key_found = True
        else:
            new_lines.append(line)
    
    if not key_found:
        new_lines.append(f"\n{key_name}={key_value}\n")
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    # Also set in current process environment
    os.environ[key_name] = key_value


def get_active_provider() -> str | None:
    """Returns which AI provider is currently configured, or None."""
    if os.getenv("GOOGLE_API_KEY"):
        return "Gemini"
    if os.getenv("OPENAI_API_KEY"):
        return "OpenAI"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "Anthropic"
    return None


def get_ai_mitigation(sentence: str) -> dict | None:
    """
    Multi-provider AI mitigation engine.
    Prioritizes Gemini (fast + free tier) → OpenAI (GPT-4o) → Anthropic (Claude).
    Returns structured JSON with is_biased, reasoning, mitigated, categories.
    """
    
    prompt = _build_prompt(sentence)

    # ── 1. Try Google Gemini (Recommended — fast, free tier, excellent quality) ──
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key and genai:
        try:
            client = genai.Client(api_key=google_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1,
                    max_output_tokens=512,
                )
            )
            result = _parse_json_response(response.text)
            if result:
                return result
        except Exception as e:
            print(f"[AI Engine] Gemini error: {e}")

    # ── 2. Try OpenAI (GPT-4o) ──────────────────────────────────────────
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and OpenAI:
        try:
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=512,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            result = _parse_json_response(response.choices[0].message.content)
            if result:
                return result
        except Exception as e:
            print(f"[AI Engine] OpenAI error: {e}")

    # ── 3. Try Anthropic (Claude 3.5 Sonnet) ────────────────────────────
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic:
        try:
            client = anthropic.Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=512,
                temperature=0.1,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            result = _parse_json_response(response.content[0].text)
            if result:
                return result
        except Exception as e:
            print(f"[AI Engine] Anthropic error: {e}")

    # No provider available — fall back to local pipeline
    return None
