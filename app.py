import ssl
from flask import Flask, request, jsonify
import requests
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, VALID_PASSWORD

app = Flask(__name__)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    
    if not data or 'password' not in data or 'message' not in data:
        return jsonify({'error': 'Missing password or message'}), 400
    
    if data['password'] != VALID_PASSWORD:
        return jsonify({'error': 'Invalid password'}), 401
    
    # Send message to Telegram
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': data['message']
    }
    
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            return jsonify({'success': 'Message sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send message'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use the self-signed certificate you created
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/etc/ssl/certs/apache-selfsigned.crt', 
                           '/etc/ssl/private/apache-selfsigned.key')
    
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)