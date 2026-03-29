from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = "psysense_secret_key"

# ================= DATABASE ================= #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
DB_PATH = os.path.join(DB_DIR, "psysense.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    
    # Chat logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_reply TEXT,
        emotion TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully at", DB_PATH)

init_db()

# ================= EMOTION DETECTION & REPLIES ================= #
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in [
        "sad", "depressed", "cry", "crying", "hopeless", "lonely", "low"
    ]):
        return "sad"

    if any(word in text for word in [
        "stress", "stressed", "pressure", "exam", "career", "future", "tension"
    ]):
        return "stress"

    if any(word in text for word in [
        "angry", "anger", "irritated", "frustrated", "mad", "annoyed"
    ]):
        return "anger"

    if any(word in text for word in [
        "happy", "good", "fine", "great", "excited", "relaxed"
    ]):
        return "happy"

    return "neutral"
def generate_therapist_reply(user_text):
    emotion = detect_emotion(user_text)

    # Conversation stages
    empathy = {
        "sad": [
            "I’m really sorry you’re feeling this way.",
            "That sounds emotionally heavy.",
            "I can sense how low this feels right now."
        ],
        "stress": [
            "It sounds like a lot is happening at once.",
            "That kind of pressure can feel overwhelming.",
            "You’re carrying a lot on your mind."
        ],
        "anger": [
            "That frustration feels intense.",
            "I can hear the anger in what you’re saying.",
            "Something clearly didn’t feel fair."
        ],
        "happy": [
            "That’s really nice to hear.",
            "I’m glad something positive happened.",
            "That sounds uplifting."
        ],
        "neutral": [
            "Thanks for sharing that.",
            "I’m listening carefully.",
            "Go on, I’m here."
        ]
    }

    reflection = {
        "sad": [
            "Sometimes sadness comes after setbacks or disappointments.",
            "Feeling this way doesn’t mean you’re weak.",
            "Emotions like this often build up silently."
        ],
        "stress": [
            "Stress often comes from caring deeply about outcomes.",
            "When many thoughts overlap, it becomes exhausting.",
            "Pressure can cloud even simple decisions."
        ],
        "anger": [
            "Anger usually protects something important inside us.",
            "Strong reactions often follow unmet expectations.",
            "It’s okay to feel this — understanding it matters."
        ],
        "happy": [
            "Moments like these are important to notice.",
            "Positive emotions help balance difficult days.",
            "It’s good to pause and acknowledge this."
        ],
        "neutral": [
            "Sometimes emotions are mixed or unclear.",
            "Not everything needs a label immediately.",
            "You don’t need to rush your thoughts."
        ]
    }

    follow_up = {
        "sad": [
            "Do you want to tell me what affected you the most?",
            "What happened just before you started feeling this way?",
            "Would talking about it help right now?"
        ],
        "stress": [
            "What’s the biggest thing worrying you right now?",
            "Is this related to studies, future, or something personal?",
            "What feels most urgent at the moment?"
        ],
        "anger": [
            "What triggered this feeling?",
            "Did something specific happen today?",
            "What part of this situation feels most unfair?"
        ],
        "happy": [
            "What made you feel this way today?",
            "Would you like to share what went well?",
            "How long have you been feeling this positive?"
        ],
        "neutral": [
            "What’s been on your mind lately?",
            "Would you like to talk more about it?",
            "What made you reach out today?"
        ]
    }

    YOUTUBE = {
        "sad": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
        "stress": "https://www.youtube.com/watch?v=inpok4MKVLM",
        "anger": "https://www.youtube.com/watch?v=ZToicYcHIOU",
        "happy": "https://www.youtube.com/watch?v=ZXsQAXx_ao0",
        "neutral": "https://www.youtube.com/watch?v=ZToicYcHIOU"
    }

    reply = (
        random.choice(empathy[emotion]) + " "
        + random.choice(reflection[emotion]) + "<br><br>"
        + random.choice(follow_up[emotion])
        + "<br><br><b>Support resource:</b><br>"
        f"<a href='{YOUTUBE[emotion]}' target='_blank'>Watch a helpful video</a>"
    )

    return reply, emotion

# ================= ROUTES ================= #

# ---------- LANDING PAGE ----------
@app.route("/")
def landing():
    return render_template("landing.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already exists")
    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        # Demo login – no DB authentication
        session["user_id"] = 1
        session["username"] = username

        return redirect(url_for("dashboard"))

    return render_template("login.html")
# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["username"])

# ---------- CHAT PAGE ----------
@app.route("/chat", methods=["GET"])
def chat_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html")


# ---------- CHAT API ----------
@app.route("/chat/send", methods=["POST"])
def chat_send():
    if "user_id" not in session:
        return jsonify({"reply": "Session expired. Please login again.", "emotion": "neutral"})

    data = request.get_json(force=True)
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type something.", "emotion": "neutral"})

    reply, emotion = generate_therapist_reply(user_msg)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_logs (user_id, user_message, bot_reply, emotion, created_at) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], user_msg, reply, emotion, datetime.now())
    )
    conn.commit()
    conn.close()

    return jsonify({"reply": reply, "emotion": emotion})
@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    # Emotion distribution for chart
    cur.execute("""
        SELECT emotion, COUNT(*) as count
        FROM chat_logs
        WHERE user_id = ?
        GROUP BY emotion
    """, (session["user_id"],))
    emotion_data = cur.fetchall()

    # Total sessions
    cur.execute("""
        SELECT COUNT(*) FROM chat_logs
        WHERE user_id = ?
    """, (session["user_id"],))
    total_sessions = cur.fetchone()[0]

    # Dominant emotion
    dominant_emotion = "N/A"
    if emotion_data:
        dominant_emotion = max(emotion_data, key=lambda x: x["count"])["emotion"]

    conn.close()

    return render_template(
        "analytics.html",
        emotion_data=emotion_data,
        total_sessions=total_sessions,
        dominant_emotion=dominant_emotion
    )

# ---------- HISTORY ----------
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_message, bot_reply, emotion, created_at
        FROM chat_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],))
    
    sessions = cur.fetchall()
    conn.close()

    return render_template("history.html", sessions=sessions)
# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_info = {
        "name": session["username"],
        "role": "Personal User",
        "project": "PsySense AI – Mental Health Assistant"
    }
    return render_template("profile.html", user=user_info)

# ---------- SUPPORT ----------
@app.route("/support")
def support():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("support.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

# ================= RUN APP ================= #
if __name__ == "__main__":
    app.run(debug=True)