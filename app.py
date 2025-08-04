from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import json
import re

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
            return jsonify({"actions": [{"type": "speak", "text": "Я вас не расслышал, пожалуйста, повторите"}]})

        prompt = f"""
        Ты — голосовой ассистент, который управляет компьютером. Твоя цель — понять команду пользователя и сгенерировать список действий в формате JSON.
        Ответ должен быть только в формате JSON, без лишнего текста.

        Пользователь сказал: "{user_text}"

        Контекст:
        - Активное окно: {window_info.get('active_window')}

        Действия, которые ты можешь использовать:
        1. speak: Озвучить текст. Пример: {{"type": "speak", "text": "Привет, чем могу помочь?"}}
        2. move_mouse: Переместить курсор мыши. Пример: {{"type": "move_mouse", "x": 500, "y": 300, "duration": 1.0}}
        3. click: Кликнуть левой кнопкой мыши. Пример: {{"type": "click"}}
        4. double_click: Сделать двойной клик. Пример: {{"type": "double_click"}}
        5. type_text: Ввести текст. Пример: {{"type": "type_text", "text": "Привет мир!", "interval": 0.1}}
        6. hotkey: Комбинация клавиш. Пример: {{"type": "hotkey", "keys": ["ctrl", "c"]}}
        7. open_app: Открыть программу. Пример: {{"type": "open_app", "name": "notepad"}}

        Верни только JSON, без форматирования Markdown.
        """

        response = model.generate_content(prompt)
        reply = response.text.strip()
        print(f"Ответ от Gemini: {reply}")

        # Удаляем обертку ```json ... ```
        if reply.startswith("```json"):
            reply = re.sub(r"^```json\s*|\s*```$", "", reply.strip(), flags=re.DOTALL)

        # Парсим JSON
        actions_data = json.loads(reply)
        return jsonify(actions_data)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Сервер голосового ассистента работает."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
