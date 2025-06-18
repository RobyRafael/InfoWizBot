import ssl
import os
import tempfile
import base64
from flask import Flask, request, jsonify
import requests
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, VALID_PASSWORD

app = Flask(__name__)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    
    if not data or 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    
    if data['password'] != VALID_PASSWORD:
        return jsonify({'error': 'Invalid password'}), 401
    
    # Handle different message types
    if 'message' in data:
        return send_text_message(data['message'])
    elif 'photo_url' in data:
        return send_photo_url(data['photo_url'], data.get('caption', ''))
    elif 'video_url' in data:
        return send_video_url(data['video_url'], data.get('caption', ''))
    elif 'file_base64' in data:
        return send_file_base64(data)
    else:
        return jsonify({'error': 'Missing message, photo_url, video_url, or file_base64'}), 400

def send_text_message(message):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            return jsonify({'success': 'Message sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send message'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_photo_url(photo_url, caption=''):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    payload = {'chat_id': CHAT_ID, 'photo': photo_url, 'caption': caption}
    return make_telegram_request(telegram_url, payload)

def send_video_url(video_url, caption=''):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo'
    payload = {'chat_id': CHAT_ID, 'video': video_url, 'caption': caption}
    return make_telegram_request(telegram_url, payload)

def send_file_base64(data):
    """
    Handle Base64 encoded files
    Expected JSON format:
    {
        "password": "Kribo",
        "file_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
        "file_type": "photo|video|document",
        "caption": "Optional caption",
        "filename": "optional_filename.jpg"
    }
    """
    try:
        # Validate required fields
        if 'file_base64' not in data:
            return jsonify({'error': 'Missing file_base64'}), 400
        
        # Decode Base64 data
        file_data = base64.b64decode(data['file_base64'])
        file_type = data.get('file_type', 'document').lower()
        caption = data.get('caption', '')
        filename = data.get('filename', f'file.{get_extension_by_type(file_type)}')
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{get_extension_by_type(file_type)}') as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name
        
        try:
            # Send based on file type
            if file_type == 'photo':
                result = send_photo_file(temp_file_path, caption)
            elif file_type == 'video':
                result = send_video_file(temp_file_path, caption)
            else:
                result = send_document_file(temp_file_path, caption, filename)
            
            return result
        finally:
            # Cleanup temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except base64.binascii.Error:
        return jsonify({'error': 'Invalid base64 data'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to process base64 file: {str(e)}'}), 500

def get_extension_by_type(file_type):
    """Get file extension by type"""
    extensions = {
        'photo': 'jpg',
        'video': 'mp4',
        'document': 'pdf'
    }
    return extensions.get(file_type, 'bin')

def send_photo_file(file_path, caption=''):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    
    try:
        with open(file_path, 'rb') as photo_file:
            files = {'photo': photo_file}
            data_payload = {'chat_id': CHAT_ID, 'caption': caption}
            
            response = requests.post(telegram_url, files=files, data=data_payload)
            
            if response.status_code == 200:
                return jsonify({'success': 'Photo sent successfully'}), 200
            else:
                return jsonify({'error': f'Failed to send photo: {response.text}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error sending photo: {str(e)}'}), 500

def send_video_file(file_path, caption=''):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo'
    
    try:
        with open(file_path, 'rb') as video_file:
            files = {'video': video_file}
            data_payload = {'chat_id': CHAT_ID, 'caption': caption}
            
            response = requests.post(telegram_url, files=files, data=data_payload)
            
            if response.status_code == 200:
                return jsonify({'success': 'Video sent successfully'}), 200
            else:
                return jsonify({'error': f'Failed to send video: {response.text}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error sending video: {str(e)}'}), 500

def send_document_file(file_path, caption='', filename='document'):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'
    
    try:
        with open(file_path, 'rb') as doc_file:
            files = {'document': (filename, doc_file)}
            data_payload = {'chat_id': CHAT_ID, 'caption': caption}
            
            response = requests.post(telegram_url, files=files, data=data_payload)
            
            if response.status_code == 200:
                return jsonify({'success': 'Document sent successfully'}), 200
            else:
                return jsonify({'error': f'Failed to send document: {response.text}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error sending document: {str(e)}'}), 500

def make_telegram_request(url, payload):
    try:
        response = requests.post(url, json=payload)
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
    
    # Use port 443 instead of 5000
    app.run(host='0.0.0.0', port=443, ssl_context=context, debug=True)