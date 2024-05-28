from multiprocessing import context
import os
import json

import asyncio
from turtle import st
from typing import List
from beanie import PydanticObjectId
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
from exceptions.custom_exception import BadRequestException, NotFoundException
from repository.student import StudentRepository
from repository.university_member import UniversityMemberRepository
from repository.users import UsersRepository
from repository.security import SecurityPersonnelRepository
from repository.staff import StaffRepository
from database.schema import Staff, SecurityPersonnel
from authentication.bearer import get_current_user
from utils.image import ProcessImages
from serializers.student import AllStudentSerializer
from serializers.staff import AllUniversityStaffSerializer
from serializers.security_personnel import AllSecurityPersonnelSerializer

from utils.notifications import notify_user_by_email, notify_users_by_phone
from validation.model import (
    CreateStudent,
    NotifySchema,
    CreateStaff,
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


@router.post("/create/staff")
async def create_staff(
    request: Request,
    staff: CreateStaff = Depends(),
    admin: Users = Depends(auth.get_current_user),
):

    if await UniversityMemberRepository.does_staff_id_exists(staff.staff_id):
        raise BadRequestException(f"staff id '{staff.staff_id}' already exists")

    model_images = ProcessImages(staff.images)

    model_images.validate()

    if staff.is_security_personnel:

        new_staff = asyncio.create_task(
            SecurityPersonnelRepository.create_security_personnel(staff)
        )

    else:
        new_staff = asyncio.create_task(StaffRepository.create_staff(staff))

    if len(staff.images) != 9:
        raise BadRequestException("must be exactly 9 images to be fitted")

    new_staff = await new_staff

    new_staff.encodings = model_images.get_face_encodings()

    new_staff.save()

    context = {"staff": new_staff.to_dict()}

    return CustomResponse(
        "created staff successfully",
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
    # admin: Users = Depends(auth.get_current_user),
):

    students = await StudentRepository.get_all_students_without_encodings()

    serialize_students = AllStudentSerializer(students=list(students)).model_serialize

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_200_OK,
        data=serialize_students,
    )


@router.get("/staff")
async def get_all_university_staffs(
    request: Request,
    # admin: Users = Depends(auth.get_current_user),
):

    university_staffs = await UniversityMemberRepository.all_university_staffs()

    university_staffs = AllUniversityStaffSerializer(staffs=list(university_staffs))

    context = {**university_staffs.model_dump()}

    return CustomResponse(
        "all univerisity staffs",
        status=status.HTTP_200_OK,
        data=context,
    )


@router.delete("/staff/{staff_id}")
async def delete_staff(request: Request, staff_id: PydanticObjectId):
    if not await UniversityMemberRepository.does_staff_exists(staff_id):
        raise NotFoundException("Staff does not exists")

    staff = await UniversityMemberRepository.delete_staff(staff_id)

    context = {}

    return CustomResponse("Deleted Staff successfully", status=status.HTTP_200_OK)


@router.delete("/student/{student_id}")
async def delete_student(request: Request, student_id: PydanticObjectId):
    if not await StudentRepository.does_student_exists(student_id):
        raise NotFoundException("student does not exists")

    await StudentRepository.delete_student(student_id)

    return CustomResponse("Deleted Student successfully", status=status.HTTP_200_OK)
