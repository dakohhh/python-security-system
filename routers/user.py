import os
import asyncio
from fastapi import Depends, Request, APIRouter, BackgroundTasks, status
from fastapi.templating import Jinja2Templates
from exceptions.custom_exception import BadRequestException
from repository.students import StudentsRepository
from repository.users import UsersRepository
from authentication.bearer import get_current_user
from utils.image import ModelImage
from utils.model import SecurityModel
from validation.model import CreateStudent, NotifySchema, CreateUser
from response.response import CustomResponse
from database.crud import fetchall_documents, fetchone_document
from database.schema import Users
from utils.notifications import notify_user_by_email


router = APIRouter(tags=["User"], prefix="/user")


templates = Jinja2Templates(directory="templates")


@router.post("/notify")
async def notify_user(
    request: Request, notify: NotifySchema, background_task: BackgroundTasks
):
    emails = [user.email for user in await fetchall_documents(Users)]

    background_task.add_task(
        notify_user_by_email,
        emails,
        notify.camera,
        notify.link,
        notify.detected_user,
        notify.time_of_detection,
    )

    return CustomResponse("notified user successfully")


@router.post("/create")
async def add_user(
    request: Request, user: CreateUser, admin: Users = Depends(get_current_user)
):
    if await fetchone_document(Users, email=user.email):
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
    admin: Users = Depends(get_current_user),
):
    if await StudentsRepository.does_matric_exist(student.matric_no):
        raise BadRequestException(f"matric no '{student.matric_no}' already exists")

    new_student = asyncio.create_task(StudentsRepository.create_student(student))

    images = ModelImage(student.images)

    images.validate_images()

    new_student = await new_student

    images.save_cropped_images(str(new_student.id))

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_201_CREATED,
        data=new_student.to_dict(),
    )


@router.patch("/blacklist/{student_id}")
async def blacklist_user(
    request: Request, student_id: str, admin: Users = Depends(get_current_user)
):
    await StudentsRepository.blacklist_student(student_id)

    return CustomResponse("blacklisted student Successfully", status=status.HTTP_200_OK)


@router.patch("/unblacklist/{student_id}")
async def unblacklist_student(
    request: Request, student_id: str, admin: Users = Depends(get_current_user)
):
    await StudentsRepository.unblacklist_student(student_id)

    return CustomResponse(
        "unblacklisted student successfully", status=status.HTTP_200_OK
    )



@router.get("/students_have_data")
async def student_have_data(request:Request, admin:Users=Depends(get_current_user)):

    path = os.path.join(os.getcwd(), "models/class_dict.json")

    class_dict = SecurityModel.get_class_dict(path)

    print(class_dict)


    return CustomResponse("have student data condition", data=None)




# @router.get("/get_users")
# async def get_users(request:Request):

#     get_user_task = asyncio.create_task(fetchall(Users))

#     class_list = asyncio.create_task(get_class_dict())

#     users = [user.to_dict() for user in await get_user_task]

#     class_list = await class_list

#     needs_train = False

#     if len(users) > len(class_list):

#         needs_train = True

#     print(needs_train)


#     context = {"request":request, "users":users, "needs_train": needs_train}

#     return templates.TemplateResponse("view.html", context)
