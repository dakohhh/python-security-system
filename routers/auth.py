from fastapi import APIRouter, Request, status
from authentication.auth import authenticate_user
from database.schema import Users
from database.crud import fetchone_document
from repository.users import UsersRepository
from response.response import CustomResponse
from validation.model import CreateUser, LoginSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login")
async def login_user(request: Request, login_input: LoginSchema):
    token = await authenticate_user(login_input.email, login_input.password)

    return CustomResponse("login user successfully", data=token)
