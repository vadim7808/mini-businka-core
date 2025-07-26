from flask import Flask, request, jsonify, Response
import openai
import requests
import os

app = Flask(__name__)

# Конфигурация
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your-elevenlabs-key")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "your-voice-id")

openai.api_key = OPENAI_API_KEY

@app.route("/")
def index():
    return "Hello from Businka!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        text = gpt_response.choices[0].message["content"]

        # ElevenLabs TTS
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
            return jsonify({"error": "TTS failed", "details": tts_response.text}), 500

        audio_data = tts_response.content
        return Response(audio_data, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
