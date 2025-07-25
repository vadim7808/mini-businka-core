from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# API keys
OPENAI_API_KEY = "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"
ELEVENLABS_API_KEY = "sk-4598e41d59610afdd7b54122344da6b11d280a981b7076"
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel

openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return "Hello, Vadim! Businka is running with GPT-4 💡"

@app.route("/vadim", methods=["POST"])
def generate_response():
    user_message = request.json.get("message")
    print(f"📥 Received message: {user_message}")

    try:
        # Send message to GPT-4
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200,
            temperature=0.7
        )
        response_text = gpt_response["choices"][0]["message"]["content"].strip()
        print(f"🤖 GPT-4 replied: {response_text}")
    except Exception as e:
        response_text = "Sorry, I couldn't get a response from GPT-4."
        print(f"❌ GPT-4 error: {e}")

    try:
        # Send text to ElevenLabs for speech
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
            print("🔊 Voice generated successfully.")
            return tts_response.content, 200, {'Content-Type': 'audio/mpeg'}
        else:
            print(f"❌ ElevenLabs error: {tts_response.status_code} {tts_response.text}")
            return jsonify({"error": "Voice synthesis failed"}), 500
    except Exception as e:
        print(f"❌ Speech synthesis error: {e}")
        return jsonify({"error": "Speech synthesis error"}), 500

if __name__ == "__main__":
    
import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
