from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False
)

def detect_emotion(text):
    if not text or text.strip() == "":
        return "neutral", 0.0

    result = emotion_classifier(text)[0]

    emotion_label = result["label"]
    confidence = round(result["score"], 3)

    return emotion_label, confidence