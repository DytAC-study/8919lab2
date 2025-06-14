from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logger to log to console (Azure will pick this up)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/')
def home():
    return "Welcome to the secure demo app."

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password123":
        app.logger.info(f"Successful login attempt by user: {username}")
        return jsonify({"message": "Login successful."}), 200
    else:
        app.logger.warning(f"Failed login attempt by user: {username}")
        return jsonify({"message": "Login failed."}), 401

if __name__ == '__main__':
    app.run()
