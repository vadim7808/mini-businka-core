import speech_recognition as sr
import requests

API_URL = "https://businka-brain.onrender.com/ask"  # Заменим позже на твой сервер

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говори...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="ru-RU")
        except sr.UnknownValueError:
            return "Не понял..."
        except sr.RequestError:
            return "Ошибка соединения."

def ask_brain(text):
    try:
        response = requests.post(API_URL, json={"question": text})
        return response.json().get("answer", "Нет ответа от мозга.")
    except Exception as e:
        return f"Ошибка: {e}"

if __name__ == "__main__":
    while True:
        query = recognize_voice()
        print("Ты сказал:", query)
        if "стоп" in query.lower():
            break
        answer = ask_brain(query)
        print("Бусинка:", answer)
