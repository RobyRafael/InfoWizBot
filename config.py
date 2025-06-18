class Config:
    TELEGRAM_BOT_TOKEN = '7384156638:AAE_oFaxF6S-eta7wjFchMnyprad3Lq_FOs'
    CHAT_ID = '-4954140947'  # Your group chat ID from the response
    PASSWORD = 'Kribo'  # Change this to your secure password
    API_URL = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_BOT_TOKEN)
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

# For backward compatibility, also create module-level variables
TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
CHAT_ID = Config.CHAT_ID
VALID_PASSWORD = Config.PASSWORD