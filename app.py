from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json()
        user_text = data.get("text", "")
        window_info = data.get("window_info", {})

        # Убедимся, что window_info — это словарь
        if not isinstance(window_info, dict):
            window_info = {}

        if not user_text:
            return jsonify({"actions": [{"type": "speak", "text": "Я вас не расслышал, пожалуйста, повторите"}]})

        prompt = f"""
        Ты — голосовой ассистент, управляющий компьютером. Понимай команду пользователя и возвращай действия в формате JSON.

        Пользователь сказал: "{user_text}"

        Контекст:
        - Активное окно: {window_info.get('active_window', '')}

        Поддерживаемые действия:
        1. speak — Пример: {{"type": "speak", "text": "Привет!"}}
        2. move_mouse — Пример: {{"type": "move_mouse", "x": 500, "y": 300, "duration": 1.0}}
        3. click — Пример: {{"type": "click"}}
        4. double_click — Пример: {{"type": "double_click"}}
        5. type_text — Пример: {{"type": "type_text", "text": "Привет", "interval": 0.1}}
        6. hotkey — Пример: {{"type": "hotkey", "keys": ["ctrl", "c"]}}
        7. open_app — Пример: {{"type": "open_app", "name": "notepad"}}

        Возвращай только JSON, например:
        {{
            "actions": [
                {{"type": "speak", "text": "Команда выполнена."}},
                {{"type": "open_app", "name": "notepad"}}
            ]
        }}
        """

        response = model.generate_content(prompt)
        reply = response.text.strip()

        print(f"Ответ от Gemini: {reply}")

        try:
            actions_data = json.loads(reply)
            return jsonify(actions_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Неверный формат JSON от Gemini", "raw_response": reply}), 500

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Сервер голосового ассистента работает."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
