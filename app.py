"""
Smart Study Notes Generator
---------------------------
A Streamlit web application using Hugging Face Transformers to generate 
concise summaries and key study points from study paragraphs.

Developed for MCA Mini Project Demonstration.
"""

import streamlit as st
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -----------------------------------------------------------------------------
# 1. Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Study Notes Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a sleek, modern, student-friendly web UI
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    .main {
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Title Card Styling */
    .title-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .title-card h1 {
        margin: 0;
        font-size: 2.3rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .title-card p {
        margin-top: 0.5rem;
        font-size: 1.05rem;
        color: #e2e8f0;
    }
    
    /* Result Box Styling */
    .summary-box {
        background-color: #ffffff;
        border-left: 5px solid #2563eb;
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .keypoints-box {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .keypoint-item {
        margin-bottom: 0.5rem;
        font-size: 1rem;
        color: #1e293b;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3c72;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. AI Model Loading (Cached for fast performance)
# -----------------------------------------------------------------------------
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

@st.cache_resource(show_spinner=False)
def load_summarization_model():
    """
    Loads pre-trained DistilBART tokenizer and Seq2Seq model from Hugging Face.
    DistilBART is lightweight, accurate, fast, and completely free (no API key needed).
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        return (tokenizer, model), None
    except Exception as e:
        return None, str(e)


# -----------------------------------------------------------------------------
# 3. Helper Functions for NLP & Key Points Extraction
# -----------------------------------------------------------------------------
def calculate_word_count(text: str) -> int:
    """Calculates total word count in a given text string."""
    if not text or not text.strip():
        return 0
    return len(text.strip().split())


def calculate_reduction_percentage(original_count: int, summary_count: int) -> float:
    """
    Formula:
    Reduction Percentage = ((Original Word Count - Summary Word Count) / Original Word Count) * 100
    """
    if original_count == 0:
        return 0.0
    reduction = ((original_count - summary_count) / original_count) * 100.0
    return max(0.0, round(reduction, 2))


def extract_key_points(summary_text: str, original_text: str) -> list:
    """
    Extracts 3-5 concise, important key study points from the generated summary and main text.
    """
    combined_text = summary_text + " " + original_text
    raw_sentences = re.split(r'(?<=[.!?]) +', combined_text.strip())
    
    cleaned_sentences = []
    seen = set()
    
    for sentence in raw_sentences:
        clean_s = sentence.strip()
        if len(clean_s) > 20 and clean_s.lower() not in seen:
            seen.add(clean_s.lower())
            cleaned_sentences.append(clean_s)
            
    if len(cleaned_sentences) == 0:
        return [summary_text]
    elif len(cleaned_sentences) <= 5:
        return cleaned_sentences
    else:
        return cleaned_sentences[:5]


def generate_summary(text: str, tokenizer, model) -> str:
    """
    Generates summary text using Seq2Seq model inference.
    """
    orig_count = calculate_word_count(text)
    max_len = max(30, int(orig_count * 0.55))
    min_len = max(15, int(orig_count * 0.25))
    
    inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        max_length=max_len,
        min_length=min_len,
        early_stopping=True,
        no_repeat_ngram_size=3
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()


# -----------------------------------------------------------------------------
# 4. Sample Texts for Demo / Testing
# -----------------------------------------------------------------------------
SAMPLE_AI = (
    "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed "
    "to think and learn like humans. These systems can process vast amounts of data, recognize complex patterns, "
    "make decisions, and solve intricate problems with remarkable speed and accuracy. Machine Learning and Deep Learning "
    "are core subfields of AI that enable algorithms to improve their performance automatically through experience and data exposure. "
    "Today, AI applications are transforming diverse global industries including healthcare, finance, transport, and education. "
    "In healthcare, AI assists medical professionals in diagnosing diseases early and accelerating drug discovery, while in "
    "financial markets, it detects fraudulent transactions and automates algorithmic trading. As AI technology continues to advance rapidly, "
    "critical ethical considerations such as algorithmic bias, data privacy protection, and workforce automation remain paramount topics "
    "of discussion among researchers and policymakers."
)

SAMPLE_CLIMATE = (
    "Climate change represents one of the most pressing global environmental challenges of the modern era, primarily driven by human "
    "activities such as the burning of fossil fuels, widespread deforestation, and intensive industrial processes. These activities "
    "release massive quantities of greenhouse gases like carbon dioxide and methane into the Earth's atmosphere, trapping solar heat "
    "and accelerating global temperature increases. The far-reaching consequences of global warming are increasingly evident through "
    "accelerating glacier melt, rising ocean sea levels, prolonged severe droughts, and unpredictable extreme weather events worldwide. "
    "Natural ecosystems and terrestrial biodiversity face unprecedented disruption, severely threatening global food security and freshwater "
    "supplies for millions of vulnerable people. Mitigating climate change demands immediate international cooperation, rapid transition "
    "towards renewable energy technologies such as solar and wind power, sustainable land management practices, and aggressive forest "
    "restoration initiatives across the globe."
)

SAMPLE_EDUCATION = (
    "Online education has fundamentally revolutionized the modern learning landscape by providing flexible, accessible, and affordable "
    "educational opportunities to students across the globe. Through digital learning platforms, virtual classrooms, and interactive video "
    "lectures, learners can access high-quality academic resources from virtually anywhere at any time. This unprecedented flexibility "
    "enables working professionals, adult learners, and students in geographically remote areas to pursue higher education degrees and acquire "
    "critical skills without physical or scheduling constraints. Furthermore, modern online platforms incorporate intelligent multimedia tools, "
    "automated knowledge quizzes, and active discussion forums to foster engaging self-paced and collaborative learning environments. "
    "Despite ongoing challenges such as the digital divide, internet bandwidth limitations, and reduced face-to-face social interaction, "
    "online education continues to complement traditional classroom instruction effectively."
)


# -----------------------------------------------------------------------------
# 5. Session State Management
# -----------------------------------------------------------------------------
if "input_paragraph" not in st.session_state:
    st.session_state.input_paragraph = ""

def load_sample(text):
    st.session_state.input_paragraph = text

def clear_input():
    st.session_state.input_paragraph = ""


# -----------------------------------------------------------------------------
# 6. Streamlit User Interface
# -----------------------------------------------------------------------------

# Header Section
st.markdown("""
    <div class="title-card">
        <h1>🎓 Smart Study Notes Generator</h1>
        <p>Transform verbose study material into concise summaries and key bullet points using Generative AI (Hugging Face Transformers)</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with Model & Project Info
with st.sidebar:
    st.header("ℹ️ Project Information")
    st.markdown("**Course:** MCA Mini Project")
    st.markdown(f"**AI Model:** `{MODEL_NAME}`")
    st.markdown("**Frameworks:** Streamlit & PyTorch")
    st.markdown("---")
    
    st.subheader("💡 Features")
    st.markdown("- 🤖 **AI Summarization** via DistilBART Transformer")
    st.markdown("- 📌 **Key Points Extraction** for quick revision")
    st.markdown("- 📊 **Text Reduction Metrics** & word count comparison")
    st.markdown("- ⚡ **1-Click Sample Testing** for easy demonstration")
    st.markdown("---")
    
    st.subheader("🧪 Quick Test Samples")
    st.caption("Click a sample to load it into the input area:")
    if st.button("🤖 1. Artificial Intelligence", use_container_width=True):
        load_sample(SAMPLE_AI)
    if st.button("🌍 2. Climate Change", use_container_width=True):
        load_sample(SAMPLE_CLIMATE)
    if st.button("📚 3. Online Education", use_container_width=True):
        load_sample(SAMPLE_EDUCATION)

# Main Input Section
st.subheader("📥 Input Study Paragraph")

# Text area bound to session_state
user_input = st.text_area(
    label="Enter or paste your study paragraph:",
    value=st.session_state.input_paragraph,
    height=200,
    placeholder="Paste a paragraph from your textbook, research paper, or study material here...",
    key="text_area_input"
)

# Action Buttons Row
col_btn1, col_btn2, col_spacer = st.columns([2, 1, 3])

with col_btn1:
    generate_btn = st.button("✨ Generate Summary & Study Notes", type="primary", use_container_width=True)

with col_btn2:
    if st.button("🗑️ Clear Input", use_container_width=True):
        clear_input()
        st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. Processing & Output Generation
# -----------------------------------------------------------------------------
if generate_btn:
    current_input = user_input.strip()
    
    # Requirement 9: Handle empty input properly
    if not current_input:
        st.warning("⚠️ **Empty Input Detected!** Please enter or paste a paragraph of text before generating a summary.")
    else:
        orig_word_count = calculate_word_count(current_input)
        
        # Friendly feedback for very short text
        if orig_word_count < 15:
            st.info("💡 **Tip:** Your input text is quite short (less than 15 words). Summarization yields best results on paragraphs with at least 30-50 words.")

        # Load model with progress indicator
        with st.spinner("⏳ Loading Generative AI Summarization Model..."):
            model_tuple, error_msg = load_summarization_model()
            
        if error_msg:
            # Requirement 10: Handle errors gracefully
            st.error(f"❌ **Failed to load AI Model:** {error_msg}")
        else:
            tokenizer, model = model_tuple
            
            with st.spinner("🤖 AI is analyzing the paragraph and creating study notes..."):
                try:
                    generated_summary = generate_summary(current_input, tokenizer, model)
                    summary_word_count = calculate_word_count(generated_summary)
                    reduction_percentage = calculate_reduction_percentage(orig_word_count, summary_word_count)
                    key_points = extract_key_points(generated_summary, current_input)
                    
                    # Requirement 4-8 & Output Section Display
                    st.success("✅ **Study Notes Generated Successfully!**")
                    
                    # Section: Summary Metrics Cards
                    st.subheader("📊 Summary Analytics & Metrics")
                    m_col1, m_col2, m_col3 = st.columns(3)
                    
                    with m_col1:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{orig_word_count}</div>
                                <div class="metric-label">Original Word Count</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with m_col2:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{summary_word_count}</div>
                                <div class="metric-label">Summary Word Count</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with m_col3:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{reduction_percentage:.1f}%</div>
                                <div class="metric-label">Text Reduction Percentage</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Output Layout: 2 Columns for side-by-side study review
                    out_col1, out_col2 = st.columns(2)

                    with out_col1:
                        st.subheader("📄 Original Paragraph")
                        st.markdown(f'<div class="summary-box">{current_input}</div>', unsafe_allow_html=True)

                    with out_col2:
                        st.subheader("⚡ Generated Summary")
                        st.markdown(f'<div class="summary-box" style="border-left-color: #8b5cf6;">{generated_summary}</div>', unsafe_allow_html=True)

                    # Section: Key Study Points
                    st.subheader("📌 Key Study Points (Quick Revision)")
                    st.markdown('<div class="keypoints-box">', unsafe_allow_html=True)
                    for idx, point in enumerate(key_points, 1):
                        st.markdown(f'<div class="keypoint-item"><strong>Point {idx}:</strong> {point}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as eval_err:
                    st.error(f"❌ **An error occurred during summarization:** {str(eval_err)}")
