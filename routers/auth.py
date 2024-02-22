from fastapi import APIRouter, Request, status
from authentication.auth import auth
from database.schema import Users
from repository.users import UsersRepository
from client.response import CustomResponse
from validation.model import CreateUser, LoginSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Auth"], prefix="/auth")



@router.post("/login")
async def login_user(request: Request, login_input: LoginSchema):

    token = await auth.authenticate_user(login_input)

    return CustomResponse("login user successfully", data=token)
