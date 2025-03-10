import os
import json
from firebase_admin import credentials, messaging, initialize_app
from dotenv import load_dotenv

# Load environment variables from .env (locally)
load_dotenv()

# Get the JSON string from the environment variable
json_str = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if not json_str:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT is not set or is empty")

# Convert the JSON string to a Python dictionary
creds_dict = json.loads(json_str)

# Initialize Firebase using the dictionary
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
