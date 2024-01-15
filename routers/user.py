import os
import asyncio
from fastapi import Depends, Request, APIRouter, BackgroundTasks, status
from fastapi.templating import Jinja2Templates
from exceptions.custom_exception import BadRequestException
from repository.staff import StaffRepository
from repository.users import UsersRepository
from authentication.bearer import get_current_user
from utils.image import ModelImage

# from utils.image import ModelImage
# from utils.model import SecurityModel
from validation.model import CreateStaff, NotifySchema, CreateUser
from client.response import CustomResponse
from database.schema import Users

# from utils.notifications import notify_user_by_email


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
        raise BadRequestException("must be exactly 5 images to be fitted")

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


@router.get("/students_have_data")
async def student_have_data(request: Request, admin: Users = Depends(get_current_user)):
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
