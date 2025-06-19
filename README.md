# Flask Telegram Bot

This project is a Flask application that serves as a server with HTTPS on AWS EC2, capable of sending notifications to a Telegram bot. Below are the steps to set up and run the application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Usage](#usage)
4. [License](#license)

## Prerequisites

- An AWS account to create an EC2 instance.
- Basic knowledge of Flask and Python.
- A Telegram account to create a bot.

## Setup Instructions

### 1. Create an EC2 Instance

- Launch an EC2 instance using Amazon Linux 2.
- Configure the security group to allow traffic on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).

### 2. Install Dependencies

- SSH into your EC2 instance.
- Install Apache and SSL modules:
  ```bash
  sudo yum install httpd mod_ssl
  ```
- Start the Apache service:
  ```bash
  sudo systemctl start httpd
  ```

### 3. Configure SSL with Self-Signed Certificate

- Create SSL certificate directory:
  ```bash
  sudo mkdir -p /etc/ssl/private
  sudo mkdir -p /etc/ssl/certs
  sudo amazon-linux-extras install epel -y

  ```

- Generate private key:
  ```bash
  sudo openssl genrsa -out /etc/ssl/private/apache-selfsigned.key 2048
  ```

- Generate self-signed certificate:
  ```bash
  sudo openssl req -new -x509 -key /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt -days 365
  ```
  **Important:** For "Common Name", use your EC2 public IP address.

- Configure Apache SSL:
  ```bash
  sudo nano /etc/httpd/conf.d/ssl.conf
  ```
  
  Update the following lines:
  ```
  SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
  SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
  ```

- Restart Apache:
  ```bash
  sudo systemctl restart httpd
  ```

**Note:** Self-signed certificates will show a security warning in browsers. This is normal for development/testing purposes.

### 4. Clone the Repository

- Clone this repository to your EC2 instance:
  ```bash
  sudo yum install git -y
  git clone <repository-url>
  cd InfoWizBot2
  ```

### 5. Install Python Dependencies

- Install the required Python packages:
  ```bash
  sudo yum install python3 -y
  sudo yum install python3-pip -y
  
  # Install compatible versions for Amazon Linux 2
  sudo pip3 install 'urllib3<2.0' 'requests<3.0' flask
  
  # Or install from requirements.txt
  pip3 install -r requirements.txt
  ```

### 6. Configure the Bot

- Create a new bot using BotFather on Telegram:
  1. Open Telegram and search for @BotFather
  2. Send `/newbot` command
  3. Follow instructions to create your bot
  4. Copy the bot token

- Get your Chat ID:
  1. Delete any existing webhook: `https://api.telegram.org/bot<YOUR_TOKEN>/deleteWebhook`
  2. Send a message to your bot
  3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
  4. Find your chat ID in the response

- Update `config.py` with your configurations

### 7. Run the Application

- Start the Flask application:
  ```bash
  # Install cryptography for SSL support
  pip3 install --user cryptography
  
  # Run with sudo for SSL certificate access
  sudo python3 app.py
  ```

## Usage

- Send a POST request to the Flask endpoint with a JSON payload containing the password and message. The bot will send the message to the specified chat.

Example payload:
```json
{
  "password": "your_password",
  "message": "Hello, Telegram!"
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.


📋 Cara Penggunaan Base64:
1. Kirim Text Message (seperti biasa):
    curl -k -X POST https://13.250.9.71:443/send_notification \
    -H "Content-Type: application/json" \
    -d '{"password": "Kribo", "message": "Hello World!"}'

2. Kirim Photo Base64:
    curl -k -X POST https://13.250.9.71:443/send_notification \
      -H "Content-Type: application/json" \
      -d '{
        "password": "Kribo",
        "file_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDAREAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAI",
        "file_type": "photo",
        "caption": "This is a Base64 photo!",
        "filename": "photo.jpg"
      }'

3. Kirim Video Base64:
    curl -k -X POST https://13.250.9.71:443/send_notification \
      -H "Content-Type: application/json" \
      -d '{
        "password": "Kribo",
        "file_base64": "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAACKBtZGF0AAAC...",
        "file_type": "video",
        "caption": "Video from Base64",
        "filename": "video.mp4"
      }'

4. Kirim Document Base64:
    curl -k -X POST https://13.250.9.71:443/send_notification \
      -H "Content-Type: application/json" \
      -d '{
        "password": "Kribo",
        "file_base64": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovT3V0bGluZXMgMiAwIFIKL1BhZ2VzIDMgMCBSCj4+CmVuZG9iag==",
        "file_type": "document",
        "caption": "PDF Document",
        "filename": "document.pdf"
      }'

5. Kirim Photo dari URL:
    curl -k -X POST https://13.250.9.71:443/send_notification \
      -H "Content-Type: application/json" \
      -d '{
        "password": "Kribo",
        "photo_url": "https://picsum.photos/800/600",
        "caption": "Random photo from URL"
      }'
