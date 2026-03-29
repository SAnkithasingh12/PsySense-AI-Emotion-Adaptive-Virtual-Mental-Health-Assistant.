def therapist_reply(user_text, emotion):
    user_text = user_text.lower()

    # Core therapist responses
    if emotion == "sad":
        reply = (
            "I’m really glad you shared this with me 💙. "
            "Feeling sad can be heavy, and you don’t have to go through it alone. "
            "What do you think is the main thing affecting you right now?"
        )
        suggestion = "Try writing your thoughts in a notebook for 5 minutes."
        video = "https://www.youtube.com/watch?v=inpok4MKVLM"

    elif emotion == "anxious":
        reply = (
            "It sounds like you’re feeling anxious, and that can be overwhelming. "
            "Let’s slow things down together. "
            "Can you tell me when these anxious thoughts usually start?"
        )
        suggestion = "Practice 4-7-8 breathing for a few minutes."
        video = "https://www.youtube.com/watch?v=YRPh_GaiL8s"

    elif emotion == "happy":
        reply = (
            "I love hearing that you’re feeling happy 😊. "
            "Moments like these are important. "
            "What’s something positive that happened today?"
        )
        suggestion = "Take a moment to appreciate this feeling."
        video = "https://www.youtube.com/watch?v=ZbZSe6N_BXs"

    elif emotion == "angry":
        reply = (
            "It seems like there’s a lot of frustration inside you. "
            "Anger often comes from feeling unheard or hurt. "
            "What triggered this feeling?"
        )
        suggestion = "Try a short walk or deep breathing."
        video = "https://www.youtube.com/watch?v=BsVq5R_F6RA"

    else:
        reply = (
            "I’m here with you 💙. "
            "Sometimes it helps to talk things out. "
            "Can you tell me a bit more about what’s on your mind?"
        )
        suggestion = "Take a deep breath and continue sharing."
        video = "https://www.youtube.com/watch?v=inpok4MKVLM"

    return reply, suggestion, video