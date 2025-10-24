from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

@app.route("/")
def hello():
    return jsonify( "Hello from Python Backend!")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

