import asyncio
from fastapi_mail import FastMail
from client import send_sms
from .mail import conf, get_notify_message_schema


async def notify_user_by_email(emails: list, camera: int, link: str, time_of_detection):
    message = get_notify_message_schema(emails, camera, link, time_of_detection)

    mail = FastMail(conf)

    asyncio.create_task(mail.send_message(message))


async def notify_user_by_phone(phone_number, camera, time_of_detection):
    message = f"""
    <p>Hello user, we have noticed some suspicious detections from camera {camera}</p> 
    <p>Details Of Detections</p>
    ============================
    <br>
    Location: Camera {camera}
    <br>
    Time: {time_of_detection}
    <br>"""

    response = send_sms(phone_number, message)

    print(response)
