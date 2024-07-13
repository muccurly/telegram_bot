import requests

TELEGRAM_TOKEN = '7446262616:AAEUrocdS7wrmw4HYXoTaDyBr4DZ4-_ZuhM'
WEBHOOK_URL = 'https://your-vercel-app-url.vercel.app/webhook'

response = requests.post(
    f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook',
    json={'url': WEBHOOK_URL}
)

print(response.json())
