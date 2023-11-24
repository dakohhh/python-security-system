from fastapi import Depends, Request, APIRouter, status
from utils.validate import get_object_id
from validation.model import CreateStudent
from response.response import CustomResponse
from database.crud import fetchone_document
from database.schema import Students
from repository.students import StudentsRepository
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Student"], prefix="/student")


@router.post("/create")
async def create_student(request: Request, student: CreateStudent = Depends()):
    if await StudentsRepository.does_matric_exist(student.matric_no):
        raise BadRequestException(f"matric no '{student.matric_no}' already exists")

    new_student = await StudentsRepository.create_student(student)

    return CustomResponse(
        "created student successfully",
        status=status.HTTP_201_CREATED,
        data=new_student.to_dict(),
    )


@router.patch("/blacklist/{student_id}")
async def blacklist_user(request: Request, student_id: str):
    student = await fetchone_document(Students, id=get_object_id(student_id))

    student.is_blacklisted = True

    student.save()

    return CustomResponse("blacklisted student Successfully", status=status.HTTP_200_OK)


@router.patch("/unblacklist/{student_id}")
async def unblacklist_student(request: Request, student_id: str):
    student = await fetchone_document(Students, id=get_object_id(student_id))

    student.is_blacklisted = False

    student.save()

    return CustomResponse(
        "unblacklisted student successfully", status=status.HTTP_200_OK
    )
