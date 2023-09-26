from fastapi import APIRouter, Request, status
from authentication.auth import authenticate_user
from authentication.hashing import hashPassword
from database.schema import Users
from database.crud import insert_user_document, fetchone_document
from response.response import CustomResponse
from validation.model import CreateUser, LoginSchema
from exceptions.custom_exception import BadRequestException




router = APIRouter(tags=["Auth"], prefix="/auth")



@router.post("/login")
async def login_user(request:Request, login_input: LoginSchema):

    token = await authenticate_user(login_input.email, login_input.password)


    return CustomResponse("login user successfully", data=token)



@router.post("/create")
async def add_user(request:Request, user:CreateUser):

    if await fetchone_document(Users, email=user.email):

        raise BadRequestException("Email already exist")



    new_user =  await insert_user_document(firstname=user.firstname, lastname=user.lastname, email=user.email, password=hashPassword(user.password))

    return CustomResponse("Added User Successfully", status=status.HTTP_201_CREATED, data=new_user.to_dict())