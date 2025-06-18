class Config:
    TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    PASSWORD = 'YOUR_SECRET_PASSWORD'
    API_URL = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_BOT_TOKEN)
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000