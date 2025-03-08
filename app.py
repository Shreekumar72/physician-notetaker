import streamlit as st
import requests

# Define API URL (Update if using a public URL)
API_URL = "https://physician-notetaker.onrender.com"

  # Make sure this matches your FastAPI server
  # Update with public URL if needed

st.title("👨‍⚕️ Physician Notetaker - Medical NLP System")

# Input Text
text_input = st.text_area("Enter Patient Conversation:")

if st.button("Analyze Text"):
    if text_input:
        # Send API request
        response = requests.post(f"{API_URL}/analyze/", json={"text": text_input})
        if response.status_code == 200:
            data = response.json()
            st.subheader("📌 Extracted Medical Details")
            st.json(data["medical_info"])

            st.subheader("📌 Summarized Report")
            st.write(data["summary"])

            

            st.subheader("📌 Sentiment Analysis")
            st.write(f"Sentiment: **{data['sentiment']['Sentiment']}**")
        else:
            st.error("Failed to process text. Try again.")
    else:
        st.warning("Please enter a conversation.")

if st.button("Generate SOAP Note"):
    if text_input:
        # Send API request
        response = requests.post(f"{API_URL}/generate-soap/", json={"text": text_input})
        if response.status_code == 200:
            data = response.json()
            st.subheader("📌 Generated SOAP Note")
            st.json(data["SOAP_Note"])
        else:
            st.error("Failed to generate SOAP note.")
    else:
        st.warning("Please enter a conversation.")
