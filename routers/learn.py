import io
import os
import cv2
import face_recognition
import asyncio
from fastapi import Depends, Request, APIRouter, UploadFile, File, Form, BackgroundTasks
from database.crud import fetchone_document
from authentication.bearer import get_current_user
from database.schema import Students, Users
from repository.students import StudentsRepository
from exceptions.custom_exception import BadRequestException, NotFoundException
from utils.file import save_image_file_to_student
from utils.model import SecurityModel
from response.response import CustomResponse
from utils.validate import verify_image, get_object_id


router = APIRouter(tags=["Learn"], prefix="/learn")


@router.get("/needs_training")
async def student_have_data(request: Request, admin: Users = Depends(get_current_user)):
    from pprint import pprint
    students = await StudentsRepository.get_all_students()

    for i in students:
        pprint(i)

    student_ids = [str(student.id) for student in students]

    path = os.path.join(os.getcwd(), "models/class_dict.json")

    class_dict = SecurityModel.get_class_dict(path)

    student_ids_set = set(student_ids)

    unknown_ids_set = set(class_dict)

    matching_ids = list(student_ids_set.intersection(unknown_ids_set))

    if matching_ids == []:
        raise BadRequestException(
            "looks like new data has been added, the security model needs to be trained!"
        )

    return CustomResponse("have student data condition", data=None)


@router.post("/train_data")
async def train(request: Request):
    path_to_data = "static/model_data"

    path_to_save_model = os.path.join(os.getcwd(), "tf_face_model.h5")

    security_model = SecurityModel(path_to_data, path_to_save_model)

    loss, accuracy = await security_model.train_evaluate_update(3)

    print(loss)

    print(accuracy)

    data = {"accuracy": accuracy, "loss": loss}

    return CustomResponse("model Trained Successfully", data=data)
