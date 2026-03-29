# emotion_model.py

from transformers import pipeline

# Load emotion detection model (REAL ML MODEL)
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

# Map model labels to project-friendly emotions
LABEL_MAP = {
    "sadness": "sad",
    "anger": "anger",
    "fear": "stress",
    "joy": "happy",
    "neutral": "neutral"
}

def detect_emotion(text):
    if not text or text.strip() == "":
        return "neutral"

    results = emotion_classifier(text)[0]

    # Get highest confidence emotion
    top_emotion = max(results, key=lambda x: x["score"])
    label = top_emotion["label"].lower()

    return LABEL_MAP.get(label, "neutral")