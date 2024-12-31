from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allows CORS from any origin

# Replace this with the URL you want to forward requests to
TARGET_URL = "https://yartalepbdghsq4auluoj5vc2y0efmgk.lambda-url.us-east-1.on.aws/"

@app.route("/proxy", methods=["POST"])
def proxy():
    # Get the body of the incoming request
    data = request.get_json()
    # Forward only the body content to the target URL
    print(data)
    response = requests.post(TARGET_URL, json=data)
    # Return only the body content from the target URL's response
    print(response.text)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000, debug=True)
