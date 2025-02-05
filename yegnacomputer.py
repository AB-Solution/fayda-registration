import os
from pyngrok import ngrok
import requests

# Telegram Bot Token
API_TOKEN = os.getenv('7625727167:AAG1bDkcgBPjNsfqdSMTiFLWePawxjGFNlw')

# Start the ngrok tunnel
def start_ngrok():
    public_url = ngrok.connect(8080, bind_tls=True)
    print(f"ngrok tunnel started at: {public_url}")
    return public_url

# Set the Telegram webhook
def set_webhook(public_url):
    webhook_url = f"{public_url}/{API_TOKEN}"
    response = requests.post(
        f"https://api.telegram.org/bot{API_TOKEN}/setWebhook",
        json={"url": webhook_url}
    )
    if response.status_code == 200:
        print(f"Webhook successfully set: {webhook_url}")
    else:
        print(f"Failed to set webhook: {response.text}")

if __name__ == "__main__":
    # Start ngrok and set webhook
    public_url = start_ngrok()
    set_webhook(public_url)

    # Start the bot
    os.system("python yegnacomputerbot.py")