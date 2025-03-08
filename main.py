from fastapi import FastAPI
from pydantic import BaseModel
from nlp_processing import extract_medical_details, summarize_text, extract_keywords, analyze_sentiment, generate_soap_note

app = FastAPI()

class MedicalTextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Physician Notetaker API is Running 🚀"}

@app.post("/analyze/")
def analyze_text(input_text: MedicalTextRequest):
    extracted_details = extract_medical_details(input_text.text)
    summary = summarize_text(input_text.text)
    keywords = extract_keywords(input_text.text)
    sentiment = analyze_sentiment(input_text.text)

    return {
        "summary": summary,
        "medical_info": extracted_details,
        "keywords": keywords,
        "sentiment": sentiment
    }

@app.post("/generate-soap/")
def generate_soap(input_text: MedicalTextRequest):
    extracted_details = extract_medical_details(input_text.text)
    soap_note = generate_soap_note(
        "John Doe",  # Example Patient Name
        extracted_details["Symptoms"],
        extracted_details["Diagnosis"],
        extracted_details["Treatment"],
        "Full recovery expected within 6 months"
    )

    return {"SOAP_Note": soap_note}
