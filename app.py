# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
from flask_cors import CORS

# Загрузка переменных окружения из файла .env
load_dotenv()

# Инициализация Flask и CORS
app = Flask(__name__)
CORS(app)  # Разрешает твоему локальному клиенту подключаться к серверу

# Настройка Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Переменная окружения GEMINI_API_KEY не установлена в файле .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    """Простой маршрут для проверки работы сервера."""
    return "Сервер голосового ассистента на базе Gemini работает."

@app.route("/process", methods=["POST"])
def process():
    """Основная точка входа для получения команд и генерации действий."""
    try:
        data = request.get_json()
        user_text = data.get("text", "")
        window_info = data.get("window_info", {})

        if not user_text:
            return jsonify({"error": "Нет текста от пользователя"}), 400

        # Составление промта для Gemini с командой пользователя и контекстом системы
        prompt = f"""
        Ты — голосовой ассистент, управляющий компьютером. Твоя задача — анализировать команды пользователя,
        учитывать контекст открытых окон и формировать список действий для выполнения на ПК.
        Твой ответ должен быть строго в формате JSON, содержащий список объектов с действиями.

        Доступные типы действий:
        - "speak": {{"type": "speak", "text": "Текст для озвучивания"}}
        - "move_mouse": {{"type": "move_mouse", "x": 100, "y": 200, "duration": 0.5}}
        - "click": {{"type": "click"}}
        - "double_click": {{"type": "double_click"}}
        - "type_text": {{"type": "type_text", "text": "Текст для ввода"}}
        - "hotkey": {{"type": "hotkey", "keys": ["ctrl", "c"]}}
        - "open_app": {{"type": "open_app", "name": "chrome"}}
        - "delay": {{"type": "delay", "delay": 1.5}}

        Текущий контекст:
        - Активное окно: {window_info.get('active_window')}
        - Все открытые окна: {', '.join(window_info.get('all_windows', []))}

        Команда пользователя: "{user_text}"

        Примеры ответов:
        1. Если пользователь говорит "Открой браузер":
        {{
            "actions": [
                {{"type": "speak", "text": "Открываю браузер."}},
                {{"type": "open_app", "name": "chrome"}}
            ]
        }}
        2. Если пользователь говорит "Привет":
        {{
            "actions": [
                {{"type": "speak", "text": "Здравствуйте, чем могу помочь?"}}
            ]
        }}

        Пожалуйста, сформируй список действий для выполнения, основываясь на команде пользователя и контексте.
        Отвечай только JSON-объектом, без лишнего текста.
        """
        
        response = model.generate_content(prompt)
        reply = response.text.strip()
        
        try:
            # Попытка разобрать JSON-ответ от Gemini
            actions_json = json.loads(reply)
            return jsonify(actions_json)
        except json.JSONDecodeError:
            # Если Gemini ответил не валидным JSON, мы обрабатываем это как обычный текст
            return jsonify({
                "actions": [
                    {"type": "speak", "text": reply}
                ]
            })

    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return jsonify({"actions": [{"type": "speak", "text": "Извините, произошла ошибка."}]}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
