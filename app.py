import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "dev")
GIT_COMMIT = os.getenv("GIT_COMMIT", "local")

@app.route('/', methods=['GET'])
def home():
    return "Payment API v2", 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="UP"), 200

@app.route('/version', methods=['GET'])
def version():
    return jsonify({
        "version": APP_VERSION,
        "build": BUILD_NUMBER,
        "commit": GIT_COMMIT
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)