import asyncio
from database.schema import Users
from authentication.auth import auth
from fastapi import APIRouter, Request, Depends, status
from fastapi.templating import Jinja2Templates
from response.response import CustomResponse
from repository.recordings import RecordingsRepository

router = APIRouter(tags=["Security"], prefix="/securities")





@router.get("/videos")
async def get_security_videos(request:Request, page_number:int, user:Users=Depends(auth.get_current_user)):

    pprint(user.to_dict())

    # per_page = 10   # Amount of Orders per page/request 

    # recordings = asyncio.create_task(RecordingsRepository.pagination(page_number, per_page))

    # total_orders = asyncio.create_task(RecordingsRepository.get_total_recordings())

    
    # data = {
    #     "recordings": await recordings,
    #     "pagination" : {
    #         "page_number": page_number,  
    #         "per_pages": per_page,
    #         "total_pages": (await total_orders + per_page - 1) // per_page,
    #     }
    # }
    

    # return CustomResponse("get all security videos", status.HTTP_200_OK, data=data)


    return None












    


