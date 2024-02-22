import os
import asyncio
from typing import List
from fastapi import Depends, Request, APIRouter, BackgroundTasks, Security, status
from fastapi.templating import Jinja2Templates
from exceptions.custom_exception import BadRequestException
from repository.staff import StaffRepository
from repository.users import UsersRepository
from authentication.bearer import get_current_user
from utils.image import ModelImage
from utils.notifications import notify_user_by_email, notify_users_by_phone
from validation.model import CreateStaff, NotifySchema, CreateUser
from client.response import CustomResponse
from database.schema import Users

router = APIRouter(tags=["User"], prefix="/user")


templates = Jinja2Templates(directory="templates")


@router.post("/notify")
async def notify_user(
    request: Request, notify: NotifySchema, background_task: BackgroundTasks
):
    security_staffs = await StaffRepository.get_security_personnel_staffs()

    print("start seding")

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


@router.post("/create/staff")
async def create_staff(
    request: Request,
    background_task: BackgroundTasks,
    staff: CreateStaff = Depends(),
    admin: Users = Depends(auth.get_current_user),
):
    if await StaffRepository.does_staff_id_exist(staff.staff_id):
        raise BadRequestException(f"staff id '{staff.staff_id}' already exists")

    new_staff = asyncio.create_task(StaffRepository.create_staff(staff))

    if len(staff.images) != 9:
        raise BadRequestException("must be exactly 9 images to be fitted")

    model_images = ModelImage(staff.images)

    model_images.validate_images()

    new_staff = await new_staff

    new_staff.encodings = model_images.get_face_encodings()

    new_staff.save()

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_201_CREATED,
        data=None,
    )

