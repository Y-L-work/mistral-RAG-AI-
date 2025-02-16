from flask import Flask, request, jsonify
from src.chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "請求中缺少 'query' 參數"}), 400
    query_text = data["query"]
    try:
        answer = chatbot.process_query(query_text)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
