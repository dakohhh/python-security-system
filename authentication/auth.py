from .hashing import checkPassword
from .tokens import create_access_token
from database.schema import Users
from database.crud import fetchone_document
from exceptions.custom_exception import BadRequestException


async def authenticate_user(email:str, password:str):

    user = await fetchone_document(Users, email=email)

    if user is None or not checkPassword(password, user.password):
        raise BadRequestException("incorrect email or password")
 
    access_token = create_access_token(str(user.id))

    return access_token