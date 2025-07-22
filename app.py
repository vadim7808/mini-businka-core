from flask import Flask, request, jsonify
import pyttsx3

app = Flask(__name__)
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # скорость голоса
engine.setProperty('voice', 'ru')  # русский голос

def generate_response(user_message):
    response = f"Привет, Вадим! Ты сказал: {user_message}"
    engine.say(response)
    engine.runAndWait()
    return response

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
