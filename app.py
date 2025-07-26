import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("prompt")
        if not user_input:
            return jsonify({"error": "Missing prompt"}), 400

        # Получаем API-ключи из переменных окружения
        openai_api_key = os.getenv("OPENAI_API_KEY")
        voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

        if not openai_api_key or not voice_id or not elevenlabs_api_key:
            return jsonify({"error": "Missing API keys"}), 500

        # Отправка запроса в OpenAI
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": user_input}]
            }
        )

        gpt_response = response.json()
        text = gpt_response["choices"][0]["message"]["content"]

        # Синтез речи через ElevenLabs
        voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": elevenlabs_api_key,
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
