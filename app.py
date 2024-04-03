import os
import certifi
from fastapi import FastAPI, File, UploadFile
from mongoengine import connect, errors
import numpy as np
from database.schema import Staffs
from repository.staff import StaffRepository
from routers.user import router as user
from routers.auth import router as auth

# from routers.learn import router as learn
from routers.security import router as security
from client.response import CustomResponse
from fastapi.middleware.cors import CORSMiddleware

from exceptions.custom_exception import *
from dotenv import load_dotenv

from utils.camera import Camera

# from utils.camera import Camera


load_dotenv()


CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")

print(os.getenv("DEVELOPMENT"))

if os.getenv("DEVELOPMENT"):
    connect(host=os.getenv("MONGODB_URL"))

else:
    connect(host=os.getenv("MONGODB_URL_ONLINE"), tls=True, tlsCAFile=CERTIFICATE)


app = FastAPI()


origins = [

    "http://localhost:3009",

    "http://127.0.0.1:5500",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user)
app.include_router(auth)
# app.include_router(learn)
app.include_router(security)
app.add_exception_handler(UserExistException, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundException, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(errors.MongoEngineException, mongo_exception_handler)




staffs = StaffRepository.get_all_staffs()

camera = Camera(staffs)


@app.patch("/security/arm")
def arm_camera(request: Request):
    camera.arm()

    return CustomResponse("Camera is Armed")


@app.patch("/security/disarm")
def arm_camera(request: Request):
    camera.disarm()

    return CustomResponse("Camera is Disarmed")


@app.post("/test_encodings")
def test_encodings(request:Request,  image: UploadFile = File(...)):

    from utils.func import threshold_compare

    staff : Staffs = Staffs.objects().first()

    import face_recognition


    unknown_image = face_recognition.load_image_file(image.file)


    unknown_faces_image_encoding = face_recognition.face_encodings(unknown_image)
    

    print(unknown_faces_image_encoding)

    for i in unknown_faces_image_encoding:

        results = face_recognition.compare_faces(np.array(staff.encodings), i)
        
        print(threshold_compare(results))

    return None