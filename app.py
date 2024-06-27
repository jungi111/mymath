from quart import Quart, request, jsonify
from quart_cors import cors
from main import MathProblemGenerator
import os
from dotenv import load_dotenv
from langchain_teddynote import logging

# .env 파일 로드 및 로깅 설정
load_dotenv()
logging.langsmith(os.getenv('LANGCHAIN_PROJECT'))

app = Quart(__name__)
cors(app)
generator = MathProblemGenerator()

@app.route("/", methods=["GET"])
async def home():
    return """
    <html>
        <head>
            <title>Math Problem Generator</title>
        </head>
        <body>
            <h1>Hello Math Study</h1>
            <p>Welcome to the Math Problem Generator API</p>
            <p>Usage:</p>
            <ul>
                <li>POST /generate_question: Generate a math problem with a given content</li>
            </ul>
            <p>Example content: 소인수분해</p>
        </body>
    </html>
    """

@app.route("/generate_question", methods=["POST"])
async def generate_question():
    if request.is_json:
        data = await request.get_json()
        content = data.get("content", "")
        if not content:
            return jsonify({"error": "Content is required"}), 400

        try:
            response = await generator.generate_question(content)
            return jsonify(response)
        except Exception as e:
            print(f"Error: {e}")  # 예외 디버그 로그 추가
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 415

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)
