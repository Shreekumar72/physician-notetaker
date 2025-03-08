from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Physician Notetaker API is Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
