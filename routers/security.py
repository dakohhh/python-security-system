import os
import cv2
import numpy as np
import asyncio
import face_recognition
from typing import List
from database.schema import Users
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from utils.camera import Camera
from utils.model import get_model, get_class_dict

from utils.video_func import adjust_text_size

router = APIRouter(tags=["Security"], prefix="/security")

templates = Jinja2Templates(directory="templates")





camera = Camera()

camera.arm()


@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})





@router.get('/feed')
async def video_feed():
    all_users = Users.objects.all()

    return StreamingResponse(detect_faces(all_users), media_type='multipart/x-mixed-replace; boundary=frame')