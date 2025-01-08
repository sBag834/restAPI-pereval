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

@app.route('/submitData/<int:id>', methods=['GET'])
def get_data(id):
    """Получение записи по ID."""
    try:
        record = db.get_record_by_id(id)
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submitData/<int:id>', methods=['PATCH'])
def patch_data(id):
    """Редактирование записи по ID."""
    data = request.json

    # Проверка наличия необходимых полей в запросе
    if not any(key in data for key in ('date_added', 'raw_data', 'images')):
        return jsonify({"state": 0, "message": "No fields to update."}), 400

    try:
        updated = db.update_record(id, data)
        if updated:
            return jsonify({"state": 1, "message": "Record updated successfully."}), 200
        else:
            return jsonify({"state": 0, "message": "Record not found or status is not 'new'."}), 400
    except Exception as e:
        return jsonify({"state": 0, "message": str(e)}), 500


@app.route('/submitData/', methods=['GET'])
def get_records_by_email():
    """Получение всех записей пользователя по email."""
    email = request.args.get('user__email')

    if not email:
        return jsonify({"error": "Email parameter is required."}), 400

    try:
        records = db.get_records_by_email(email)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)