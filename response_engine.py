import random

def generate_response(emotion, user_msg):
    """
    Mental-health aware response generator
    Uses empathy + validation + gentle coping + open question
    """

    responses = {

        "depressed": [
            "I’m really sorry you’re feeling this much pain. What you’re experiencing sounds overwhelming, and it’s okay to feel this way. Sometimes taking a slow breath or talking things out can help a little. Would you like to share what’s been hurting you the most?",
            
            "It sounds like you’ve been carrying a lot emotionally. You’re not weak for feeling this way, and you don’t have to go through it alone. What has been making things feel so heavy lately?"
        ],

        "sad": [
            "I hear that you’re feeling low right now. Difficult moments can drain a lot of energy, and it’s completely valid to feel this way. What’s been bothering you recently?",
            
            "That sounds really tough. Even small setbacks can feel overwhelming sometimes. Would you like to talk about what happened?"
        ],

        "happy": [
            "That’s good to hear 😊 It sounds like something positive is happening in your life. What’s been making you feel this way?",
            
            "I’m glad you’re feeling better today. Moments like these are important. Would you like to share what’s going well?"
        ]
    }

    # fallback
    default_response = (
        "I’m here to listen. You can share whatever is on your mind, "
        "and we can take it one step at a time."
    )

    reply_list = responses.get(emotion, [])
    reply = random.choice(reply_list) if reply_list else default_response

    return {
        "emotion": emotion,
        "reply": reply
    }