import asyncio
from fastapi import UploadFile

async def save_image(image:UploadFile):

    image_data = asyncio.create_task(image.read())


    if not verify_image(await image_data):
        raise BadRequestException("invalid image or image type")

    image_data = io.BytesIO(await image_data)

    _image = face_recognition.load_image_file(image_data)

    face_locations = face_recognition.face_locations(_image)

    if not face_locations:
        raise BadRequestException("cannot process this image, No face was found.")
