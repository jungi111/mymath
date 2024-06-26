# app.py
from flask import Flask, request, jsonify
from main import MathProblemGenerator

app = Flask(__name__)
generator = MathProblemGenerator()

@app.route("/generate_question", methods=["POST"])
def generate_question():
    if request.is_json:
        data = request.get_json()
        content = data.get("content", "")
        if not content:
            return jsonify({"error": "Content is required"}), 400

        try:
            response = generator.generate_question(content)
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 415

if __name__ == "__main__":
    app.run(debug=False)
