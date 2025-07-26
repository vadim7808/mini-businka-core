from flask import Flask, render_template_string, request, jsonify
import pyttsx3
import io
from flask import send_file

app = Flask(__name__)
engine = pyttsx3.init()

html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Businka Voice</title>
</head>
<body>
    <h1>🎤 Бусинка слушает...</h1>
    <button onclick="startRecording()">Говорить</button>
    <p id="result"></p>

    <script>
        function startRecording() {
            const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = 'ru-RU';
            recognition.start();

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                document.getElementById('result').innerText = 'Вы сказали: ' + text;

                fetch('/speak', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                }).then(resp => resp.blob())
                  .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const audio = new Audio(url);
                    audio.play();
                });
            };
        }
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return "Hello from Businka!"

@app.route("/businka", methods=["GET"])
def businka_page():
    return render_template_string(html)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    response_text = f"Привет, Вадим! Ты сказал: {text}"

    # Говорим напрямую, без сохранения
    audio_stream = io.BytesIO()
    engine.save_to_file(response_text, audio_stream)
    engine.runAndWait()
    audio_stream.seek(0)

    return send_file(audio_stream, mimetype="audio/mp3")

if __name__ == "__main__":
    app.run(debug=True)
