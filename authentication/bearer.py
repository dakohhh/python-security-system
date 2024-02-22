from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from database.crud import fetchone_document
from database.schema import Users
from utils.validate import get_object_id


bearer = HTTPBearer()





async def get_current_user(request:Request, data:HTTPAuthorizationCredentials=Depends(bearer)) -> Users:


    access_token_data = verify_access_token(data.credentials)


    user =  await fetchone_document(Users, id=get_object_id(access_token_data.user))

    return user







