import asyncio
from utils.image import ModelImage
from validation.model import CreateStudent
from response.response import CustomResponse
from repository.students import StudentsRepository
from exceptions.custom_exception import BadRequestException
from fastapi import Depends, Request, APIRouter, status, BackgroundTasks



router = APIRouter(tags=["Student"], prefix="/student")


@router.post("/create")
async def create_student(
    request: Request,
    background_task: BackgroundTasks,
    student: CreateStudent = Depends(),
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
async def blacklist_user(request: Request, student_id: str):
    await StudentsRepository.blacklist_student(student_id)

    return CustomResponse("blacklisted student Successfully", status=status.HTTP_200_OK)


@router.patch("/unblacklist/{student_id}")
async def unblacklist_student(request: Request, student_id: str):
    await StudentsRepository.unblacklist_student(student_id)

    return CustomResponse(
        "unblacklisted student successfully", status=status.HTTP_200_OK
    )
