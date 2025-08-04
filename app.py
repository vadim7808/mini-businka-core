from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import json

# Загрузка переменных окружения
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

        if not user_text:
            return jsonify({
                "actions": [
                    {"type": "speak", "text": "Я вас не расслышал, пожалуйста, повторите"}
                ]
            })

        prompt = f"""
        Ты — голосовой ассистент, управляющий компьютером. Пользователь сказал: "{user_text}".
        Контекст: активное окно — {window_info.get('active_window', 'неизвестно')}.

        Доступные действия:
        - speak: {{ "type": "speak", "text": "..." }}
        - move_mouse: {{ "type": "move_mouse", "x": ..., "y": ..., "duration": ... }}
        - click: {{ "type": "click" }}
        - double_click: {{ "type": "double_click" }}
        - type_text: {{ "type": "type_text", "text": "...", "interval": ... }}
        - hotkey: {{ "type": "hotkey", "keys": ["ctrl", "c"] }}
        - open_app: {{ "type": "open_app", "name": "notepad" }}

        Ответ должен быть в виде JSON:
        {{
            "actions": [
                {{ "type": "speak", "text": "..." }},
                ...
            ]
        }}

        Если ты не можешь выполнить команду, скажи об этом через speak.
        Ответ — только JSON, без текста вокруг.
        """

        # Получение ответа от Gemini
        response = model.generate_content(prompt)
        raw_reply = response.text if hasattr(response, "text") else "".join([p.text for p in response.parts])
        print(f"Ответ от Gemini: {raw_reply}")

        try:
            actions_data = json.loads(raw_reply)
            return jsonify(actions_data)
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return jsonify({"error": "Ошибка при разборе JSON", "raw_response": raw_reply}), 500

    except Exception as e:
        print(f"Внутренняя ошибка сервера: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Сервер голосового ассистента работает."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
