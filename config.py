import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tajny_klic')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///health_reminder.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurácia pre FCM (Firebase Cloud Messaging)
    FCM_API_KEY = os.environ.get('FCM_API_KEY', 'tvoj_fcm_api_klic')
