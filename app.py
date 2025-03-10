from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, User, Reminder
from config import Config
from scheduler import init_scheduler
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

# Inicializácia databázy a migrácií
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return "Vitaj na hlavnej stránke mojej aplikácie!"


# Endpoint pre registráciu používateľa
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400
    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered", "user_id": user.id}), 201


# Endpoint pre pridanie pripomienky
@app.route('/api/reminder', methods=['POST'])
def add_reminder():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    reminder_time_str = data.get('reminder_time')  # očakáva sa formát "HH:MM:SS"
    time_obj = datetime.strptime(reminder_time_str, "%H:%M:%S").time()

    if not all([user_id, title, reminder_time_str]):
        return jsonify({"message": "user_id, title and reminder_time are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404


    reminder = Reminder(title=title, reminder_time=time_obj, user_id=user.id)
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder added", "reminder_id": reminder.id}), 201


# Endpoint pre zobrazenie všetkých pripomienok používateľa
@app.route('/api/reminders/<int:user_id>', methods=['GET'])
def get_reminders(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    reminders = [
        {
            "id": r.id,
            "title": r.title,
            "reminder_time": r.reminder_time.strftime("%H:%M:%S"),
            "active": r.active
        } for r in user.reminders
    ]
    return jsonify({"reminders": reminders}), 200


# Endpoint na aktualizáciu device tokenu pre push notifikácie
@app.route('/api/update_token', methods=['POST'])
def update_token():
    data = request.get_json()
    user_id = data.get('user_id')
    device_token = data.get('device_token')

    if not user_id or not device_token:
        return jsonify({"message": "user_id and device_token are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.device_token = device_token
    db.session.commit()
    return jsonify({"message": "Device token updated"}), 200


if __name__ == '__main__':
    # Inicializácia APScheduler pre push notifikácie
    init_scheduler(app)
    app.run(debug=True)
