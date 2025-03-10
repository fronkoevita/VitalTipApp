import os
import json
import base64
from firebase_admin import credentials, initialize_app, messaging

encoded_creds = os.environ.get("FIREBASE_CREDENTIALS")
if not encoded_creds:
    raise ValueError("FIREBASE_CREDENTIALS not set in Heroku Config Vars")

decoded_json = base64.b64decode(encoded_creds).decode("utf-8")
creds_dict = json.loads(decoded_json)

cred = credentials.Certificate(creds_dict)
firebase_app = initialize_app(cred)


def send_push_notification(token: str, title: str, body: str):
    """
    Sends a push notification via Firebase Cloud Messaging (FCM v1).

    :param token: Device token of the recipient
    :param title: Notification title
    :param body: Notification body text
    :return: The response from Firebase
    """
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token
    )
    response = messaging.send(message, app=firebase_app)
    return response
