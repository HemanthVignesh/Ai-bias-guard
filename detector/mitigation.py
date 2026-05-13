"""
Hybrid Mitigation Pipeline — AI-First with Semantic Template + FLAN-T5 Fallback.

Processing order:
  1. Advanced AI Engine (Gemini/OpenAI/Anthropic) — best quality
  2. Semantic Template Matching (cosine similarity > 0.70) — pre-written rewrites
  3. FLAN-T5 Base (few-shot prompting) — local fallback
  4. Rule-based generic fallback — guaranteed safety net
"""

import streamlit as st
import re
from detector.ai_engine import get_ai_mitigation
from detector.bias_detector import detect_sentence_bias
from detector.highlighting import generate_highlighted_html

# ─── HIGH-QUALITY MITIGATION TEMPLATES ──────────────────────────────────────────
# Each entry: (pattern_sentence, neutral_rewrite)
# These are GPT-quality rewrites covering all 10 bias categories.
MITIGATION_TEMPLATES = [
    # ── Gender Bias ──────────────────────────────────────────────────────────────
    ("Women are too emotional to be leaders",
     "Leadership ability depends on individual skills, experience, and emotional intelligence rather than gender."),
    ("Women are too emotional to handle leadership positions",
     "Leadership ability depends on individual skills, experience, and emotional intelligence rather than gender."),
    ("Men are naturally better at coding than women",
     "Programming ability is influenced by learning, practice, and experience, not gender."),
    ("Men are better at engineering than women",
     "Engineering ability is shaped by education, practice, and dedication, not gender."),
    ("Women are bad drivers",
     "Driving ability is an individual skill and is not determined by gender."),
    ("Women are not good at handling pressure in technical fields",
     "The ability to handle pressure in technical fields depends on individual experience and resilience, not gender."),
    ("Men should not work as nurses because it is a feminine profession",
     "Career suitability is determined by individual skills, interest, and qualifications rather than gender stereotypes."),
    ("Women belong in the kitchen",
     "Domestic responsibilities and career choices are personal decisions not determined by gender."),
    ("Men don't cry",
     "Expressing emotions is a natural human trait regardless of gender."),
    ("Girls are not good at math or science",
     "Mathematical and scientific ability are shaped by education, practice, and individual aptitude, not gender."),
    ("A woman's place is in the home",
     "Every person's place is wherever their skills, ambitions, and choices take them."),
    ("Women should not hold positions of power",
     "Positions of power should be filled based on competence, vision, and leadership skills, not gender."),
    ("Men are not nurturing enough to be caregivers",
     "Caregiving ability depends on individual empathy, patience, and dedication, not gender."),
    ("Women can't handle the stress of executive roles",
     "The ability to manage executive-level stress depends on individual resilience, experience, and coping strategies."),
    ("Men are better at high-stakes decision making",
     "Strategic decision-making capability is a professional skill developed through experience, regardless of gender."),

    # ── Age Bias ─────────────────────────────────────────────────────────────────
    ("Older employees usually struggle with modern technology",
     "Employees of all age groups can learn and adapt to new technologies with proper training and support."),
    ("Older employees are slow when it comes to learning new technologies",
     "Employees of all age groups can learn and adapt to new technologies with proper training and support."),
    ("Young workers are irresponsible and unreliable",
     "Reliability and professionalism vary from person to person regardless of age."),
    ("Young employees are irresponsible and unreliable in professional environments",
     "Reliability and professionalism vary from person to person regardless of age."),
    ("Elderly people should avoid working in fast-paced industries",
     "The ability to thrive in fast-paced industries depends on individual capability and adaptability, not age."),
    ("Old people can't learn new things",
     "Learning ability is an individual trait that varies from person to person regardless of age."),
    ("Millennials are entitled and lazy",
     "Work ethic and ambition are individual characteristics that cannot be generalized across an entire generation."),
    ("Boomers are resistant to change",
     "Openness to change is an individual personality trait, not a generational characteristic."),
    ("Young people have no respect for authority",
     "Respect for authority is shaped by individual values and upbringing, not age."),
    ("Older workers are past their prime",
     "Professional capability and expertise often grow with experience and are not diminished by age alone."),
    ("Recent graduates lack the maturity for serious roles",
     "Professional maturity is developed through experience and individual growth, not strictly by age."),

    # ── Socioeconomic Bias ───────────────────────────────────────────────────────
    ("Poor people are usually lazy and uneducated",
     "Economic circumstances do not determine a person's work ethic, intelligence, or potential."),
    ("Poor people are lazy",
     "Work ethic is an individual trait regardless of economic status."),
    ("Rich kids never understand hard work",
     "People's understanding of hard work depends on their experiences and values, not solely their financial background."),
    ("Rich kids never understand the value of hard work",
     "People's understanding of hard work depends on their experiences and values, not solely their financial background."),
    ("Poor students usually cannot compete with private school students",
     "Academic potential depends on individual effort, access to resources, and dedication rather than economic background."),
    ("People on welfare are taking advantage of the system",
     "Social safety nets serve diverse populations facing various challenges, and participation does not reflect individual character."),
    ("Rich people are greedy and selfish",
     "Generosity and selfishness are individual traits that exist across all economic backgrounds."),
    ("People from low-income neighborhoods are more likely to be criminals",
     "Criminal behavior is influenced by complex social factors and should not be generalized based on socioeconomic background."),

    # ── Nationality / Ethnic Bias ────────────────────────────────────────────────
    ("Immigrants take away jobs from local citizens",
     "Employment trends are influenced by many economic and social factors, and immigrants also contribute to economies and communities."),
    ("People from that country are always rude",
     "Behavior varies between individuals and should not be generalized based on nationality."),
    ("People from that country are always rude and dishonest",
     "Behavior and character vary between individuals and should not be generalized based on nationality."),
    ("People from rural areas are not smart enough for top tech companies",
     "Intelligence and professional capability are individual traits not determined by geographic background."),
    ("People from small towns are less innovative than city people",
     "Innovation and creativity are individual qualities not determined by geographic origin."),
    ("Non-native English speakers are usually poor communicators",
     "Communication skills are developed through practice and experience regardless of one's native language."),
    ("Immigrants don't integrate into society",
     "Integration is a two-way process influenced by individual effort, community support, and institutional policies."),
    ("Foreign workers are less qualified than local workers",
     "Professional qualifications should be evaluated on individual credentials and experience, not nationality."),

    # ── Religious Bias ───────────────────────────────────────────────────────────
    ("People of that religion are extremists",
     "Extremism should not be associated with an entire religion or community."),
    ("Certain religions promote violence and extremism",
     "Violence and extremism are actions of individuals, not characteristics of entire religions."),
    ("Religious people are irrational",
     "Rationality is an individual trait and is not determined by religious beliefs."),
    ("Atheists have no morals",
     "Moral character is shaped by individual values, empathy, and life experiences, not by religious affiliation."),
    ("Muslims are terrorists",
     "Terrorism is the act of individuals and extremist groups and should never be attributed to an entire religious community."),
    ("Religious people are less intelligent",
     "Intelligence is shaped by individual learning and cognitive ability, not by religious belief or practice."),

    # ── Disability Bias ──────────────────────────────────────────────────────────
    ("Disabled employees cannot handle demanding jobs",
     "People with disabilities can perform demanding roles effectively when provided with appropriate support and accessibility."),
    ("Disabled workers cannot handle high-pressure jobs",
     "People with disabilities can perform high-pressure roles effectively when provided with appropriate support and accessibility."),
    ("Disabled people are a burden on society",
     "People with disabilities contribute meaningfully to society when given equitable opportunities."),
    ("People with mental health issues are dangerous",
     "Mental health conditions vary widely and do not determine a person's likelihood of being dangerous; everyone deserves a safe environment."),
    ("Depressed people just need to try harder",
     "Mental health conditions are medical issues that require professional support and understanding rather than just individual effort."),
    ("Autistic people can't work in teams",
     "Team collaboration skills vary among individuals and are not determined by neurodivergent status."),
    ("People in wheelchairs can't live independent lives",
     "Independence is achieved through individual capability, adaptive tools, and accessible environments, not limited by mobility aids."),

    # ── Appearance Bias ──────────────────────────────────────────────────────────
    ("Attractive people are more intelligent and successful",
     "Intelligence and success are determined by skills, effort, and opportunities rather than appearance."),
    ("Attractive people are more likely to succeed in life",
     "Success in life is determined by skills, effort, and opportunities rather than physical appearance."),
    ("People with tattoos are less professional than others",
     "Professionalism is determined by behavior, work ethic, and competence rather than physical appearance."),
    ("Overweight people are lazy and lack discipline",
     "Body weight is influenced by many factors including genetics and health conditions; it does not determine a person's discipline or work ethic."),
    ("Short men are less attractive and less authoritative",
     "Authority and attractiveness are shaped by individual confidence, competence, and character, not physical stature."),
    ("People who dress casually are not serious about their work",
     "Work ethic and professionalism are demonstrated through actions and results, not clothing choices."),

    # ── Racial / Ethnic Bias ──────────────────────────────────────────────────
    ("Certain groups are more prone to criminal behavior",
     "Criminal behavior is a result of complex social and individual factors and should not be attributed to any specific racial or ethnic group."),
    ("People of that race are not as intelligent",
     "Intelligence is an individual trait influenced by education and opportunity, not race or ethnicity."),
    ("He is very articulate for someone of his background",
     "Communication skills are an individual achievement and should be recognized without reference to a person's background."),
    ("Asians are good at math",
     "Mathematical ability is an individual skill developed through education and practice, not an inherent trait of any ethnic group."),
    ("Black people are naturally more athletic",
     "Athletic ability is developed through individual training, dedication, and genetics at the personal level, not determined by race."),
    ("White people can't dance",
     "Dancing ability is an individual skill developed through practice and cultural exposure, not determined by race."),
    ("Hispanic people are hardworking but uneducated",
     "Education level and work ethic are individual characteristics shaped by personal circumstances and opportunity, not ethnicity."),

    # ── Workplace Stereotype Bias ──────────────────────────────────────────────
    ("Introverts are bad managers",
     "Management effectiveness depends on leadership skills, communication, and decision-making rather than personality type alone."),
    ("Introverts are bad managers because they lack communication skills",
     "Management effectiveness depends on leadership skills, communication style, and decision-making rather than personality type alone."),
    ("Women can't lead teams",
     "Leadership ability is determined by individual skills and experience, not gender."),
    ("We need a better culture fit for this role",
     "Candidates should be evaluated based on their skills, values, and how they contribute to the team's goals and diversity."),
    ("She is too aggressive to be a manager",
     "Leadership styles vary, and communication should be evaluated based on professional impact rather than gendered personality traits."),
    ("Remote workers are less productivity than office workers",
     "Productivity depends on individual work habits, management practices, and task requirements, not work location."),
    ("Part-time employees are less committed to their jobs",
     "Professional commitment is demonstrated through work quality and dedication, not the number of hours worked."),
    ("People without college degrees are less capable",
     "Professional capability is shaped by diverse forms of learning including experience, self-education, and practical training."),
    ("Engineers don't have good social skills",
     "Social skills vary among individuals in every profession and are not determined by one's field of work."),

    # ── Political Bias ───────────────────────────────────────────────────────────
    ("Conservatives are all racists",
     "Political beliefs are diverse and complex; holding a political viewpoint does not determine a person's views on race."),
    ("Liberals are naive and out of touch with reality",
     "Political perspectives reflect different value priorities and should be evaluated on their merits, not dismissed with stereotypes."),
    ("People who vote for that party are uneducated",
     "Voting decisions reflect diverse personal values and priorities and are not determined by education level."),
    
    # ── Subtle / Modern Bias ──────────────────────────────────────────────────
    ("She is a diversity hire and doesn't have the technical depth",
     "Every team member is evaluated based on their unique skills, experience, and contributions to the project."),
    ("We need someone with more 'culture fit' for this leadership role",
     "Leadership candidates should be evaluated based on their skills, values, and how they contribute to the team's objectives."),
    ("He is surprisingly articulate for someone from his background",
     "Communication skills are an individual achievement and should be recognized based on their professional impact."),
    ("This role requires a 'digital native' who understands modern trends",
     "The role requires proficiency in modern trends, which can be demonstrated by candidates of any age through their experience and skills."),
    ("We should avoid hiring parents because they lack focus",
     "Professional focus and dedication are individual traits and are not determined by a person's parental status."),
]

# ─── CATEGORY-SPECIFIC FALLBACK TEMPLATES ───────────────────────────────────────
# Used when no semantic match is found AND AI/FLAN-T5 fail
CATEGORY_FALLBACKS = {
    "Gender Bias": "Abilities, roles, and characteristics should be evaluated based on individual merit and experience, not gender.",
    "Age Bias": "Capability and potential are individual traits that exist across all age groups with proper opportunity and support.",
    "Racial/Ethnic Bias": "Character, abilities, and behavior are individual traits shaped by personal experience and should not be generalized based on race or ethnicity.",
    "Religious Bias": "Beliefs and values are personal matters; character and behavior should be evaluated at the individual level regardless of religious affiliation.",
    "Socioeconomic Bias": "Economic circumstances do not define a person's character, intelligence, or potential for success.",
    "Disability Bias": "People with disabilities contribute meaningfully to all aspects of society when given equitable access and opportunity.",
    "Nationality Bias": "Character and abilities are individual traits that should not be generalized based on national origin or geographic background.",
    "Appearance Bias": "A person's competence, character, and worth are defined by their actions and abilities, not their physical appearance.",
    "Political Bias": "Political beliefs are diverse and complex; they should be discussed on their merits without resorting to stereotypes.",
    "Workplace Stereotype": "Professional effectiveness is determined by individual skills, dedication, and experience rather than stereotypical assumptions.",
}


# ─── SEMANTIC MATCHING ENGINE ───────────────────────────────────────────────────
@st.cache_resource
def load_semantic_matcher():
    """Loads a lightweight sentence-transformer for matching input to templates."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Pre-encode all template patterns
    patterns = [t[0] for t in MITIGATION_TEMPLATES]
    embeddings = model.encode(patterns, convert_to_tensor=True)
    return model, embeddings

@st.cache_resource
def load_mitigator():
    """Loads FLAN-T5-base as a fallback for novel sentences."""
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model = model.to("cpu")
    return model, tokenizer


def mitigate_sentence(sentence: str, categories: list) -> str:
    """
    Advanced Hybrid Mitigation Engine:
    1. Semantic Retrieval: Finds the most relevant mitigation patterns from the knowledge base.
    2. Dynamic Few-Shot Prompting: Uses those patterns as "hints" for the local transformer.
    3. Contextual Generalization: Forces the model to focus on individual merit.
    """

    # ── STEP 1: Semantic Retrieval ──
    matcher, template_embeddings = load_semantic_matcher()
    input_embedding = matcher.encode(sentence, convert_to_tensor=True)
    
    from sentence_transformers import util
    similarities = util.cos_sim(input_embedding, template_embeddings)[0]
    
    # Get top 2 matches for dynamic examples
    top_k = 2
    top_scores, top_indices = similarities.topk(k=top_k)
    
    best_score = top_scores[0].item()
    best_idx = top_indices[0].item()

    # Exact/Near match bypass (very high confidence)
    if best_score > 0.92:
        return MITIGATION_TEMPLATES[best_idx][1]

    # ── STEP 2: Dynamic Few-Shot Prompt Construction ──
    # We pull the best matching templates to "teach" the model how to handle this specific bias
    dynamic_examples = ""
    for idx in top_indices:
        ex_input, ex_output = MITIGATION_TEMPLATES[idx.item()]
        dynamic_examples += f"Input: {ex_input}\nNeutral: {ex_output}\n\n"

    # Enhanced instruction for complex/unknown sentences
    bias_context = f" ({', '.join(categories)} bias)" if categories else ""
    
    prompt = f"""Task: Neutralize social bias in the input sentence.
Rules:
1. Replace group stereotypes with individual-based merit.
2. Maintain the professional tone and original meaning.
3. Do not simply invert the bias; generalize it to all people.
4. If the sentence is complex, ensure the neutral version remains grammatically coherent.

### Reference Examples for Style:
{dynamic_examples}### Your Task:
Input: {sentence}{bias_context}
Neutral:"""

    # ── STEP 3: Transformer Execution ──
    model, tokenizer = load_mitigator()
    inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
    
    # Optimized sampling for complex sentence generation
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        num_beams=5,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    
    rewritten = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    # Cleanup logic
    prefixes = ["Neutral version:", "Neutral:", "Response:", "Rewritten:", "Output:"]
    for prefix in prefixes:
        if rewritten.lower().startswith(prefix.lower()):
            rewritten = rewritten[len(prefix):].strip()
            
    # Check if the model just echoed the input or failed
    clean_rewritten = rewritten.lower().strip(" .!?\t\n")
    clean_sentence = sentence.lower().strip(" .!?\t\n")
            
    if len(rewritten) < 5 or clean_rewritten == clean_sentence:
        # Fallback to category-specific reasoning if generation fails
        cat = categories[0] if categories else "this topic"
        return CATEGORY_FALLBACKS.get(cat, 
            f"Statements regarding {cat.lower()} should be framed around individual performance and objective criteria rather than group identity.")
        
    return rewritten


def process_paragraph(paragraph: str):
    """
    Segments paragraph into sentences, runs detection on each, and mitigates if biased.
    Returns full analysis payload.
    """
    if not paragraph.strip():
         return {"is_biased": False, "max_score": 0, "severity": "None", "color": "gray", "categories": [], "edits": [], "original_highlighted_html": "", "mitigated_paragraph": ""}

    # ── STEP 1: Full-Paragraph AI Mitigation (Preferred) ──
    # Sending the whole paragraph to the AI engine allows for better context and coherence.
    ai_res = get_ai_mitigation(paragraph)
    
    if ai_res:
        is_biased = ai_res.get("is_biased", False)
        if is_biased:
            mitigated = ai_res.get("mitigated", paragraph)
            reasoning = ai_res.get("reasoning", "Rewritten for inclusive language.")
            categories = ai_res.get("categories", ["Social Bias"])
            
            # Synthesize the result structure expected by the UI
            return {
                "is_biased": True,
                "max_score": 95.0,
                "severity": "High",
                "color": "#ef4444",
                "categories": categories,
                "edits": [{
                    "original": paragraph,
                    "mitigated": mitigated,
                    "reasoning": reasoning,
                    "categories": categories,
                    "score": 95.0,
                    "severity": "High"
                }],
                # For UI highlighting, we highlight the whole block if it's biased
                "original_highlighted_html": f"<span class='bias-span' style='background-color:rgba(239, 68, 68, 0.2); border-bottom: 2px solid #ef4444;'>{paragraph}</span>",
                "mitigated_paragraph": mitigated
            }
        else:
            return {
                "is_biased": False,
                "max_score": 0,
                "severity": "None",
                "color": "#10b981",
                "categories": [],
                "edits": [],
                "original_highlighted_html": paragraph,
                "mitigated_paragraph": paragraph
            }

    # ── STEP 2: Local Sentence-Level Fallback (No AI Available) ──
    # Segment by punctuation while preserving delimiters and whitespace
    segments = re.split(r'([.!?]+(?:\s+|$|\n))', paragraph)
    
    final_mitigated_segments = []
    edits = []
    
    max_score = 0.0
    highest_severity = "Low"
    all_categories = set()
    overall_color = "#10b981"
    
    is_paragraph_biased = False
    html_segments = []
    
    for segment in segments:
        if re.search(r'[a-zA-Z0-9]', segment):
            clean_sentence = segment.strip()
            det = detect_sentence_bias(clean_sentence)
            
            if det["is_biased"]:
                is_paragraph_biased = True
                max_score = max(max_score, det["score"])
                all_categories.update(det["categories"])
                
                # Mitigate using local hybrid engine
                mitigated = mitigate_sentence(clean_sentence, det["categories"])
                
                edits.append({
                    "original": clean_sentence,
                    "mitigated": mitigated,
                    "reasoning": "Rewritten to remove identity-based generalizations.",
                    "categories": det["categories"],
                    "score": det["score"],
                    "severity": det["severity"]
                })
                
                # Highlight in original text
                html_segment = generate_highlighted_html(clean_sentence, det["spans"])
                
                # Reconstruct
                leading_ws = segment[:len(segment) - len(segment.lstrip())]
                trailing_ws = segment[len(segment.rstrip()):]
                final_mitigated_segments.append(f"{leading_ws}{mitigated}{trailing_ws}")
                html_segments.append(f"{leading_ws}{html_segment}{trailing_ws}")
            else:
                final_mitigated_segments.append(segment)
                html_segments.append(segment)

            # Track max severity color
            if is_paragraph_biased:
                if max_score > 85:
                    highest_severity = "Severe"
                    overall_color = "#991b1b"
                elif max_score > 60 and highest_severity not in ["Severe"]:
                    highest_severity = "High"
                    overall_color = "#ef4444"
                elif max_score > 40 and highest_severity not in ["Severe", "High"]:
                    highest_severity = "Moderate"
                    overall_color = "#f59e0b"
        else:
            final_mitigated_segments.append(segment)
            html_segments.append(segment)
            
    return {
        "is_biased": is_paragraph_biased,
        "max_score": max_score,
        "severity": highest_severity,
        "color": overall_color,
        "categories": list(all_categories),
        "edits": edits,
        "original_highlighted_html": "".join(html_segments),
        "mitigated_paragraph": "".join(final_mitigated_segments)
    }
