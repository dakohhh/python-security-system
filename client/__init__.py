import os
import json
from urllib import response
import requests
from .request import NotifyClient, SMSClient

from dotenv import load_dotenv

load_dotenv()

SMS_BASE_URL = os.getenv("BASE_SMS_URL")
SMS_SENDER = os.getenv("SMS_SENDER")
SMS_USER_NAME = os.getenv("SMS_USER_NAME")
SMS_PASSWORD = os.getenv("SMS_PASSWORD")

BASE_APP_URL = os.getenv("BASE_APP_URL")


async def send_sms(phone_number: str, message: str) -> requests.Response:
    sms_client = SMSClient(SMS_BASE_URL)

    params = {
        "username": SMS_USER_NAME,
        "password": SMS_PASSWORD,
        "sender": SMS_SENDER,
        "recipient": f"@@{phone_number}@@",
        "message": message,
    }

    response = sms_client.get(params=params)

    print(response)

    return response


def send_notify_request(camera_loc, time_of_detection):
    notify_client = NotifyClient(BASE_APP_URL)

    payload = json.dumps({"camera": camera_loc, "time_of_detection": time_of_detection})

    response = notify_client.post("/user/notify", data=payload)

    return response
