import os
import json

import asyncio
from typing import List
from fastapi import (
    Depends,
    File,
    Request,
    APIRouter,
    BackgroundTasks,
    Security,
    UploadFile,
    status,
)
from fastapi.templating import Jinja2Templates
from exceptions.custom_exception import BadRequestException
from repository.student import StudentRepository
from repository.users import UsersRepository
from repository.security import SecurityPersonnelRepository
from authentication.bearer import get_current_user
from utils.image import ProcessImages
from serializers.student import AllStudentSerializer
from serializers.security_personnel import AllSecurityPersonnelSerializer

from utils.notifications import notify_user_by_email, notify_users_by_phone
from validation.model import (
    CreateStudent,
    NotifySchema,
    CreateUser,
    CreateSecurityPersonnel,
)
from client.response import CustomResponse
from database.schema import Users

router = APIRouter(tags=["User"], prefix="/user")


templates = Jinja2Templates(directory="templates")


@router.post("/notify")
async def notify_user(
    request: Request, notify: NotifySchema, background_task: BackgroundTasks
):
    security_staffs = await StudentRepository.get_security_personnel_staffs()

    print("start sending")

    background_task.add_task(
        notify_users_by_phone,
        staffs=security_staffs,
        camera=notify.camera,
        time_of_detection=notify.time_of_detection,
    )

    return CustomResponse("notified user successfully")


from authentication.auth import auth


@router.post("/signup")
async def signup(
    request: Request,
    user: CreateUser,
):
    if await UsersRepository.get_user_by_email(email=user.email):
        raise BadRequestException("email already exist")

    new_user = await UsersRepository.create_user(user)

    return CustomResponse(
        "created user successfully",
        status=status.HTTP_201_CREATED,
        data=new_user.to_dict(),
    )


@router.post("/create/student")
async def create_student(
    request: Request,
    background_task: BackgroundTasks,
    student: CreateStudent = Depends(),
    admin: Users = Depends(auth.get_current_user),
):

    if await StudentRepository.does_matric_no_exists(student.matric_no):
        raise BadRequestException(f"matric no '{student.matric_no}' already exists")

    new_student = asyncio.create_task(StudentRepository.create_student(student))

    if len(student.images) != 9:
        raise BadRequestException("must be exactly 9 images to be fitted")

    model_images = ProcessImages(student.images)

    model_images.validate()

    new_student = await new_student

    new_student.encodings = model_images.get_face_encodings()

    new_student.save()

    context = {"student": new_student.to_dict()}

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_201_CREATED,
        data=context,
    )


@router.post("/create/security_personnel")
async def create_security_personnel(
    request: Request,
    security_personnel: CreateSecurityPersonnel = Depends(),
    admin: Users = Depends(auth.get_current_user),
):

    if await SecurityPersonnelRepository.does_staff_id_exists(
        security_personnel.staff_id
    ):
        raise BadRequestException(
            f"staff id '{security_personnel.staff_id}' already exists"
        )

    new_security_personnel = asyncio.create_task(
        SecurityPersonnelRepository.create_security_personnel(security_personnel)
    )

    if len(security_personnel.images) != 9:
        raise BadRequestException("must be exactly 9 images to be fitted")

    model_images = ProcessImages(security_personnel.images)

    model_images.validate()

    new_security_personnel = await new_security_personnel

    new_security_personnel.encodings = model_images.get_face_encodings()

    new_security_personnel.save()

    context = {"security_personnel": new_security_personnel.to_dict()}

    return CustomResponse(
        "created security personnel successfully",
        status=status.HTTP_201_CREATED,
        data=context,
    )


@router.get("/students")
async def get_students(
    request: Request,
    admin: Users = Depends(auth.get_current_user),
):

    students = await StudentRepository.get_all_students_without_encodings()

    serialize_students = AllStudentSerializer(students=list(students)).model_serialize

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_200_OK,
        data=serialize_students,
    )


@router.get("/security_personnel")
async def get_security_personnel(
    request: Request,
    admin: Users = Depends(auth.get_current_user),
):

    security_personnels = (
        await SecurityPersonnelRepository.get_all_security_personnel_without_encoding()
    )

    serialize_security_personnels = AllSecurityPersonnelSerializer(
        security_personnels=list(security_personnels)
    ).model_serialize

    return CustomResponse(
        "created security personnel successfully",
        status=status.HTTP_200_OK,
        data=serialize_security_personnels,
    )
