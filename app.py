from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensures uploads/ is created

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TELEGRAM_BOT_TOKEN = os.getenv("7625727167:AAG1bDkcgBPjNsfqdSMTiFLWePawxjGFNlw")  # Store in environment variable
ADMIN_CHAT_ID = os.getenv("364010528")  # Store your Telegram chat ID securely

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form.get('name')
    id_number = request.form.get('id_number')
    file = request.files.get('pdf')

    if not full_name or not id_number or not file:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    # Save file
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Send message to Telegram
    message = f"New Registration:\n\nName: {full_name}\nID Number: {id_number}"
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                  json={"chat_id": ADMIN_CHAT_ID, "text": message})

    # Send document to Telegram
    with open(filename, "rb") as pdf:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
                      files={"document": pdf}, data={"chat_id": ADMIN_CHAT_ID})

    return jsonify({'status': 'success', 'message': 'Data sent to Telegram'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

