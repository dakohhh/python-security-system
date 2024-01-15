import os
import requests
from .request import SMSClient



SMS_BASE_URL = os.getenv("BASE_SMS_URL")
SMS_SENDER = os.getenv("SMS_SENDER")
SMS_USER_NAME = os.getenv("SMS_USER_NAME")
SMS_PASSWORD = os.getenv("SMS_PASSWORD")


def send_sms(phone_number: str, message: str) -> requests.Response:
    sms_client = SMSClient(SMS_BASE_URL)

    params = {
        "username": SMS_USER_NAME,
        "password": SMS_PASSWORD,
        "sender": SMS_SENDER,
        "recipient": f"@@{phone_number}@@",
        "message": message,
    }

    response = sms_client.get(params=params)

    return response
