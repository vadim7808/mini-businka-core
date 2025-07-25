from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Замените своими ключами, если используете переменные среды
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

@app.route("/generate", methods=["POST"])
def generate_response():
    try:
        data = request.json
        response_text = data.get("text", "")

        # Запрос к ElevenLabs
        tts_response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": response_text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
        )

        if tts_response.status_code == 200:
            print("✅ Voice generated successfully.")
            return tts_response.content, 200, {'Content-Type': 'audio/mpeg'}
        else:
            print(f"❌ ElevenLabs error: {tts_response.status_code} {tts_response.text}")
            return jsonify({"error": "Voice synthesis failed"}), 500

    except Exception as e:
        print(f"❌ Speech synthesis error: {e}")
        return jsonify({"error": "Speech synthesis error"}), 500
