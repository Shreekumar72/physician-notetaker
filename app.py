from fastapi import FastAPI

# Force FastAPI to use the root path expected by Hugging Face Spaces
app = FastAPI(root_path="/")

@app.get("/")
def root():
    return {"message": "Physician Notetaker API is Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
