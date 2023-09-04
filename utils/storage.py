import os
import asyncio
import requests
import threading 
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()




cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),

  api_key = os.getenv("CLOUDINARY_API_KEY"), 

  api_secret = os.getenv("CLOUDINARY_API_SECRET"),

  secure = True
)




def handle_upload(name, current_recording_path:str, user={"email": "wisdomdakoh@gmail.com"}):

    print(user)

    metadata = cloudinary.uploader.upload_large(current_recording_path, 
        resource_type = "video",
        public_id = f"python_security/{name}",
        chunk_size = 6000000,
        eager = [
            { "width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
            { "width": 160, "height": 100, "crop": "crop", "gravity": "south",
                "audio_codec": "none"}],
        eager_async = True,
    )


    print(metadata["url"])


    





async def save_metadata_to_database(metadata:dict, user):

    pass



handle_upload("03-09-23-19-01-26", os.path.join(os.getcwd(), "models/03-09-23-19-01-26.avi"), "user")