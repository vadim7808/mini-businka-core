from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if "hello" in question.lower() or "привет" in question.lower():
        answer = "Hello, Vadim! I am online and ready."
    else:
        answer = "I am still learning, but I will get smarter soon."

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
