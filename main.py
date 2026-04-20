from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

classifier = pipeline("sentiment-analysis")

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

# Create app
app = FastAPI()

# Allow frontend (HTML) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model
classifier = pipeline("sentiment-analysis")

# Input format
class TextInput(BaseModel):
    text: str

# Convert AI result to your business logic
def map_result(label):
    if label.lower() == "positive":
        return "Bullish 📈"
    elif label.lower() == "negative":
        return "Bearish 📉"
    else:
        return "Neutral"

# API endpoint
@app.post("/analyze")
def analyze(input: TextInput):
    result = classifier(input.text)[0]
    mapped = map_result(result["label"])

    return {
        "prediction": mapped,
        "confidence": round(result["score"] * 100, 2)
    }

