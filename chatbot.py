import random

# ---------------- QUOTES ---------------- #

MOTIVATIONAL_QUOTES = [
    "This feeling will pass. You are stronger than you think.",
    "Even the darkest night will end and the sun will rise.",
    "You have survived 100% of your worst days so far.",
    "Your mind is tired, not broken.",
    "Healing is not linear, and that’s okay."
]

# ---------------- YOUTUBE VIDEOS ---------------- #

YOUTUBE_VIDEOS = {
    "anxiety": "https://www.youtube.com/watch?v=O-6f5wQXSu8",
    "stress": "https://www.youtube.com/watch?v=2FGR-OspxsU",
    "depression": "https://www.youtube.com/watch?v=XiCrniLQGYc",
    "sleep": "https://www.youtube.com/watch?v=nm1TxQj9IsQ",
    "motivation": "https://www.youtube.com/watch?v=wnHW6o8WMas",
    "breathing": "https://www.youtube.com/watch?v=SEfs5TJZ6Nk"
}

# ---------------- THERAPIST ENGINE ---------------- #

def generate_reply(message):
    msg = message.lower()

    # 🚨 SUICIDE / SELF-HARM (CRITICAL)
    if any(word in msg for word in ["suicide", "kill myself", "end my life", "die", "self harm"]):
        return (
            "I’m really glad you told me this. What you’re feeling is very serious, "
            "but you don’t have to go through it alone.\n\n"
            "You matter. Your life has value, even if it doesn’t feel like it right now.\n\n"
            "Please consider reaching out to someone immediately:\n"
            "📞 **India Suicide Helpline: 9152987821**\n\n"
            "If you can, tell me — what made you feel this way today?"
        )

    # 😰 ANXIETY
    if any(word in msg for word in ["anxious", "anxiety", "panic", "nervous"]):
        return (
            "Anxiety can make your thoughts race and your body feel unsafe, even when you are not in danger.\n\n"
            "Let’s slow things down for a moment. Take a deep breath in… and out.\n\n"
            "What usually triggers this anxiety for you?\n\n"
            f"🎥 You may find this helpful: {YOUTUBE_VIDEOS['breathing']}"
        )

    # 📚 EXAMS / STUDIES
    if any(word in msg for word in ["exam", "test", "study", "marks", "result"]):
        return (
            "Academic pressure can feel overwhelming, especially when expectations are high.\n\n"
            "You are more than your marks. Exams test memory — not your worth.\n\n"
            "Which part is stressing you the most: preparation, time, or fear of failure?"
        )

    # 😢 SADNESS / DEPRESSION
    if any(word in msg for word in ["sad", "depressed", "unhappy", "hopeless", "empty"]):
        return (
            "I’m really sorry you’re feeling this way. Feeling low can drain your energy and hope.\n\n"
            "You’re not weak for feeling this — you’re human.\n\n"
            "Has this sadness been there for a long time, or did something specific happen recently?\n\n"
            f"💬 Quote for you: \"{random.choice(MOTIVATIONAL_QUOTES)}\""
        )

    # 😡 ANGER
    if any(word in msg for word in ["angry", "anger", "frustrated", "irritated"]):
        return (
            "Anger often hides deeper emotions like hurt, disappointment, or feeling ignored.\n\n"
            "Your feelings are valid. Let’s understand them instead of pushing them away.\n\n"
            "What exactly happened that made you feel angry?"
        )

    # 😵 STRESS / PRESSURE
    if any(word in msg for word in ["stress", "pressure", "burden", "overwhelmed"]):
        return (
            "It sounds like you’re carrying a lot on your shoulders right now.\n\n"
            "When stress piles up, even small things can feel heavy.\n\n"
            "What responsibilities are weighing on you the most?\n\n"
            f"🎥 Stress relief video: {YOUTUBE_VIDEOS['stress']}"
        )

    # 😴 SLEEP PROBLEMS
    if any(word in msg for word in ["sleep", "insomnia", "cannot sleep"]):
        return (
            "Sleep issues often come from an overactive mind.\n\n"
            "Your body wants rest, but your thoughts won’t slow down.\n\n"
            "Do you usually think a lot before bedtime?\n\n"
            f"🎥 Sleep relaxation video: {YOUTUBE_VIDEOS['sleep']}"
        )

    # ❤️ LONELINESS
    if any(word in msg for word in ["lonely", "alone", "no one"]):
        return (
            "Feeling lonely can hurt deeply, even when people are around.\n\n"
            "You deserve connection and understanding.\n\n"
            "Do you feel emotionally disconnected from others, or physically alone?"
        )

    # 🌱 DEFAULT THERAPIST RESPONSE
    return (
        "Thank you for opening up to me.\n\n"
        "I’m here to listen, without judgment.\n\n"
        "Can you tell me more about what’s been going on in your mind lately?"
    )