from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='face_auth'
)
cursor = conn.cursor()


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    user = data.get("user")

    cursor.execute("SELECT * FROM users WHERE name = %s", (user,))
    result = cursor.fetchone()

    if result:
        return jsonify({"status": "success", "message": "Access Granted", "user": user}), 200
    else:
        return jsonify({"status": "failure", "message": "Access Denied"}), 401


@app.route('/control_motor', methods=['POST'])
def control_motor():
    data = request.json
    command = data.get("command")

    if command == "start":
        # Send command to ESP8266
        return jsonify({"status": "success", "message": "Motor started"}), 200
    elif command == "stop":
        return jsonify({"status": "success", "message": "Motor stopped"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid command"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
