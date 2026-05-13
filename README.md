# 🛡️ AI Bias Guard

A production-quality academic demo that leverages state-of-the-art NLP models to detect, classify, and mitigate social biases in text. Built with a premium Streamlit interface.

## 🚀 Key Features
- **Hybrid Semantic Detection**: Combines zero-shot transformer classification (`BART-large-MNLI`) with lexical keyword matching for robust analysis.
- **Multi-Label Classification**: Detects and categorizes biases across 10 categories: Gender, Age, Race, Religion, Socioeconomic, Disability, Nationality, Appearance, Politics, and Workplace Stereotypes.
- **Intelligent Highlighting**: Pinpoints specific biased phrases within paragraphs using regex-based span extraction.
- **Smart Mitigation**: Generates neutral, generalized rewrites using `FLAN-T5-large` with few-shot prompting to ensure context preservation and zero repetition.
- **Premium UI**: Modern dark-mode dashboard with glassmorphism components and real-time inference monitoring.

## 📁 Project Structure
- `app.py`: Main Streamlit application and UI layout.
- `detector/`:
    - `bias_detector.py`: Core detection pipeline (Semantic + Lexical + Toxicity).
    - `mitigation.py`: Seq2Seq rewriting engine with few-shot generalization.
    - `scoring.py`: Hybrid severity and confidence mapping.
    - `highlighting.py`: HTML span extraction for UI rendering.
    - `categories.py`: Bias category definitions and lexicons.
- `assets/`: Custom CSS for premium styling.
- `data/`: Local storage for feedback and persistent data.

## 🛠️ Setup & Usage

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```
   *The application will automatically download required models on the first run. Please ensure you have a stable internet connection.*

3. **Inference Time**
   The application uses `BART-large` and `FLAN-T5-large` locally. Expect ~2-5 seconds for full analysis and mitigation of a standard paragraph on most modern hardware.
