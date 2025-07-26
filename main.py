import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")

def speak(text):
    voice_id = "EXAVITQu4vr4xnSDxMaL"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Голос создан. Сохранили как output.mp3")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    speak("Привет, Вадим! Я — голос твоей Бусинки.")
