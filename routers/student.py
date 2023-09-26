from fastapi import Request, APIRouter, BackgroundTasks, status
from fastapi.templating import Jinja2Templates
from utils.validate import get_object_id
from validation.model import CreateStudent, NotifySchema, CreateUser
from authentication.hashing import hashPassword
from response.response import CustomResponse
from database.crud import fetchall_documents, fetchone_document
from database.schema import Users, Students
from utils.notifications import notify_user_by_email


router = APIRouter(tags=["Student"], prefix="/student")


templates = Jinja2Templates(directory="templates")




@router.post("/create")
async def add_user(request:Request, user:CreateStudent):

    new_user = Students(firstname=user.firstname, lastname=user.lastname, matric_no=user.matric_no)

    new_user.save()

    return CustomResponse("created user successfully", status=status.HTTP_201_CREATED)



@router.patch("/blacklist/{student_id}")
async def blacklist_user(request:Request, student_id:str):
    
    student = await fetchone_document(Students, id=get_object_id(student_id))

    student.is_blacklisted = True

    student.save()

    return CustomResponse("blacklisted student Successfully", status=status.HTTP_200_OK)




@router.patch("/unblacklist/{student_id}")
async def unblacklist_student(request:Request, student_id:str):

    student = await fetchone_document(Students, id=get_object_id(student_id))

    student.is_blacklisted = False

    student.save()

    return CustomResponse("unblacklisted student successfully", status=status.HTTP_200_OK)