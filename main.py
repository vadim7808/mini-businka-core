import speech_recognition as sr
import requests
import pyttsx3  # встроенный синтез речи

API_URL = "https://businka-brain.onrender.com/ask"  # заменим позже

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(text)
    engine.runAndWait()

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
            speak("Хорошо, выхожу.")
            break
        answer = ask_brain(query)
        print("Бусинка:", answer)
        speak(answer)
