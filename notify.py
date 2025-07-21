import requests
import json
from constants import TOKEN

HA_URL = "http://192.168.1.111:8123"  # or your HA IP
NOTIFY_SERVICE = "notify.notify"  # Adjust to match your device


def sendNotification(message=''):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "message": message,
        "title": "Home Assistant Alert"
    }

    response = requests.post(
        f"{HA_URL}/api/services/{NOTIFY_SERVICE.replace('.', '/')}",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.status_code} - {response.text}")