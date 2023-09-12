from fastapi import Request, APIRouter, BackgroundTasks, status
from fastapi.templating import Jinja2Templates
from validation.model import NotifySchema, CreateUser
from authentication.hashing import hashPassword
from response.response import CustomResponse
from database.crud import fetchall_documents
from database.schema import Users
from utils.notifications import notify_user_by_email


router = APIRouter(tags=["User"], prefix="/user")


templates = Jinja2Templates(directory="templates")





@router.post("/notify")
async def notify_user(request:Request, notify:NotifySchema, background_task:BackgroundTasks):


    emails = [user.email for user in await fetchall_documents(Users)]


    background_task.add_task(notify_user_by_email, emails, notify.camera, notify.link, notify.detected_user, notify.time_of_detection)
    

    return CustomResponse("Notified user successfully")






# @router.get("/get_users")
# async def get_users(request:Request):

#     get_user_task = asyncio.create_task(fetchall(Users))

#     class_list = asyncio.create_task(get_class_dict())

#     users = [user.to_dict() for user in await get_user_task]

#     class_list = await class_list
    
#     needs_train = False

#     if len(users) > len(class_list):
    
#         needs_train = True

#     print(needs_train)
    
    
#     context = {"request":request, "users":users, "needs_train": needs_train}
        
#     return templates.TemplateResponse("view.html", context)







# @router.post("/")
# async def add_user(request:Request, user:CreateUser):

#     new_user = Users(firstname=user.firstname, lastname=user.lastname, email=user.email, password=hashPassword(user.password))

#     new_user.save()

#     return CustomResponse("Added User Successfully", status=status.HTTP_201_CREATED)




# @router.patch("/blacklist/{user_id}")
# async def blacklist_user(request:Request, user_id:str):
#     user = await fetchone_document(Users, id=get_object_id(user_id))

#     user.is_blacklisted = True

#     user.save()

#     return CustomResponse("Blacklisted User Successfully", status=status.HTTP_200_OK)




# @router.patch("/unblacklist/{user_id}")
# async def unblacklist_user(request:Request, user_id:str):
#     user = await fetchone_document(Users, id=get_object_id(user_id))

#     user.is_blacklisted = False

#     user.save()

#     return CustomResponse("Unblacklisted User Successfully", status=status.HTTP_200_OK)
    


# @router.post("/add-image")
# async def add_image(user_id:str =Form(...), image:UploadFile = File(...)):

#     image_data = asyncio.create_task(image.read())

#     get_user_task =  asyncio.create_task(fetchone_document(Users, id=get_object_id(user_id)))

#     if not verify_image(await image_data):
#         raise BadRequestException("Invalid image or image type")

#     user = await get_user_task

#     if not user:
#         raise NotFoundException("User does not exist")


#     image_data = io.BytesIO(await image_data)

#     _image = face_recognition.load_image_file(image_data)

#     face_locations = face_recognition.face_locations(_image)

#     if not face_locations:
#         raise BadRequestException("Cannot proccess, No face found in the image.")


#     top, right, bottom, left = face_locations[0]

#     cropped_image = face_recognition.load_image_file(image_data)

#     cropped_image = cropped_image[top:bottom, left:right]

#     cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

#     file_path_for_user = os.path.join(os.getcwd(), f"static/model_data/{user_id}")

#     os.makedirs(file_path_for_user, exist_ok=True)

#     save_image_file_to_user(cropped_image, file_path_for_user)           

#     return CustomResponse("Added Image To User Successfully")


