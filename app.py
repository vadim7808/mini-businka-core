from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_response(user_message):
    return f"Привет, Вадим! Ты сказал: {user_message}"

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
