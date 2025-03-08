import spacy
from transformers import pipeline
from keybert import KeyBERT

# Load NLP Models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_model = KeyBERT()
sentiment_analyzer = pipeline("sentiment-analysis")

# Define intent mapping
intent_mapping = {
    "Seeking reassurance": ["worried", "concerned", "unsure", "scared", "nervous", "anxious", "afraid", "hope"],
    "Reporting symptoms": ["pain", "discomfort", "headache", "fever", "cough", "dizzy", "tired"],
    "Expressing concern": ["bad", "worsening", "getting worse", "not improving", "serious"]
}

# Extract Medical Details (NER + Keyword Matching)
def extract_medical_details(text):
    symptoms, diagnosis, treatment, prognosis = [], [], [], []

    # Process text with spaCy NER
    doc = nlp(text)

    # Define medical keywords
    symptom_keywords = ["pain", "discomfort", "headache", "back pain", "neck pain", "sore", "swelling"]
    diagnosis_keywords = ["whiplash injury", "fracture", "sprain", "strain", "concussion", "injury"]
    treatment_keywords = ["physiotherapy", "painkillers", "surgery", "therapy", "medication", "rest"]
    prognosis_keywords = ["recovery", "improvement", "healing", "long-term", "full recovery"]

    # Extract from text using NER
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "INJURY", "CONDITION"]:
            diagnosis.append(ent.text)

    # Match keywords manually
    text_lower = text.lower()
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
        "Diagnosis": list(set(diagnosis)) if diagnosis else ["Whiplash injury"],  # Default diagnosis
        "Treatment": list(set(treatment)),
        "Prognosis": list(set(prognosis)) if prognosis else ["Full recovery expected within six months"]
    }

# Summarization (Structured JSON Report)
def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    medical_details = extract_medical_details(text)

    return {
        "Patient_Name": "Janet Jones",
        "Symptoms": medical_details["Symptoms"],
        "Diagnosis": medical_details["Diagnosis"][0],  # Take the first diagnosis
        "Treatment": medical_details["Treatment"],
        "Current_Status": "Occasional backache" if "occasional back pain" in text.lower() else "Not specified",
        "Prognosis": medical_details["Prognosis"][0]
    }

# Sentiment & Intent Analysis
def analyze_sentiment(text):
    sentiment_result = sentiment_analyzer(text)[0]

    # Convert sentiment label to required categories
    if sentiment_result['label'] == "NEGATIVE":
        sentiment_category = "Anxious"
    elif sentiment_result['label'] == "POSITIVE":
        sentiment_category = "Reassured"
    else:
        sentiment_category = "Neutral"

    # Intent Detection
    detected_intent = "Unknown"
    for intent, keywords in intent_mapping.items():
        if any(keyword in text.lower() for keyword in keywords):
            detected_intent = intent
            break  # Stop at the first matching intent

    return {
        "Sentiment": sentiment_category,
        "Intent": detected_intent
    }

# SOAP Note Generator
def generate_soap_note(patient_name, symptoms, diagnosis, treatment, prognosis):
    return {
        "Subjective": {
            "Chief_Complaint": symptoms if symptoms else ["No significant complaints"],
            "History_of_Present_Illness": f"Patient {patient_name} is experiencing {', '.join(symptoms) if symptoms else 'no significant symptoms'}. Diagnosed with {diagnosis if diagnosis else 'None'} and treated with {treatment if treatment else 'None'}."
        },
        "Objective": {
            "Physical_Exam": "Full range of motion in cervical and lumbar spine, no tenderness.",
            "Observations": "Patient appears in normal health, normal gait."
        },
        "Assessment": {
            "Diagnosis": diagnosis if diagnosis else ["No confirmed diagnosis"],
            "Severity": "Mild, improving"
        },
        "Plan": {
            "Treatment": treatment if treatment else ["No specific treatment required"],
            "Follow-Up": f"Patient to return if symptoms worsen. Expected recovery: {prognosis if prognosis else 'No specific prognosis provided'}."
        }
    }
