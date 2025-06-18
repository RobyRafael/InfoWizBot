from flask import Flask, request, jsonify
import requests
import json
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, VALID_PASSWORD

app = Flask(__name__)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()

    if not data or 'password' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    password = data['password']
    message = data['message']

    if password != VALID_PASSWORD:
        return jsonify({'error': 'Unauthorized'}), 403

    send_telegram_message(message)
    return jsonify({'status': 'Message sent'}), 200

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5000)