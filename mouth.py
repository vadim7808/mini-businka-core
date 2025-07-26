import requests
import os
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def speak(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        with open("voice_output.mp3", "wb") as f:
            f.write(response.content)
        os.system("start voice_output.mp3")
    else:
        print("Ошибка озвучки:", response.text)

# Тест
if __name__ == "__main__":
    speak("Привет, Вадим! Я Бусинка, твой голосовой ассистент.")
