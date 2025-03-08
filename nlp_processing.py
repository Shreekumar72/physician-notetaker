import spacy
from transformers import pipeline
from keybert import KeyBERT

# Load NLP Models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="t5-small")
kw_model = KeyBERT()
sentiment_analyzer = pipeline("sentiment-analysis")

# Extract Medical Details (NER)
import re

def extract_medical_details(text):
    symptoms = []
    diagnosis = []
    treatment = []
    prognosis = []

    # Define medical keywords
    symptom_keywords = ["pain", "discomfort", "headache", "back pain", "neck pain", "sore", "swelling"]
    diagnosis_keywords = ["whiplash", "fracture", "sprain", "strain", "concussion", "injury"]
    treatment_keywords = ["physiotherapy", "painkillers", "surgery", "therapy", "medication", "rest"]
    prognosis_keywords = ["recovery", "improvement", "healing", "long-term", "full recovery"]

    # Convert text to lowercase for better matching
    text_lower = text.lower()

    # Search for keywords in text
    for word in symptom_keywords:
        if word in text_lower:
            symptoms.append(word)

    for word in diagnosis_keywords:
        if word in text_lower:
            diagnosis.append(word)

    for word in treatment_keywords:
        if word in text_lower:
            treatment.append(word)

    for word in prognosis_keywords:
        if word in text_lower:
            prognosis.append(word)

    return {
        "Symptoms": list(set(symptoms)),
        "Diagnosis": list(set(diagnosis)),
        "Treatment": list(set(treatment)),
        "Prognosis": list(set(prognosis))
    }


# Summarization
def summarize_text(text):
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']


# Keyword Extraction
def extract_keywords(text):
    return kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')


# Sentiment Analysis
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return {"Sentiment": result['label']}


# Test Example (Make sure output is visible)
if __name__ == "__main__":
    test_text = "Patient had whiplash injury, underwent 10 physiotherapy sessions, and still has occasional back pain."

    print("\n🔹 **Extracted Medical Details:**")
    print(extract_medical_details(test_text))

    print("\n🔹 **Summarized Report:**")
    print(summarize_text(test_text))

    print("\n🔹 **Important Keywords:**")
    print(extract_keywords(test_text))

    print("\n🔹 **Sentiment Analysis:**")
    print(analyze_sentiment(test_text))

    # Ensure script execution is confirmed
    print("\n✅ Script executed successfully!")
# SOAP Note Generator
def generate_soap_note(patient_name, symptoms, diagnosis, treatment, prognosis):
    return {
        "Subjective": {
            "Chief_Complaint": symptoms,
            "History_of_Present_Illness": f"Patient {patient_name} is experiencing {', '.join(symptoms)}. Diagnosed with {diagnosis} and treated with {treatment}."
        },
        "Objective": {
            "Physical_Exam": "Full range of motion in cervical and lumbar spine, no tenderness.",
            "Observations": "Patient appears in normal health, normal gait."
        },
        "Assessment": {
            "Diagnosis": diagnosis,
            "Severity": "Mild, improving"
        },
        "Plan": {
            "Treatment": treatment,
            "Follow-Up": f"Patient to return if symptoms worsen. Expected recovery: {prognosis}."
        }
    }

# Test SOAP Note
if __name__ == "__main__":
    test_text = "Patient had whiplash injury, underwent 10 physiotherapy sessions. He still has occasional back pain and has whiplash injuries."

    extracted_details = extract_medical_details(test_text)
    patient_name = "John Doe"  # Example name
    print("\n🔹 **Extracted Medical Details (Debugging):**")
    print(extracted_details)


    # Generate SOAP note
    soap_note = generate_soap_note(
        patient_name,
        extracted_details["Symptoms"],
        extracted_details["Diagnosis"],
        extracted_details["Treatment"],
        "Full recovery expected within 6 months"
    )

    print("\n🔹 **Generated SOAP Note:**")
    print(soap_note)
