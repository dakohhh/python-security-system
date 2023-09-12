import os
import certifi
from fastapi import FastAPI
from mongoengine import connect
from routers.user import router as user
from routers.auth import router as auth
from exceptions.custom_exception import *
from dotenv import load_dotenv

from utils.camera import Camera



load_dotenv()



CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")


connect(host=os.getenv("MONGODB_URL"), tls=True, tlsCAFile=CERTIFICATE)


app = FastAPI()



app.include_router(user)
app.include_router(auth)
app.add_exception_handler(UserExistException, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundException, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)




# camera = Camera()

# camera.arm()










