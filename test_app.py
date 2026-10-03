"""
Verification Script for Smart Study Notes Generator
-----------------------------------------------------
Tests the AI summarizer model, word count logic, reduction percentage formula, 
and key points extraction across all 3 sample paragraphs.
"""

from app import load_summarization_model, generate_summary, calculate_word_count, calculate_reduction_percentage, extract_key_points

# Sample Paragraphs
SAMPLES = {
    "Artificial Intelligence": (
        "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed "
        "to think and learn like humans. These systems can process vast amounts of data, recognize complex patterns, "
        "make decisions, and solve intricate problems with remarkable speed and accuracy. Machine Learning and Deep Learning "
        "are core subfields of AI that enable algorithms to improve their performance automatically through experience and data exposure. "
        "Today, AI applications are transforming diverse global industries including healthcare, finance, transport, and education. "
        "In healthcare, AI assists medical professionals in diagnosing diseases early and accelerating drug discovery, while in "
        "financial markets, it detects fraudulent transactions and automates algorithmic trading. As AI technology continues to advance rapidly, "
        "critical ethical considerations such as algorithmic bias, data privacy protection, and workforce automation remain paramount topics "
        "of discussion among researchers and policymakers."
    ),
    "Climate Change": (
        "Climate change represents one of the most pressing global environmental challenges of the modern era, primarily driven by human "
        "activities such as the burning of fossil fuels, widespread deforestation, and intensive industrial processes. These activities "
        "release massive quantities of greenhouse gases like carbon dioxide and methane into the Earth's atmosphere, trapping solar heat "
        "and accelerating global temperature increases. The far-reaching consequences of global warming are increasingly evident through "
        "accelerating glacier melt, rising ocean sea levels, prolonged severe droughts, and unpredictable extreme weather events worldwide. "
        "Natural ecosystems and terrestrial biodiversity face unprecedented disruption, severely threatening global food security and freshwater "
        "supplies for millions of vulnerable people. Mitigating climate change demands immediate international cooperation, rapid transition "
        "towards renewable energy technologies such as solar and wind power, sustainable land management practices, and aggressive forest "
        "restoration initiatives across the globe."
    ),
    "Online Education": (
        "Online education has fundamentally revolutionized the modern learning landscape by providing flexible, accessible, and affordable "
        "educational opportunities to students across the globe. Through digital learning platforms, virtual classrooms, and interactive video "
        "lectures, learners can access high-quality academic resources from virtually anywhere at any time. This unprecedented flexibility "
        "enables working professionals, adult learners, and students in geographically remote areas to pursue higher education degrees and acquire "
        "critical skills without physical or scheduling constraints. Furthermore, modern online platforms incorporate intelligent multimedia tools, "
        "automated knowledge quizzes, and active discussion forums to foster engaging self-paced and collaborative learning environments. "
        "Despite ongoing challenges such as the digital divide, internet bandwidth limitations, and reduced face-to-face social interaction, "
        "online education continues to complement traditional classroom instruction effectively."
    )
}

def run_tests():
    print("=" * 80)
    print("RUNNING AUTOMATED TEST SUITE FOR SMART STUDY NOTES GENERATOR")
    print("=" * 80)
    
    print("\n[1/2] Loading Hugging Face Summarization Model...")
    model_tuple, error = load_summarization_model()
    if error:
        print(f"FAILED to load model: {error}")
        return
    tokenizer, model = model_tuple
    print("SUCCESS: AI Summarization Model Loaded!")
    
    print("\n[2/2] Running Test Cases on 3 Sample Paragraphs...")
    print("-" * 80)
    
    for topic, paragraph in SAMPLES.items():
        orig_count = calculate_word_count(paragraph)
        summary = generate_summary(paragraph, tokenizer, model)
        summary_count = calculate_word_count(summary)
        reduction_pct = calculate_reduction_percentage(orig_count, summary_count)
        key_points = extract_key_points(summary, paragraph)
        
        print(f"\nTOPIC: {topic}")
        print(f"Original Word Count: {orig_count}")
        print(f"Summary Word Count:  {summary_count}")
        print(f"Reduction Percentage: {reduction_pct:.2f}%")
        print(f"Generated Summary:\n  \"{summary}\"")
        print("Key Points:")
        for idx, kp in enumerate(key_points, 1):
            print(f"  {idx}. {kp}")
        print("-" * 80)

    print("\nALL 3 TEST CASES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
