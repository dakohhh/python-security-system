from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from utils.camera import Camera


router = APIRouter(tags=["Security"], prefix="/security")

templates = Jinja2Templates(directory="templates")





