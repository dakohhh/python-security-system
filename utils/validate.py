from bson import ObjectId
from PIL import Image
from exceptions.custom_exception import BadRequestException




def get_object_id(id:str):
    try:
        return ObjectId(id)
    
    except:
        raise BadRequestException(f"{id} is not a valid object id")
    


def verify_image(image_bytes:bytes):
    try:
        im  = Image.frombytes('RGBA', (128,128), image_bytes, 'raw')

        im.verify()
        return True
    except:
        return False