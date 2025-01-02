from flask import Flask, request, jsonify
from database import Database
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла (если он есть)
load_dotenv()

app = Flask(__name__)
db = Database()

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

@app.route('/submitData', methods=['POST'])
def submit_data():
    """Обработка POST запроса для добавления перевала."""
    data = request.json

    # Проверка наличия необходимых полей в запросе
    if not all(key in data for key in ('date_added', 'raw_data', 'images')):
        return jsonify({"error": "Missing required fields"}), 400

    date_added = data['date_added']
    raw_data = data['raw_data']
    images = data['images']

    try:
        new_id = db.submit_data(date_added, raw_data, images)
        return jsonify({"message": "Data submitted successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)