import asyncio
from database.schema import Users
from authentication.auth import auth
from fastapi import APIRouter, Request, Depends, status
from fastapi.templating import Jinja2Templates
from client.response import CustomResponse
from repository.logs import LogsRepository

router = APIRouter(tags=["Security"], prefix="/security")





@router.get("/logs")
async def get_security_logs(request:Request, page_number:int, user:Users=Depends(auth.get_current_user)):

    from pprint import pprint

    pprint(user.to_dict())
    # return CustomResponse("get all security videos", status.HTTP_200_OK, data=data)


    return None




@router.post("/register")
async def register_security_personnel(request:Request, user:Users=Depends(auth.get_current_user)):


    


    return CustomResponse("created security personnel")









    


