from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    device_token = db.Column(db.String(255), nullable=True)  # token pre push notifikácie
    reminders = db.relationship('Reminder', backref='user', lazy=True)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # napr. "Vypiť vodu" alebo "Užiť liek"
    reminder_time = db.Column(db.Time, nullable=False)
    last_sent = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)
