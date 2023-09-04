import asyncio
from fastapi_mail import FastMail
from .mail import conf, get_notify_message_schema







async def notify_user_by_email(user, camera, link, detected_user, time_of_detection):

    message = get_notify_message_schema(user, camera, link, detected_user, time_of_detection)

    mail = FastMail(conf)

    asyncio.create_task(mail.send_message(message))
