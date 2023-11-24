from fastapi import Request, APIRouter, BackgroundTasks, status
from fastapi.templating import Jinja2Templates
from exceptions.custom_exception import BadRequestException
from repository.users import UsersRepository
from validation.model import NotifySchema, CreateUser
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
async def add_user(request: Request, user: CreateUser):
    if await fetchone_document(Users, email=user.email):
        raise BadRequestException("email already exist")

    new_user = await UsersRepository.create_user(user)

    return CustomResponse(
        "created user successfully",
        status=status.HTTP_201_CREATED,
        data=new_user.to_dict(),
    )


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
