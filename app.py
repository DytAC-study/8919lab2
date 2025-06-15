from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# === Logging configuration ===
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# === Simulated user database ===
users = {
    "admin": "password123",
    "guest": "guestpass",
    "user1": "abc123"
}

# === Track failed login attempts by IP ===
ip_failed_counts = {}

@app.route('/')
def home():
    return "Welcome to the enhanced secure demo app."

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    ip = request.remote_addr or "unknown"
    ua = request.headers.get("User-Agent", "unknown")
    timestamp = datetime.utcnow().isoformat()

    # Check login
    if username in users and users[username] == password:
        app.logger.info(f"Login SUCCESS | user={username} | ip={ip} | ua=\"{ua}\" | time={timestamp}")
        return jsonify({"message": "Login successful"}), 200
    else:
        # Update failure count
        ip_failed_counts[ip] = ip_failed_counts.get(ip, 0) + 1
        fail_count = ip_failed_counts[ip]

        app.logger.warning(f"Login FAILED | user={username} | ip={ip} | ua=\"{ua}\" | fail_count={fail_count} | time={timestamp}")
        return jsonify({"message": "Login failed"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
