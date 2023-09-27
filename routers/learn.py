import io
import os
import cv2
import face_recognition
import asyncio
from fastapi import Request, APIRouter, UploadFile, File, Form, BackgroundTasks
from database.crud import fetchone_document, change_student_data_status
from database.schema import Users, Students
from exceptions.custom_exception import BadRequestException, NotFoundException
from utils.file import save_image_file_to_student
from utils.model import train_evaluate_update
from response.response import CustomResponse
from utils.validate import verify_image, get_object_id




router = APIRouter(tags=["Learn"], prefix="/learn")





@router.post("/add_student_image")
async def add_image(request:Request, backgroud_task:BackgroundTasks, student_id:str = Form(...), image:UploadFile = File(...)):

    image_data = asyncio.create_task(image.read())

    get_student_task =  asyncio.create_task(fetchone_document(Students, id=get_object_id(student_id)))

    if not verify_image(await image_data):
        raise BadRequestException("invalid image or image type")

    student = await get_student_task

    if not student:
        raise NotFoundException("student does not exist")


    image_data = io.BytesIO(await image_data)

    _image = face_recognition.load_image_file(image_data)

    face_locations = face_recognition.face_locations(_image)

    if not face_locations:
        raise BadRequestException("cannot process this image, No face was found.")


    top, right, bottom, left = face_locations[0]

    cropped_image = face_recognition.load_image_file(image_data)

    cropped_image = cropped_image[top:bottom, left:right]

    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    file_path_for_student = os.path.join(os.getcwd(), f"static/data/{student_id}")

    os.makedirs(file_path_for_student, exist_ok=True)

    save_image_file_to_student(cropped_image, file_path_for_student)

    asyncio.create_task(change_student_data_status(student))

    return CustomResponse("Added Image To student Successfully")







@router.post("/train-data")
async def train(request:Request):

    loss, accuracy = await train_evaluate_update(3, "static/model_data")

    print(loss)

    print(accuracy)

    data = {"accuracy": accuracy, "loss": loss}

    return CustomResponse("Model Trained Successfully", data=data)