from typing import List, Union
from fastapi import Form
from pydantic import BaseModel, validator
from bson import ObjectId
from email_validator import validate_email, EmailNotValidError
from exceptions.custom_exception import BadRequestException


class TokenData(BaseModel):
    username:str
    user_id: str
    refresh_token: Union[str, None]
    expire: int



class CreateUser(BaseModel):
    firstname:str
    lastname:str
    email:str
    password:str

    @validator("email")
    def validate_email(cls, v):
        try:
            emailinfo = validate_email(v, check_deliverability=True)

            email = str(emailinfo.email)

            return email

        except EmailNotValidError as e:

            raise BadRequestException(str(e))




class CreateStudent(BaseModel):
    firstname:str
    lastname:str
    matric_no:str

    @validator("matric_no")
    def validate_matric_no(cls, v):

        try:
            if len(v) != 11: raise BadRequestException("matric no must be lenght of 10")

            return int(v)
        
        except ValueError as e:
            raise BadRequestException(str(e))




class LoginSchema(BaseModel):
    email:str
    password:str

    @validator("email")
    def validate_email(cls, v):
        try:
            emailinfo = validate_email(v, check_deliverability=False)

            email = str(emailinfo.email)

            return email

        except EmailNotValidError as e:

            raise BadRequestException(str(e))




class NotifySchema(BaseModel):
    camera:str 
    link:str
    detected_user:str 
    time_of_detection:str
