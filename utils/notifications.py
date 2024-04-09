import asyncio
from typing import List
from fastapi_mail import FastMail
from client import send_sms
from database.schema import SecurityPersonnel
from .mail import conf, get_notify_message_schema


async def notify_user_by_email(emails: list, camera: int, link: str, time_of_detection):
    message = get_notify_message_schema(emails, camera, link, time_of_detection)

    mail = FastMail(conf)

    asyncio.create_task(mail.send_message(message))


async def notify_users_by_phone(
    security_personnel: List[SecurityPersonnel], camera, time_of_detection
):

    async def send_bulk_sms(phone_numbers: list, message: str):
        tasks = [send_sms(phone_number, message) for phone_number in phone_numbers]
        await asyncio.gather(*tasks)

    phone_security_personnels = [
        personnel.phone_number
        for personnel in security_personnel
        if personnel.is_security_personnel
    ]

    message = f"""
    <p>Hello user, we have noticed some suspicious detections from camera {camera}</p> 
    <p>Details Of Detections</p>
    ============================
    <br>
    Location: Camera {camera}
    <br>
    Time: {time_of_detection}
    <br>"""

    await send_bulk_sms(phone_security_personnels, message)
