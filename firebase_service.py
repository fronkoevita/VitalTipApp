import firebase_admin
from firebase_admin import credentials, messaging
import os

# Načítaj cestu k JSON so service account
SERVICE_ACCOUNT_PATH = os.environ.get("FIREBASE_SERVICE_ACCOUNT", "credentials/serviceAccountKey.json")


# Inicializácia Firebase len raz (singleton pattern)
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_app = firebase_admin.initialize_app(cred)

def send_push_notification(token: str, title: str, body: str):
    """
    Odošle push notifikáciu cez Firebase Cloud Messaging (v1).
    :param token: Device token prijímateľa
    :param title: Nadpis správy
    :param body: Obsah správy
    :return: výsledok z Firebase
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    response = messaging.send(message, app=firebase_app)
    return response
