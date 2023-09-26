from fastapi import APIRouter, Request, Depends, status
from authentication.bearer import get_current_user
from fastapi.templating import Jinja2Templates
from database.schema import Users, Recordings
from response.response import CustomResponse
from utils.camera import Camera


router = APIRouter(tags=["Security"], prefix="/security")

templates = Jinja2Templates(directory="templates")







@router.get("/videos")
def get_security_videos(request:Request, page_number:int, user:Users=Depends(get_current_user)):

    per_page = 10   # Amount of Orders per page/request 

    offset = (page_number - 1) * per_page

    recordings = Recordings.objects().order_by('-updated_at').skip(offset).limit(per_page)

    total_orders = Recordings.objects().count()

    data = {
        "recordings": recordings,
        "page_number": page_number,  
        "per_pages": per_page,
        "total_pages": (total_orders + per_page - 1) // per_page,
    }

    return CustomResponse("get all security videos", status.HTTP_200_OK, data=data)





    


