from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ELEVENLABS_API_KEY = "sk_4598e41d5961a0afdd7b54122344da6cb11d280a981b7076"
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Стандартный женский голос (Rachel)

def generate_response(user_message):
    response_text = f"Привет, Вадим! Ты сказал: {user_message}"
    
    # Отправляем текст в ElevenLabs для озвучки
    tts_response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "text": response_text,
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.8
            }
        }
    )
    
    if tts_response.status_code == 200:
        with open("response.mp3", "wb") as f:
            f.write(tts_response.content)
        # Проигрываем голосовой ответ
        import playsound
        playsound.playsound("response.mp3")
    else:
        print("Ошибка синтеза речи:", tts_response.status_code, tts_response.text)
    
    return response_text

@app.route("/")
def index():
    return "Привет, Вадим! Бусинка работает 💕"

@app.route("/vadim", methods=["POST"])
def vadim():
    data = request.get_json(force=True)
    if not data or "message" not in data:
        return jsonify({"error": "Нет сообщения"}), 400
    
    user_message = data["message"]
    response_text = generate_response(user_message)
    return jsonify({"response": response_text}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
