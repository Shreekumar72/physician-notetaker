from fastapi import FastAPI
from pydantic import BaseModel
import nlp_processing  # Import full module

app = FastAPI()

class MedicalTextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Physician Notetaker API is Running 🚀"}

@app.post("/analyze/")
def analyze_text(input_text: MedicalTextRequest):
    extracted_details = nlp_processing.extract_medical_details(input_text.text)
    summary = nlp_processing.summarize_text(input_text.text)
    sentiment = nlp_processing.analyze_sentiment(input_text.text)

    return {
        "summary": summary,
        "medical_info": extracted_details,
        "sentiment": sentiment
    }

@app.post("/generate-soap/")
def generate_soap(input_text: MedicalTextRequest):
    extracted_details = nlp_processing.extract_medical_details(input_text.text)
    soap_note = nlp_processing.generate_soap_note(
        "John Doe",
        extracted_details["Symptoms"],
        extracted_details["Diagnosis"],
        extracted_details["Treatment"],
        "Full recovery expected within 6 months"
    )

    return {"SOAP_Note": soap_note}
