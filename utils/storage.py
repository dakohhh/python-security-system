import os
import asyncio
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()





cloudinary.config( 
  cloud_name = "do1iufmkf", 
  api_key = "426142844111283", 
  api_secret = "-sJAFceCOjqBqM6dtzyILjsWQmo",
  secure = True
)



async def handle_upload(current_recording_name, user):

    cloudinary.uploader.upload("my_image.jpg")

    metadata = cloudinary.uploader.upload_large("dog.mp4", 
        resource_type = "video",
        public_id = "myfolder/mysubfolder/dog_closeup",
        chunk_size = 6000000,
        eager = [
            { "width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
            { "width": 160, "height": 100, "crop": "crop", "gravity": "south",
                "audio_codec": "none"}],
        eager_async = True,
        eager_notification_url = "https://mysite.example.com/notify_endpoint"
    )


    print(metadata)





async def save_metadata_to_database(metadata:dict, user):

    pass