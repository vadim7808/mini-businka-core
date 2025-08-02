import asyncio
import json
from io import BytesIO

import websockets
from gtts import gTTS
from pydub import AudioSegment

# === Настройки ===
HOST = "0.0.0.0"
PORT = 8765


async def process_command(message):
    """Обрабатывает текст команды и возвращает ответ и действие."""
    text = message.get("text", "").lower()

    if "открой браузер" in text:
        return "Открываю браузер", {"action": "open_app", "name": "Chrome"}
    elif "привет" in text:
        return "Привет! Чем могу помочь?", None
    elif "как дела" in text:
        return "У меня всё отлично. Спасибо, что спросил!", None
    else:
        return "Я не совсем понял. Повтори, пожалуйста.", None


async def handler(websocket, path):
    print(f"[+] Клиент подключён: {websocket.remote_address}", flush=True)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"[>] Получено: {data}", flush=True)

            reply_text, command = await process_command(data)

            # Синтез речи
            tts = gTTS(reply_text, lang="ru")
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            audio = AudioSegment.from_file(audio_fp, format="mp3")

            # WAV для клиента
            wav_fp = BytesIO()
            audio.export(wav_fp, format="wav")
            wav_fp.seek(0)
            wav_bytes = wav_fp.read()

            await websocket.send(
                json.dumps(
                    {
                        "type": "audio",
                        "audio": list(wav_bytes),  # массив байт
                        "text": reply_text,
                        "command": command,
                    }
                )
            )
            print(f"[<] Ответ: {reply_text}", flush=True)

    except websockets.exceptions.ConnectionClosed:
        print("[-] Клиент отключён", flush=True)


async def main():
    # 💡 маячок для Render-логов
    print("🧠 WebSocket server started 🎉", flush=True)

    async with websockets.serve(handler, HOST, PORT):
        print(f"Сервер запущен на {HOST}:{PORT}", flush=True)
        await asyncio.Future()  # держим процесс бесконечно


if __name__ == "__main__":
    asyncio.run(main())


