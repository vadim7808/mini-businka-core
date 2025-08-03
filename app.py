from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    user_text = data.get("text", "")
    window_info = data.get("window_info", {})

    prompt = f"""
Ты — голосовой ассистент. Пользователь сказал: "{user_text}".
Контекст окон: {window_info}

Ответь:
1. Что озвучить (ключ 'speak').
2. Какие действия выполнить (список в ключе 'actions').
Если не знаешь — просто поприветствуй.
"""

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()

        return jsonify({
            "actions": [
                {"type": "speak", "text": reply}
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "💡 Сервер голосового ассистента работает."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
