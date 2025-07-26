import os
from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

# Получение API-ключей из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def index():
    return "🟢 Businka Voice API is running."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("question", "")
        if not user_input:
            return jsonify({"error": "Missing question"}), 400

        # Получение ответа от ChatGPT
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты голосовой ассистент по имени Бусинка."},
                {"role": "user", "content": user_input}
            ]
        )
        text = gpt_response.choices[0].message["content"]

        # Синтез речи через ElevenLabs
        voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.7
            }
        }
        tts_response = requests.post(voice_url, headers=headers, json=payload)

        if tts_response.status_code != 200:
            return jsonify({"error": "Failed to generate voice", "details": tts_response.text}), 500

        audio_data = tts_response.content
        return audio_data, 200, {
            "Content-Type": "audio/mpeg"
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
Update app.py for Businka
